# cmd> python dir_files_to_webp.py folder-name 80

import sys, os
from subprocess import call
from glob import glob

def remove_if_exists_as_webp(fileName):
    if(os.path.exists(fileName.split('.')[0]+'.webp')):
        os.remove(fileName.split('.')[0]+'.webp')
        print("File .webp exists : removing " + fileName.split('.')[0]+'.webp')

def get_jpg_jpeg_png_filename_in_dir(dir_path):
    img_list = []
    if(os.path.exists(dir_path)):
        for img_name in glob(path+'/*'):
            if img_name.endswith(".jpg") or img_name.endswith(".png") or img_name.endswith(".jpeg"):
                img_list.append(os.path.basename(img_name))
        return img_list

#folder-name
path = sys.argv[1]
#quality of produced .webp images [0-100]
quality = sys.argv[2]
#resize width
#width = sys.arg[3]

if int(quality) < 0 or int(quality) > 100:
    print("image quality out of range[0-100] ;/:/")
    sys.exit(0)

img_list = get_jpg_jpeg_png_filename_in_dir(path)

print(img_list)   # for debug

for img_name in img_list:
    remove_if_exists_as_webp(path+'/'+img_name)
    # though the chances are very less but be very careful when modifying the below code
    cmd='cwebp '+path+'/'+img_name+' -q '+quality+' -o '+path+'/'+(img_name.split('.')[0])+'.webp'
    # running the above command
    os.system(cmd)
    print(cmd)    # for debug

