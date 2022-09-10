import requests, string
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen

info = "1. Input fields will only accept characters A-Z as valid input. \n \n" \
       "2. API usage may be limited for high traffic accounts. \n \n" \
       "3. If you encounter an error, Please reference the Error code in your email. \n \n " \
       "4. I take no credibility for being a home wrecker."


class MainPage(Screen):
    data = {
            'Info': 'information-variant',
            'Clear Input': 'close',
            'Show Results': 'hand-heart'
        }

    def reset_input_field(self):
        self.root.get_screen('main').ids.first_name.text = ""
        self.root.get_screen('main').ids.second_name.text = ""

    def callback(self, instance):
        if instance.icon == 'hand-heart':
            self.show_results()

        elif instance.icon == 'close':
            self.reset_input_field()

        elif instance.icon == 'information-variant':
            info_dialog = MDDialog(title=f"Usage Information", text=f"{info}",
                                   buttons=[MDFlatButton(text="Close", on_release=lambda _: info_dialog.dismiss())])
            return info_dialog.open()

    def show_results(self):
        first_user = self.root.get_screen('main').ids.first_name.text
        second_user = self.root.get_screen('main').ids.second_name.text

        if first_user == "":
            self.reset_input_field()
            error_code_1 = MDDialog(title=f"Invalid Name Entered \n Error Code(1)",
                                    text=f"No user input was registered for the first input field,"
                                         f" Please enter a valid input and try again. \n\n"
                                         f"if the error persists, contact <test@test.com>",
                                    buttons=[MDFlatButton(text="Close",
                                                          on_release=lambda _: error_code_1.dismiss())])

            return error_code_1.open()

        elif any(char in string.punctuation for char in first_user):
            self.reset_input_field()
            error_code_2 = MDDialog(title=f"Invalid Name Entered \n Error Code(2)",
                                    text=f"First input field contains special characters, "
                                         f" Please enter a valid input and try again."
                                         f" \n\n if the error persists, contact <test@test.com>",
                                    buttons=[MDFlatButton(text="Close",
                                                          on_release=lambda _: error_code_2.dismiss())])
            return error_code_2.open()

        if second_user == "":
            self.reset_input_field()
            error_code_3 = MDDialog(title=f"Invalid Name Entered \n Error Code(3)",
                                    text=f"No user input was registered for secondary input field, "
                                         f" Please enter a valid input and try again. \n\n"
                                         f"if the error persists, contact <test@test.com>",
                                    buttons=[MDFlatButton(text="Close",
                                                          on_release=lambda _: error_code_3.dismiss())])
            return error_code_3.open()

        elif any(char in string.punctuation for char in second_user):
            self.reset_input_field()
            error_code_4 = MDDialog(title=f"Invalid Name Entered \n Error Code(4)",
                                    text=f"Secondary edit field contains special characters,"
                                         f" Please enter a valid input and try again. \n\n"
                                         f"if the error persists, contact <test@test.com>",
                                    buttons=[MDFlatButton(text="Close",
                                                          on_release=lambda _: error_code_4.dismiss())])
            return error_code_4.open()

        url = "https://love-calculator.p.rapidapi.com/getPercentage"

        querystring = {"sname": f"{first_user}", "fname": f"{second_user}"}

        headers = {

            'x-rapidapi-host': "love-calculator.p.rapidapi.com",
            'x-rapidapi-key': "c5a59d3501msh30b27fbd50eb596p16e483jsn5fb122484d0e"

        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        love_calc = response['percentage']

        show_results = MDDialog(title=f"{first_user} and {second_user}",
                                text=f"Have a {love_calc}% chance of falling in love",
                                buttons=[MDFlatButton(text="Close",
                                                      on_release=lambda _: show_results.dismiss())])

        self.reset_input_field()
        return show_results.open()

