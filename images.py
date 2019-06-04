from bottle import request, response, get, static_file
import database as db
import json

''' Generates a preview image with the specified width and height '''
@get('/images/<w>x<h>/<path:re:.+>')
def generate_image_preview(w, h, path):
    try:
        image = db.get_image(w, h, path)
    except ValueError as e:
        response.status = e.args[0]
        return

    return image
