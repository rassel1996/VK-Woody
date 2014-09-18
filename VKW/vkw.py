#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Application
import api, auth, vk_auth, db

# System
import os
import sys
import json
import shlex
import sqlite3
import subprocess

# GTK+
from gi.repository import Gtk, Gdk, GObject, AppIndicator3 as appindicator


PING_FREQUENCY = 1 # seconds
APP_DIR        = os.path.dirname(os.path.realpath(__file__)) + "/" # Application path

class CheckVK:
    # Инициализация
    def __init__(self):
        self.client_id = "4508898"
        self.CNT       = False

        # Проверка авторизации и авторизация пользователя
        auth.Auth()

        self.token, self.user_id = db.getOne('token'), db.getOne('user_id')

        self.applet()
        self.check()
        GObject.timeout_add(PING_FREQUENCY * 1000, self.check)
        Gtk.main()  

    # Инициализация апплета (показ иконки апплета и меню)
    def applet(self):
        self.a = appindicator.Indicator.new("vk-icon", "%sicons/vk-icon.x64.png" % (APP_DIR), appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.a.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.a.set_attention_icon("%sicons/vk-icon-active.png" % (APP_DIR))
        self.menu()

    def quit_item(self):
        self.qi = Gtk.MenuItem( 'Выход' )
        self.m.append(self.qi)
        self.qi.connect('activate', Gtk.main_quit)
        self.qi.show()

    def messages_item(self, unread = False, refresh = False):
        unread      = unread if unread != False else self.unread()
        button_text = 'Диалоги (%s)' % (unread) if unread > 0 else 'Диалоги'

        if refresh == True:
            self.message_button.set_label('Диалоги (%s)' % (unread) if unread > 0 else 'Диалоги')
        else:
            if self.CNT == False:
                self.CNT = unread

            self.message_button = Gtk.MenuItem( button_text )
            self.m.append(self.message_button)
            self.message_button.connect('activate', self.dialog_window)   
            self.message_button.show()

    def dialog_window(self, widget):
        window = Gtk.Window()

        builder = Gtk.Builder()
        builder.add_from_file("templates/im.glade")

        window = builder.get_object("im")

        screen = Gdk.Screen.get_default()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('common.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider,
                                        Gtk.STYLE_PROVIDER_PRIORITY_USER)

        window.show()



    def menu(self):
        self.m  = Gtk.Menu()
        self.messages_item()
        self.quit_item()
        self.a.set_menu(self.m)

    # Проверка непрочитанных сообщений
    def check(self):
        unread = self.unread()

        if type(unread) is int:
            if unread < self.CNT:
                self.CNT = unread
                self.messages_item(unread, True)

            if unread > 0:
                #print self.CNT
                #print unread
                #print "--------------------------------------------------------------------------------"

                if unread > self.CNT:
                    args = shlex.split('notify-send "Новое сообщение" -i "%sicons/vk-icon.png"' % (APP_DIR))
                    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    self.CNT = unread
                    self.messages_item(unread, True)
                            
                self.a.set_status(appindicator.IndicatorStatus.ATTENTION)
            else:
                self.a.set_status(appindicator.IndicatorStatus.ACTIVE)



        # Мешает работе кнопок
        #self.menu()
        return True

    # Получение кол-ва непрочитанных сообщений
    def unread(self):
        return api.call_api("execute.unread", [("v", "5.24")], self.token)

if __name__ == "__main__":
    indicator = CheckVK()
