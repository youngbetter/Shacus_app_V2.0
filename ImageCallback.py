# -*-coding: utf-8 -*-


from BaseHandler import BaseHandler

class ImageCallback(BaseHandler):
    def post(self):
        print('\n---------headers\n')
        print (self.request.headers)
        print('\n---------uri\n')
        print (self.request.uri)
        print ('\n--------youip\n')
        print (self.request.remote_ip)