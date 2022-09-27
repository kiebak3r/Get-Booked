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
                    self.root.get_screen('profile').ids.display_name.text = f"{username}'s Profile"
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
    def add_user_to_database(self):
        username = self.root.get_screen('sign_up').ids.new_username.text
        password = self.root.get_screen('sign_up').ids.new_password.text
        confirm_password = self.root.get_screen('sign_up').ids.new_password_confirm.text

        if len(username) > 14:
            username_error = MDDialog(
                title=f"Invalid Credentials \n Error Code (8)",
                text=f"The username entered exceeds 14 characters, please try again.",
                buttons=[MDFlatButton(text="Close", on_release=lambda _: username_error.dismiss())])

            return username_error.open()

        elif any(char in string.punctuation for char in username):
            spec_char_error = MDDialog(
                title=f"Invalid Credentials \n Error Code (9)",
                text="The username cannot contain special characters, please try again.",
                buttons=[MDFlatButton(text="Close", on_release=lambda _: spec_char_error.dismiss())])

            return spec_char_error.open()

        elif len(username) > 2 and password == confirm_password:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()

            try:
                cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
                conn.commit(), conn.close()

            except sqlite3.IntegrityError:
                self.root.get_screen('sign_up').ids.new_username.text = ""
                duplicate_username_error = MDDialog(
                    title=f"Invalid Username \n Error Code (10)",
                    text=f"The username selected is not available Please select a new username and try again.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda _: duplicate_username_error.dismiss())])

                return duplicate_username_error.open()
