import configparser
import os
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivymd.toast import toast
from kivyauth.google_auth import login_google, logout_google
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.list import TwoLineListItem, OneLineListItem
from kivy.properties import ListProperty, StringProperty
from datetime import datetime
import sqlite3, datetime
import requests, string
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivymd.uix.picker import MDDatePicker
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.animation import Animation
from kivy.metrics import dp
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
database = 'misc/getbooked.db'


class Chat(Screen):
    def callback_for_menu_items(self, *args):
        toast(args[0])

    def show_example_grid_bottom_sheet(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Camera": "camera",
            "Photos": "folder-multiple-image",
        }

        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()

    messages = ListProperty()

    def add_message(self, text, side, color):
        self.messages.append({
            'message_id': len(self.messages),
            'text': text,
            'side': side,
            'bg_color': color,
            'text_size': [None, None],
        })

    def send_message(self, textinput):
        global text
        text = textinput.text
        textinput.text = ''

        try:
            self.add_message(text, 'right', '#848482')
            self.client_socket.send(bytes(text, "utf8"))
            self.focus_textinput(textinput)
            self.scroll_bottom()

        except OSError:
            print("No connection to server")

    def fetch_message(self):
        while True:
            try:
                received = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                if received != text:
                    self.add_message(received, 'left', '#9f00ff')
                    self.scroll_bottom()

            except OSError:
                print("No connection to server")
                break

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

    try:
        HOST = "127.0.0.1"
        PORT = 33000
        BUFSIZ = 1024
        ADDR = (HOST, PORT)
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)

    except ConnectionRefusedError:
        print("couldnt make server connection.")

    def chat_thread(self):
        self.receive_thread = Thread(target=self.fetch_message)
        self.receive_thread.start()

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


class PictureFloatLayout(FloatLayout):
    source = StringProperty()


class Profile(Screen):
    def add_picture_to_database(self):
        # Add pictures path -- can use self.select_path() to save users profile pic to db
        self.insertBLOB(f"{self.select_path(self)}", )

    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def insertBLOB(self, photo):
        try:
            sqliteConnection = sqlite3.connect('misc/getbooked.db')
            cursor = sqliteConnection.cursor()
            sqlite_insert_blob_query = f" UPDATE users SET profile_picture = ? WHERE username = '{username}'"

            empPhoto = self.convertToBinaryData(photo)
            data_tuple = (empPhoto,)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error:
            pass

        finally:
            if sqliteConnection:
                sqliteConnection.close()

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

    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
        self.manager_open = True

    def select_path(self, path):
        self.exit_manager()
        if os.path.isfile(path):
            Clock.schedule_once(lambda x: self.set_pic(path), 1)
        return path

    def set_pic(self, new):
        if os.path.isfile(new):
            self.root.get_screen('profile').ids.profile_pic.source = new

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


class SignIn(Screen):
    def google_login(self):
        login_google()

    def after_login(self):
        pass

    def error_listener(self):
        pass

    def remember_me(self, value, checkbox):
        if checkbox:
            username = self.root.get_screen('sign_in').ids.username.text
            global config
            config = configparser.ConfigParser()
            config.read('misc/settings.ini')
            config.set('PROFILE_SETTINGS', 'remember_me', 'True')
            config.set('PROFILE_SETTINGS', 'last_user', f'{username}')
            pass

        if not checkbox:
            config = configparser.ConfigParser()
            config.read('misc/settings.ini')
            config.set('PROFILE_SETTINGS', 'remember_me', 'False')
            config.set('PROFILE_SETTINGS', 'last_user', '')
            with open('misc/settings.ini', 'w') as configfile:
                config.write(configfile)
                configfile.close()
            pass

    def write_to_settings(self):
        with open('misc/settings.ini', 'w') as configfile:
            config.write(configfile)
            configfile.close()

    def sign_out_settings_fix(self):
        config = configparser.ConfigParser()
        config.read('misc/settings.ini')
        config.set('PROFILE_SETTINGS', 'remember_me', 'False')
        config.set('PROFILE_SETTINGS', 'last_user', '')
        with open('misc/settings.ini', 'w') as configfile:
            config.write(configfile)
            configfile.close()

    def skip_login(self):
        config = configparser.ConfigParser()
        config.read('misc/settings.ini')
        remember_me = config['PROFILE_SETTINGS']['remember_me']
        user = config['PROFILE_SETTINGS']['last_user']
        if remember_me == "True" and not user == "":
            self.root.get_screen('profile').ids.display_name.text = f"{user}'s Profile"
            self.root.current = "profile"
        else:
            pass

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
                    self.write_to_settings()
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


class Schedule(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_prompt = None
        self.event_id = None
        self.date = None
        self.event_title = None
        self.details = None
        self.start = None
        self.end = None
        self.service = None

    def clear_appointments(self):
        self.root.get_screen('schedule').ids.container.clear_widgets()

    def delete_appointment(self):
        self.service.events().delete(calendarId='primary', eventId=self.event_id, sendUpdates='all').execute()
        self.user_prompt.dismiss()
        self.clear_appointments()
        self.check_appointments()

    def check_appointments(self):
        creds = None
        if os.path.exists('misc/token.json'):
            creds = Credentials.from_authorized_user_file('misc/token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'misc/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('misc/token.json', 'w') as token:
                token.write(creds.to_json())
        try:
            self.service = build('calendar', 'v3', credentials=creds)

            now = datetime.datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                       maxResults=10, singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                failed_to_sync_calendar = MDDialog(
                    title=f"No Appointments \n ",
                    text=f"You have no upcoming appointments in your calendar.",
                    buttons=[MDFlatButton(text="Close",
                                          on_release=lambda _: failed_to_sync_calendar.dismiss())])

                return failed_to_sync_calendar.open()

            for event in events:
                try:
                    try:
                        self.event_title = event['summary']
                    except KeyError:
                        pass

                    try:
                        self.event_id = event['id']
                    except KeyError:
                        pass

                    try:
                        self.details = event['description']
                    except KeyError:
                        pass

                    try:
                        self.date = event['start']['dateTime'][0:10]
                    except KeyError:
                        pass

                    try:
                        self.start = event['start']['dateTime'][11:16]
                    except KeyError:
                        pass

                    try:
                        self.end = event['end']['dateTime'][11:16]
                    except KeyError:
                        pass

                    if self.event_title is not None:
                        self.user_prompt = MDDialog(
                            title=f"Actions menu",
                            buttons=[MDFlatButton(text="Close",
                                                  on_release=lambda x: self.user_prompt.dismiss()),
                                     MDFlatButton(text="Delete",
                                                  on_release=lambda x: self.delete_appointment())])

                        self.root.get_screen('schedule').ids.container.add_widget(
                            TwoLineListItem(text=self.event_title,
                                            secondary_text=f"{self.date} at {self.start} - {self.end}",
                                            on_release=lambda x: self.user_prompt.open()
                                            )
                        )

                        self.root.current = "schedule"

                except NameError:
                    pass

        except HttpError:
            pass


class Calendar(Screen):
    pass


class CalendarCard(DragBehavior, MDCard):
    pass
