from classes import *
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

screen_manager = ScreenManager()
Window.size = (300, 600)
screen_manager.add_widget(Profile(name="profile"))
screen_manager.add_widget(SignIn(name="sign_in"))
screen_manager.add_widget(SignUp(name="sign_up"))


styling = """
#:import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    transition: NoTransition()
    SignIn:
    SignUp:
    Profile:

<SignIn>
    name: "sign_in"
    
    MDFloatLayout:
        ElementCard:
            image: "media/logo.png"
                                         
    MDLabel: 
        text: "catchy slogan here.."
        font_style: "H5"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        halign: "center"
        valign: "center"
    
    MDTextField:
        id: username
        hint_text: "Username"
        icon_right: "account"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        size_hint_x: .8
        max_text_length: 14
        multiline: False
        
    MDTextField:
        id: password
        password: True
        hint_text: "Password"
        icon_right: "lock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint_x: .8
        max_text_length: 10
        multiline: False
    
    MDRectangleFlatIconButton:
        text: "Sign In"
        icon: "arrow-right-bold"
        pos_hint: {'center_x': 0.5, 'center_y': 0.22}
        theme_text_color: "Custom"
        text_color: "black"
        line_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"
        on_release: app.user_login_lookup()
    
    MDTextButton:
        text: "Create an account"
        font_style: "Subtitle2"
        pos_hint: {'center_x': 0.5, 'center_y': 0.15}
        on_press: root.manager.current = "sign_up"
    
<SignUp>
    name: "sign_up"
                      
    MDBoxLayout:    
        orientation: "vertical"

        MDBottomNavigation:
            text_color_normal: 1, 1, 1, 1

            MDBottomNavigationItem:
                name: "back"
                text: "Go back"
                icon: "arrow-left-thick"
                on_tab_release: root.manager.current = "sign_in"

            MDBottomNavigationItem:
                name: "help"
                text: "Help"
                icon: "comment-question"
                on_tab_release: root.manager.current = ""
                                       
    MDLabel: 
        text: "Create an account"
        font_style: "H5"
        pos_hint: {'center_x': 0.5, 'center_y': 0.8}
        halign: "center"
        valign: "center"
            
    MDTextField:
        id: new_username
        hint_text: "Choose a username"
        icon_right: "account"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint_x: .8
        max_text_length: 14
        multiline: False
        
    MDTextField:
        id: new_password
        password: True
        hint_text: "Choose a password"
        icon_right: "lock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: .8
        max_text_length: 10
        multiline: False
    
    MDTextField:
        id: new_password_confirm
        password: True
        hint_text: "Confirm your password"
        icon_right: "alert-circle-check"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        size_hint_x: .8
        max_text_length: 10
        multiline: False
    
    MDRectangleFlatIconButton:
        text: "Create Account"
        icon: "plus-thick"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        theme_text_color: "Custom"
        text_color: "black"
        line_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"
        on_release: app.add_user_to_database()
    
        
<Profile>
    name: "profile"
            
    MDBoxLayout:    
        orientation: "vertical"

        MDBottomNavigation:
            text_color_normal: 1, 1, 1, 1

            MDBottomNavigationItem:
                name: "home"
                text: "Home"
                icon: "home-circle"
                on_tab_release: root.manager.current = ""

            MDBottomNavigationItem:
                name: "calendar"
                text: "Calendar"
                icon: "calendar-month"
                on_tab_release: root.manager.current = ""

            MDBottomNavigationItem:
                name: "messages"
                text: "Messages"
                icon: "message"
                on_tab_release: root.manager.current = ""

    MDFloatLayout:
        ElementCard:
            image: "media/avatar1.png"

    MDLabel: 
        id: display_name
        text: "placeholder"
        font_style: "H5"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        halign: "center"
        valign: "center"

    MDRectangleFlatIconButton:
        text: " My Calendar"
        icon: "calendar"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        halign: "center"
        valign: "center"
        size_hint_x: None
        theme_text_color: "Custom"
        text_color: "black"
        line_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"

    MDRectangleFlatIconButton:
        text: " My Messages"
        icon: "message-processing-outline"
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        size_hint_x: None
        theme_text_color: "Custom"
        text_color: "black"
        line_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"
    
    MDRectangleFlatIconButton:
        text: " Sign Out"
        icon: "exit-to-app"
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        size_hint_x: None
        theme_text_color: "Custom"
        text_color: "black"
        line_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"
        on_release: root.manager.current = "sign_in"
    
    MDTextButton:
        text: "Delete account"
        font_style: "Subtitle2"
        pos_hint: {'center_x': 0.5, 'center_y': 0.15}
        on_press: app.delete_account()


<ElementCard@MDCard>
    image: ''
    size_hint: None, None
    elevation: 0
    radius: dp(100)
    padding: dp(5)
    size_hint_y: .35
    size_hint_x: .7
    pos_hint: {"center_x": .5, "center_y": .71}

    orientation: 'vertical'
    Image:
        source: root.image
        halign: "center"
        
"""