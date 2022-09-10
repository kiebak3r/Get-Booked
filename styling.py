from classes import *
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

screen_manager = ScreenManager()
Window.size = (300, 600)
screen_manager.add_widget(MainPage(name="main"))


styling = """
ScreenManager:
    MainPage:

<MainPage>
    name: "main"
    elevation: 40
    radius: [36, ]

    FitImage:  # Background
        id: bg_image
        source: "media/bg.png"
        size_hint_y: 1
        radius: 0, 0, 0, 0
        
    MDTextField:
        id: first_name
        hint_text: " Enter your name"
        hint_text_color: 0, 1, 1, 0
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}
        icon_right: "account"
        multiline: False
        size_hint_x: None
        width: 250
    
    MDTextField:
        id: second_name
        hint_text: " Enter your lovers name"
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        icon_right: "cards-heart"
        icon_right_color: "red"
        multiline: False
        size_hint_x: None
        width: 250
    
    MDFloatingActionButtonSpeedDial:
        data: app.data
        icon: "heart-plus"
        root_button_anim: True
        label_text_color: "white"
        callback: app.callback

"""