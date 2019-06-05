# programatorAPI
Implementation of the programator.sk API

## Files
- **main.py:** starts the server on port 8080.
- **gallery.py:** controller for routes /gallery and /gallery/{path}.
- **images.py:** controller for route /image/{w}x{h}/{path}.
- **database.py:** manages database (filesystem is used as database).
- **FBlogin.py:** handles user authorization. Note that images can not be uploaded without a token in the Authorizaton header.

## Use
*python3 main.py* starts the server on port 8080

## Dependencies
- This project uses the bottle framework
- Module PIL is also used for resizing images
- Facebook SDK for Python for getting the users ID
