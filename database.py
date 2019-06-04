import os
import shutil
import time
from bottle import static_file
from PIL import Image

''' Initialises database, if directory "gallery" doesn't exist, creates it '''
def init_database():
    db_path = get_full_path('')
    if not os.path.exists(db_path):
        os.mkdir(db_path)

''' Creates the full path for the specified file or directory '''
def get_full_path(path):
    cwd = os.getcwd()
    return os.path.join(cwd, 'gallery', path)

''' Creates a new gallery (directory) '''
def create_gallery(name):
    try:
        fullpath = get_full_path(name)
        os.mkdir(fullpath)
    except FileExistsError:
        return False

    return name.replace(' ', '%20')   # path

''' Deletes an existing gallery (directory)

returns appropriate HTTP status code
'''
def delete_img_or_gallery(path):
    fullpath = get_full_path(path)

    if not os.path.exists(fullpath):
        # gallery or image does not exist
        return 404

    try:
        if os.path.isdir(fullpath):
            # delete gallery and all images in it
            shutil.rmtree(fullpath)
        else:
            # delete image
            os.remove(fullpath)
    except OSError as e:
        return 500

    # image or gallery successfully removed
    return 200

''' Saves the image (FileUpload instance) to the filesystem '''
def save_image(image, gallery):
    gallery_path = get_full_path(gallery)

    if not os.path.isdir(gallery_path):
        # gallery does not exist
        return False

    save_path = os.path.join(gallery_path, image.filename)
    try:
        image.save(save_path)
    except OSError:
        # file exists, expected behaviour not specified, replacing file
        os.remove(save_path)
        image.save(save_path)

    # generate and return info about the uploaded image
    path = image.filename
    fullpath = '%s/%s' % (gallery, path)
    name = path.split('.')[0].capitalize()   # expecting only 1 '.' in the filename
    modified = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())
    return {"path": path, "fullpath": fullpath, "name": name, "modified": modified}

''' Returns a list of (path, name) for each gallery '''
def get_galleries():
    gallery_path = get_full_path('')
    # get all gallery names
    gallery_names = [d for d in os.listdir(gallery_path)
            if os.path.isdir(os.path.join(gallery_path, d))]

    # create (path, name) tuples
    gallery_info = []
    for name in gallery_names:
        gallery_info.append((
                name.replace(' ', '%20'),   # path
                name ))

    return gallery_info

''' Returns the path and name of the specified gallery_info

if the specified gallery does not exist False is returned
'''
def get_gallery_info(gallery):
    gallery_path = get_full_path(gallery)
    try:
        if not os.path.isdir(gallery_path):
            raise OSError
    except OSError:
        return False

    return {
            'path': gallery.replace(' ', '%20'),
            'name': gallery }

''' Returns a list of all images in the specified gallery '''
def get_images(gallery):
    gallery_path = get_full_path(gallery)
    # get all file names in the gallery
    image_files = [f for f in os.listdir(gallery_path)
            if os.path.isfile(os.path.join(gallery_path, f))]

    # create a list of all images containing information about the images
    images = []
    for filename in image_files:
        fullpath = '%s/%s' % (gallery, filename)
        name = filename.split('.')[0].capitalize()
        modTimesinceEpoc = os.path.getmtime(os.path.join(gallery_path, filename))
        modified = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(modTimesinceEpoc))

        images.append({
                'path': filename,
                'fullpath': fullpath,
                'name': name,
                'modified': modified })

    return images

''' Returns an image (static_file) with the specified width and height '''
def get_image(w, h, path):
    fullpath = get_full_path(path)

    if not os.path.exists(fullpath):
        # image does not exist
        raise ValueError(404)

    try:
        w_int = int(w)
        h_int = int(h)
    except:
        # w, h parameters are not set propperly
        raise ValueError(500)

    image = Image.open(fullpath)

    # if neither width nor height is specified, size can not be calculated
    if w_int == 0 and h_int == 0:
        raise ValueError(500)

    width, height = image.size
    ratio = width/height
    if w_int == 0:
        w_int = int(h_int * ratio)
    elif h_int == 0:
        h_int = int(w_int / ratio)

    # resize the image according to given params
    resized_img = image.resize((w_int, h_int))
    # create a temporary file for the resized image
    resized_img_path = fullpath.replace('.', '_tmp.')
    resized_img.save(resized_img_path, 'JPEG')

    image_response = static_file(path.replace('.', '_tmp.'), root=os.path.join(os.getcwd(), 'gallery'), mimetype='image/jpeg')
    # remove temporary image file
    os.remove(resized_img_path)

    return image_response
