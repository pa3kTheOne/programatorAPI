from bottle import request, response
from bottle import post, get, put, delete
import database as db
import json
from FBlogin import get_FBuser_id

''' Creates a new gallery '''
@post('/gallery')
def create_gallery():
    try:
        data = request.json
        if data is None:
            raise ValueError

        # extract gallery name
        try:
            name = data['name']
        except (TypeError, KeyError):
            raise ValueError

        # gallery name cannot contain '/'
        if '/' in name:
            raise ValueError

        # create gallery
        path = db.create_gallery(name)
        if not path:
            # gallery with this name already exists
            raise NameError

    except ValueError:
        response.status = 400
        response.headers['Content-Type'] = 'application/json'
        return json.dumps({
                'code': 400,
                'payload': {
                    'paths': ['name'],
                    'validator': 'required',
                    'example': None
                },
                'name': 'INVALID_SCHEMA',
                'description': 'Bad JSON object: u\'name\' is a required property'
                })
    except NameError:
        response.status = 409
        return

    # gallery successfully created, return code 201
    response.status = 201
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'path': path, 'name': name})

''' Returns a list of all galleries and images in them '''
@get('/gallery')
def get_galleries():
    # get gallery paths and names
    galleries_info_noimg = db.get_galleries()

    # get images
    galleries_info = []
    for path, name in galleries_info_noimg:
        gallery = {
                'path': path,
                'name': name,
                }
        # get images from the current gallery
        imgs = db.get_images(name)
        if imgs:
            gallery['image'] = imgs[0]

        galleries_info.append(gallery)

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'galleries': galleries_info})

''' Returns a list of all images in the specified gallery '''
@get('/gallery/<path>')
def get_gallery_info(path):
    # get info about the specified gallery to check if it exists
    gallery_info = db.get_gallery_info(path)

    if not gallery_info:
        # gallery does not exist
        response.status = 404
        return

    # get all images in the specified gallery
    images = db.get_images(path)

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'gallery': gallery_info, 'images': images})

''' Deletes the specified gallery or image '''
@delete('/gallery/<path:re:.+>')
def delete_img_or_gallery(path):
    status = db.delete_img_or_gallery(path)
    response.status = status
    return

''' Extracts the bearer token from the Autorization header of the request '''
def extract_bearer_token():
    bearer = request.headers['Authorization']
    token = bearer.replace('Bearer ', '')
    return token

''' Uploads image to the specified gallery '''
@post('/gallery/<path>')
def upload_image(path):
    # get token from Authorization header
    try:
        token = extract_bearer_token()
        if not token:
            raise ValueError
        # get the users id
        user_id = get_FBuser_id(token)
    except:
        # no authorization provided or an error occured while retrieving user information
        # request must be authorized, returning without uploading the file
        response.status = 401
        return


    try:
        file = request.files.get('image')

        # only allow upload of jpg files
        if file.content_type != 'image/jpeg':
            raise ValueError
    except:
        response.status = 400
        return

    info = db.save_image(file, path, user_id)
    if not info:
        # gallery not found
        response.status = 404
        return

    response.status = 201
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'uploaded': [info]})
