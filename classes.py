import sqlite3
import requests, string
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from plyer import filechooser
from kivy.properties import ListProperty
import shutil
from datetime import datetime
import sqlite3
import requests, string
from kivy.properties import ListProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.app import MDApp


database = 'getbooked.db'


class Chat(Screen):
    messages = ListProperty()

    def add_message(self, text, side, color):
        self.messages.append({
            'message_id': len(self.messages),
            'text': text,
            'side': side,
            'bg_color': color,
            'text_size': [None, None],
        })

    def update_message_size(self, message_id, texture_size, max_width):
        if max_width == 0:
            return

        one_line = dp(50)

        if texture_size[0] >= max_width * 2 / 3:
            self.messages[message_id] = {
                **self.messages[message_id],
                'text_size': (max_width * 2 / 3, None),
            }

        elif texture_size[0] < max_width * 2 / 3 and \
                texture_size[1] > one_line:
            self.messages[message_id] = {
                **self.messages[message_id],
                'text_size': (max_width * 2 / 3, None),
                '_size': texture_size,
            }

        else:
            self.messages[message_id] = {
                **self.messages[message_id],
                '_size': texture_size,
            }

    @staticmethod
    def focus_textinput(textinput):
        textinput.focus = True

    def send_message(self, textinput):
        text = textinput.text
        textinput.text = ''
        self.add_message(text, 'right', '#848482')
        self.focus_textinput(textinput)
        Clock.schedule_once(lambda *args: self.answer(text), 1)
        self.scroll_bottom()

    def answer(self, text, *args):
        self.add_message('Auto response', 'left', '#9955bb')

    def scroll_bottom(self):
        rv = self.root.get_screen('chat').ids.rv
        box = self.root.get_screen('chat').ids.box
        if rv.height < box.height:
            Animation.cancel_all(rv, 'scroll_y')
            Animation(scroll_y=0, t='out_quad', d=.5).start(rv)

    def on_save(self, instance, value, date_range):
        self.root.get_screen('booking').ids.date_button.text = str(value)

    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker(primary_color="gray")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()


class Profile(Screen):
    def delete_account(self):
        global delete
        delete = MDDialog(
                    title=f"Account Deletion",
                    text=f"Are you sure you would like to delete your account?",
                    buttons=[MDFlatButton(text="No", on_release=lambda _: delete.dismiss()),
                             MDFlatButton(text="Yes", on_release=lambda _: self.delete_flow())])

        return delete.open()

    def delete_flow(self):
        delete.dismiss()
        self.root.current = 'sign_in'
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM users WHERE username = "{username}" ')
        conn.commit()

    selection = ListProperty([])

    def choose(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        self.selection = selection

    def on_selection(self, *a, **k):
        profile_pic = str(self.selection).strip("['']")
        shutil.copyfile(str(profile_pic), 'C:\\Users\\ds23s\PycharmProjects\\Get-Booked\\media\\avatar1.png')


class SignIn(Screen):
    def reset_input_field(self):
        self.root.get_screen('sign_in').ids.username.text = ""
        self.root.get_screen('sign_in').ids.password.text = ""

    def user_login_lookup(self):
        global username
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
            conn.close()

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
    def sign_in_screen(self, user_added):
        self.root.current = "sign_in"
        user_added.dismiss()

    def add_user_to_database(self):
        username = self.root.get_screen('sign_up').ids.new_username.text
        password = self.root.get_screen('sign_up').ids.new_password.text
        confirm_password = self.root.get_screen('sign_up').ids.new_password_confirm.text

        if len(username) > 14:
            self.root.get_screen('sign_up').ids.new_username.text = ""
            username_error = MDDialog(
                title=f"Invalid Credentials \n Error Code (8)",
                text=f"The username entered exceeds 14 characters, please try again.",
                buttons=[MDFlatButton(text="Close", on_release=lambda _: username_error.dismiss())])

            return username_error.open()

        elif any(char in string.punctuation for char in username) or " " in username:
            self.root.get_screen('sign_up').ids.new_username.text = ""
            spec_char_error = MDDialog(
                title=f"Invalid Credentials \n Error Code (9)",
                text="The username cannot contain special characters, please try again.",
                buttons=[MDFlatButton(text="Close", on_release=lambda _: spec_char_error.dismiss())])

            return spec_char_error.open()

        elif len(username) > 2:
            if len(password) > 10:
                self.root.get_screen('sign_up').ids.new_password.text = ""
                self.root.get_screen('sign_up').ids.new_password_confirm.text = ""

                password_error = MDDialog(
                    title=f"Invalid Credentials \n Error Code (11)",
                    text=f"Password cannot be greater than 10 characters, please try again.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda _: password_error.dismiss())])

                return password_error.open()

            elif any(char in string.punctuation for char in password):
                self.root.get_screen('sign_up').ids.new_password.text = ""
                self.root.get_screen('sign_up').ids.new_password_confirm.text = ""

                spec_char_error = MDDialog(
                    title=f"Invalid Credentials \n Error Code (12)",
                    text="Password cannot contain special characters, please try again.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda _: spec_char_error.dismiss())])

                return spec_char_error.open()

            elif len(password) < 5:
                self.root.get_screen('sign_up').ids.new_password.text = ""
                self.root.get_screen('sign_up').ids.new_password_confirm.text = ""

                min_length_error = MDDialog(
                    title=f"Invalid Credentials \n Error Code (13)",
                    text="Password cannot be less than 5 character and cannot be more than 10, please try again.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda _: min_length_error.dismiss())])

                return min_length_error.open()

            elif password != confirm_password:
                self.root.get_screen('sign_up').ids.new_password.text = ""
                self.root.get_screen('sign_up').ids.new_password_confirm.text = ""

                passwords_dont_match = MDDialog(
                    title=f"Invalid Credentials \n Error Code (14)",
                    text="The password and the confirmation password do not match, please try again.",
                    buttons=[MDFlatButton(text="Close", on_release=lambda _: passwords_dont_match.dismiss())])

                return passwords_dont_match.open()

            else:
                conn = sqlite3.connect(database)
                cursor = conn.cursor()

                try:
                    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
                    conn.commit(), conn.close()

                    user_added = MDDialog(
                        title=f"Account Created \n ",
                        text=f"Your account has been created, You can now sign in.",
                        buttons=[MDFlatButton(text="Sign In",
                                              on_release=lambda _: self.sign_in_screen(user_added))])

                    return user_added.open()

                except sqlite3.IntegrityError:
                    self.root.get_screen('sign_up').ids.new_username.text = ""
                    self.root.get_screen('sign_up').ids.new_password.text = ""
                    self.root.get_screen('sign_up').ids.new_password_confirm.text = ""

                    duplicate_username_error = MDDialog(
                        title=f"Invalid Username \n Error Code (10)",
                        text=f"The username selected is not available Please select a new username and try again.",
                        buttons=[MDFlatButton(text="Close", on_release=lambda _: duplicate_username_error.dismiss())])

                    return duplicate_username_error.open()
