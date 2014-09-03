#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gi.repository import Gtk

import os, sys, json, sqlite3

import vk_auth, api, db

builder   = False
window    = False
client_id = "4508898"
APP_DIR   = os.path.dirname(os.path.realpath(__file__)) + "/"

class Handler():
    def __init__(self):
        self.auth = False

    def enter(self, object):
        global client_id

        self.login    = builder.get_object('login').get_text()
        self.password = builder.get_object('password').get_text()

        try:
            token, user_id = vk_auth.auth(self.login, self.password, client_id, "messages")
            db.update("token = '%s', user_id = '%s'" % (token, user_id))

            self.auth = True;

            window.close()
        except Exception:
            builder.get_object('error').show()
            builder.get_object('error').set_text("Ошибка авторизации")

    def close(self, button, object = False):
        if self.auth == True:
            window.destroy()
            Gtk.main_quit()
        else:
            sys.exit(1)

class Auth:
    def __init__(self):
        global builder, window

        if api.call_api("execute.auth", [], db.getOne('token')) == True:
            self.token, self.user_id = db.getOne('token'), db.getOne('user_id')
        else:
            self.gui()
            self.token, self.user_id =  db.getOne('token'), db.getOne('user_id')

            if api.call_api("execute.auth", [], self.token) != True:
                self.__init__()

    def gui(self):
        global builder, window

        window = Gtk.Window()

        builder = Gtk.Builder()
        builder.add_from_file("templates/auth.glade")
        builder.connect_signals(Handler())

        window = builder.get_object("window1")
        window.show()

        # window[self.cnt].set_title("Авторизация 1")
        # window[self.cnt].set_border_width(10)
        # window[self.cnt].set_default_size(300, 150)

        Gtk.main()