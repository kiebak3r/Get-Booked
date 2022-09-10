from styling import *
from classes import *
from kivy.lang import Builder
from kivymd.app import MDApp


class LoveCalculator(MDApp, MainPage):

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.primary_hue = 'A700'
        screen = Builder.load_string(styling)
        return screen


LoveCalculator().run()
