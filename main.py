from PIL import Image, ExifTags
from datetime import datetime
from os import listdir, getcwd, mkdir
from os.path import join, abspath, isdir
from shutil import move

ROOT_DIRECTORY = getcwd()

#36867 is a static tag for date look at documentation 
#https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif/datetimeoriginal.html
def get_date_image_was_shot_from_metadata(path):
    return Image.open(path)._getexif()[36867]

def strip_date(date):
    date_object = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
    return date_object.strftime('%Y-%m-%d')

def get_dictionary_of_pictures_and_dates_for_file_extension(f_ext):
    dates_dict = {}
    for file in listdir(ROOT_DIRECTORY):
        if file.endswith(f_ext):
            dates_dict[file] = strip_date((get_date_image_was_shot_from_metadata(abspath(file))))
    return dates_dict


def get_dates_set_for_dict(dates_dict : dict):
    dates_set = set(dates_dict.values())
    return dates_set

def create_folders_structure_from_set(dates_set):
    for date in dates_set:
        date_folder_path = join(ROOT_DIRECTORY, date)
        if isdir(date_folder_path) is False:
            mkdir(date_folder_path)
            jpg_subfolder_path = join(date_folder_path, "JPGs")
            raws_subfolder_path = join(date_folder_path, "RAWs")
            mkdir(jpg_subfolder_path)
            mkdir(raws_subfolder_path)

def move_pictures_to_folder(dates_dict):
    for file_name in dates_dict.keys():
        original = join(ROOT_DIRECTORY, file_name)
        destination = join(ROOT_DIRECTORY, f"{dates_dict[file_name]}/JPGs/{file_name}" )
        move(original, destination)

def execute():
    dates_dict_jpgs = get_dictionary_of_pictures_and_dates_for_file_extension(".JPG")
    dates_set = get_dates_set_for_dict(dates_dict_jpgs)
    create_folders_structure_from_set(dates_set)
    move_pictures_to_folder(dates_dict_jpgs)

def main():
    execute()


if __name__  == "__main__":
    main()
