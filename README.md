# programatorAPI
Implementation of the programator.sk API

## Files
- **main.py:** starts the server on port 8080
- **gallery.py:** controller for routes /gallery and /gallery/{path}
- **images.py:** controller for route /image/{w}x{h}/{path}
- **database.py:** manages database (filesystem is used as database)

## Use
python3 main.py starts the server on port 8080

## Dependencies
- This project uses the bottle framework
- Module PIL is also used for resizing images
