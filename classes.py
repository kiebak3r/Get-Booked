import requests, string
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen


class Profile(Screen):
    def reset_input_field(self):
        self.root.get_screen('main').ids.first_name.text = ""
        self.root.get_screen('main').ids.second_name.text = ""


class SignIn(Screen):
    pass


class SignUp(Screen):
    pass