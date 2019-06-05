import bottle
import gallery
import images
import FBlogin
import database as db

db.init_database()

app = application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8080)
