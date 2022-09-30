from classes import *
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

default_avatar = 'C:\\Users\\kieran.baker\\PycharmProjects\\Get-Booked\\media\\avatar1.png'

screen_manager = ScreenManager()
Window.size = (300, 600)
screen_manager.add_widget(Profile(name="profile"))
screen_manager.add_widget(SignIn(name="sign_in"))
screen_manager.add_widget(SignUp(name="sign_up"))
screen_manager.add_widget(Chat(name="chat"))

styling = """
#:import RGBA kivy.utils.rgba
#:import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    transition: NoTransition()
    SignIn:
    SignUp:
    Profile:
    Chat:

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
    
    MDCheckbox:
        id: remember_me
        group: 'group'
        size_hint: None,None
        size: "48dp", "48dp"
        pos_hint: {'center_x': .2, 'center_y': .22}
        on_active: app.remember_me(*args)

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
                on_tab_release: root.manager.current = "chat"

    PictureFloatLayout:
        id: profile_pic
        pos_hint: {"center_x": .5, "center_y": .63}      
        canvas:
            Color:
                rgb: 1, 1, 1          
            Ellipse:
                source: self.source
                pos: [self.center_x - 305/3, self.center_y - 100/3]
                size: 200, 200
                angle_start: 0
                angle_end: 360
                
    MDIconButton:
        icon: "pencil-circle"
        icon_size: "64sp"
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        on_press: app.file_manager_open()

    MDLabel: 
        id: display_name
        text: ""
        text_size: 
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
        radius: dp(100)


<ImageButton@ButtonBehavior+Image>:
    size_hint: None, None
    size: self.texture_size
    canvas.before:
        PushMatrix
        Scale:
            origin: self.center
            x: 1 if self.state == 'down' else 1
            y: 1 if self.state == 'down' else 1
    canvas.after:
        PopMatrix

<Chat>
    name: "chat"

    BoxLayout:
        orientation: 'vertical'
        padding: dp(5), dp(5)

        RecycleView:
            id: rv
            data: app.messages
            viewclass: 'Message'
            do_scroll_x: False

            RecycleBoxLayout:
                id: box
                orientation: 'vertical'
                size_hint_y: None
                size: self.minimum_size
                default_size_hint: .95, None
                # magic value for the default height of the message
                default_size: 0, 39
                key_size: '_size'

        BoxLayout:
            size_hint: 1, None
            size: self.minimum_size

            MDTextField:
                hint_text: "Type a new message"
                mode: "fill"
                id: ti
                size_hint: 1, None
                height: min(max(self.line_height, self.minimum_height), 150)
                # pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                multiline: False
                on_text_validate:
                    app.send_message(self)

            MDIconButton:
                icon: "folder-multiple-image"
                icon_size: "64sp"
                pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                # on_release:  

            MDIconButton:
                icon: "send-circle"
                icon_size: "64sp"
                pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                on_release: app.send_message(ti)  

    MDIconButton:
        icon: "arrow-left"
        icon_size: "64sp"
        pos_hint: {'center_x': 0.0999, 'center_y': 0.95}
        on_release: root.manager.current = "profile" 

<Message@FloatLayout>:
    message_id: -1
    bg_color: '#223344'
    side: 'left'
    text: ''
    size_hint_y: None
    _size: 0, 0
    size: self._size
    text_size: None, None
    opacity: min(1, self._size[0])
    Label:
        text: root.text
        padding: 15, 15
        size_hint: None, 1
        size: self.texture_size
        text_size: root.text_size
        on_texture_size:
            app.update_message_size(
            root.message_id,
            self.texture_size,
            root.width,
            )
        pos_hint:
            (
            {'x': 0, 'center_y': .5}
            if root.side == 'left' else
            {'right': 1, 'center_y': .5}
            )
        canvas.before:
            Color:
                rgba: RGBA(root.bg_color)
            RoundedRectangle:
                size: self.texture_size
                radius: dp(5), dp(5), dp(5), dp(5)
                pos: self.pos
        canvas.after:
            Color:
            Line:
                rounded_rectangle: self.pos + self.texture_size + [dp(5)]
                width: 1.01

"""