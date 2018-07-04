# Importing modules
import functools
import tornado.web
import tornado.ioloop
import json


class AuthHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        user = self.get_current_user()
        if not user:
            raise tornado.web.HTTPError(401, "Access denied")

        self.write("Welcome back, {}".format(user))
