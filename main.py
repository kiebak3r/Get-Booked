import os, sys
from kivy.resources import resource_add_path, resource_find
from styling import *
from classes import *
from kivy.lang import Builder
from kivymd.app import MDApp


class GetBooked(

                MDApp, SignIn, SignUp,
                Profile, Chat, Schedule

                ):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Gray'
        self.theme_cls.primary_hue = 'A700'
        Clock.schedule_once(lambda x: self.file_manager, 3)
        screen = Builder.load_string(styling)
        return screen

    def on_start(self):
        self.root.get_screen('profile').ids.profile_pic.source = default_avatar
        self.chat_thread()


if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    GetBooked().run()
