import os, sys
from kivy.resources import resource_add_path, resource_find
from styling import *
from classes import *
from kivy.lang import Builder
from kivymd.app import MDApp


class GetBooked(

                MDApp, SignIn, SignUp,
                Profile, Chat

                ):

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Gray'
        self.theme_cls.primary_hue = 'A700'
        screen = Builder.load_string(styling)
        return screen


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    GetBooked().run()
