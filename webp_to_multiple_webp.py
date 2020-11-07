# cmd> python webp_to_multiple_webp.py folder-name 80

import sys, os
from subprocess import call
from glob import glob
from PIL import Image

def append_text_to_file(text):
    f = open("images.html", "a")
    f.write(text)
    f.close()

def reset_output_file():
    f = open("images.html", "w")
    f.write("")
    f.close()

def remove_if_exists_as_webp(fileName):
    if(os.path.exists(fileName.split('.')[0]+'.webp')):
        os.remove(fileName.split('.')[0]+'.webp')
        print("File .webp exists : removing " + fileName.split('.')[0]+'.webp')

def get_webp_filename_in_dir(dir_path):
    img_list = []
    if(os.path.exists(dir_path)):
        for img_name in glob(path+'/*'):
            if img_name.endswith(".webp"):
                img_list.append(os.path.basename(img_name))
        return img_list

def get_list_desired_width():
    res_list = [320,480,800,1200]
    return res_list

def rename_filename(old_filename, new_filename):
    os.rename(path +'/'+old_filename, path +'/'+new_filename)

def get_height_of_webp(filename):
    im = Image.open(path +'/'+filename)
    im.size
    return im.size[1]

def get_width_of_webp(filename):
    im = Image.open(path +'/'+filename)
    im.size
    return im.size[0]

def generate_all_webp(filename):
    img_filename = []
    for res in get_list_desired_width():
        tmp_filename = (filename.split('.')[0])+'-temp.webp'
        remove_if_exists_as_webp(tmp_filename)
        if(res < get_width_of_webp(filename)):
            cmd='cwebp '+path+'/'+filename+' -q '+quality+' -o '+path+'/'+tmp_filename+' -resize '+str(res)+' 0'
            os.system(cmd)
            new_filename = filename.split('.')[0]+'-'+str(res)+'x'+str(get_height_of_webp(tmp_filename))+'.webp'
            rename_filename(tmp_filename, new_filename)
            img_filename.append((res,new_filename))
    return (filename,img_filename)

#[('debarras.webp', [(320, 'debarras-320x427.webp'), (480, 'debarras-480x640.webp'), (800, 'debarras-800x1067.webp'), (1200, 'debarras-1200x1600.webp')])]
def generate_html(data):
    html = ""
    for image_data in data:
        image_name = image_data[0]
        html += '<img src="./'+path+'/'+image_name+'" srcset="'
        for subdata in image_data[1]:
            html += './'+path+'/'+subdata[1] + ' ' + str(subdata[0]) + 'w,'
        html = html[0:len(html)-1]
        html += '" />'
        append_text_to_file(html)
        html = ""

path = sys.argv[1]
quality = sys.argv[2]

if int(quality) < 0 or int(quality) > 100:
    print("image quality out of range[0-100] ;/:/")
    sys.exit(0)
reset_output_file()
img_list = get_webp_filename_in_dir(path)
output = []
for img_name in img_list:
    output.append(generate_all_webp(img_name))
print(output)
generate_html(output)
