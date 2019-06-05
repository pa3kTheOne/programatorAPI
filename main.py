'''
HTTPS
'''
# import bottle
# import gallery
# import images
# import FBlogin
# import database as db
#
# class SSLWSGIRefServer(bottle.ServerAdapter):
#     def run(self, handler):
#         from wsgiref.simple_server import make_server, WSGIRequestHandler
#         import ssl
#         if self.quiet:
#             class QuietHandler(WSGIRequestHandler):
#                 def log_request(*args, **kw): pass
#             self.options['handler_class'] = QuietHandler
#         srv = make_server(self.host, self.port, handler, **self.options)
#         srv.socket = ssl.wrap_socket (
#          srv.socket,
#          certfile='./keys/server.pem',  # path to certificate
#          server_side=True)
#         srv.serve_forever()
#
# db.init_database()
#
# # context = ('./keys/server.pem', './keys/server.pem')
# # context = SSL.Context(SSL.SSLv23_METHOD)
# # context.use_privatekey_file('./keys/server.pem')
# # context.use_certificate_file('./keys/server.pem')
#
# app = application = bottle.default_app()
#
# if __name__ == '__main__':
#     srv = SSLWSGIRefServer(host="127.0.0.1", port=443)
#     bottle.run(server=srv)
#     # bottle.run(host = '127.0.0.1', port = 80, server=SSLCherryPyServer, debug=True)

'''
HTTP
'''
import bottle
import gallery
import images
import FBlogin
import database as db

db.init_database()

app = application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 80)
