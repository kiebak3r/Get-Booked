import sqlite3
import requests, string
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen

database = 'getbooked.db'


class Profile(Screen):
    pass


class SignIn(Screen):
    def reset_input_field(self):
        self.root.get_screen('sign_in').ids.username.text = ""
        self.root.get_screen('sign_in').ids.password.text = ""

    def user_login_lookup(self):
        username = self.root.get_screen('sign_in').ids.username.text

        if len(username) > 14:
            self.reset_input_field()
            password_error = MDDialog(
                title=f"Invalid Credentials \n Error Code (1)",
                text=f"The username entered exceeds 14 characters, please try again.",
                buttons=[MDFlatButton(text="Close", on_release=lambda _: password_error.dismiss())])

            return password_error.open()

        elif any(char in string.punctuation for char in username):
            self.reset_input_field()
            spec_char_error = MDDialog(
                title=f"Invalid Credentials \n Error Code (2)",
                text="The username cannot contain special characters, please try again.",
                buttons=[MDFlatButton(text="Close", on_release=lambda _: spec_char_error.dismiss())])

            return spec_char_error.open()

        elif len(username) > 2:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            query = cursor.execute(f'SELECT password FROM users WHERE username = "{username}" ').fetchone()

            try:
                if self.root.get_screen('sign_in').ids.password.text == query[0]:
                    self.reset_input_field()
                    self.root.current = "profile"

                else:
                    self.reset_input_field()
                    password_error = MDDialog(
                                title=f"Invalid Credentials \n Error Code (3)",
                                text=f"the username or password entered was not recognised, please try again.",
                                buttons=[MDFlatButton(text="Close", on_release=lambda _: password_error.dismiss())])

                    return password_error.open()

            except TypeError:
                self.reset_input_field()
                database_error = MDDialog(
                    title=f"Invalid Username \n Error Code (5)",
                    text=f"The username or password was not recognised, please try again.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda _: database_error.dismiss())])

                return database_error.open()

        else:
            self.reset_input_field()
            username_error = MDDialog(
                title=f"Invalid Username \n Error Code (4)",
                text=f"The username must be between 3-14 characters, please try again.",
                buttons=[MDFlatButton(text="Close", on_release=lambda _: username_error.dismiss())])

            return username_error.open()


class SignUp(Screen):
    pass