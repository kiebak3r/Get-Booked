from classes import *
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

default_avatar = f'{os.environ["USERPROFILE"]}\\PycharmProjects\\Get-Booked\\media\\avatar1.png'

screen_manager = ScreenManager()
Window.size = (300, 600)
screen_manager.add_widget(Profile(name="profile"))
screen_manager.add_widget(SignIn(name="sign_in"))
screen_manager.add_widget(SignUp(name="sign_up"))
screen_manager.add_widget(Chat(name="chat"))
screen_manager.add_widget(Chat(name="schedule"))
screen_manager.add_widget(Chat(name="calendar"))

styling = """
#:import RGBA kivy.utils.rgba
#:import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    transition: NoTransition()
    SignIn:
    SignUp:
    Profile:
    Chat:
    Schedule:
    Calendar:

<Calendar>
    name: "calendar"
    
    MDBoxLayout:    
        orientation: "vertical"

        MDBottomNavigation:
            text_color_normal: 1, 1, 1, 1

            MDBottomNavigationItem:
                name: "back"
                text: "Go back"
                icon: "arrow-left-thick"
                on_tab_release: root.manager.current = "profile"

            MDBottomNavigationItem:
                name: "add"
                text: "Add"
                icon: "plus-circle"
                on_tab_release: root.manager.current = ""
                
    FloatLayout:
        CalendarCard:
            size_hint: 0.15, 0.3
            text: 'Drag me'
    
<CalendarCard>:
    drag_rectangle: self.x, self.y, self.width, self.height
    radius: dp(20)
    # elevation: 0
    drag_timeout: 10000000
    drag_distance: 0
    
            
<Schedule>
    name: "schedule"
            
    MDBoxLayout:    
        orientation: "vertical"

        MDBottomNavigation:
            text_color_normal: 1, 1, 1, 1

            MDBottomNavigationItem:
                name: "back"
                text: "back"
                icon: "arrow-left-circle"
                on_tab_press: app.clear_appointments()
                on_tab_release: root.manager.current = "profile"

            MDBottomNavigationItem:
                name: "refresh"
                text: "refresh"
                icon: "refresh-circle"
                on_tab_press: app.clear_appointments()
                on_tab_release: app.check_appointments()
    
    MDLabel:
        text: "Upcoming Appointments"
        pos_hint: {"center_y": 0.92, "center_x": 0.5}
        font_style: "H6"
        halign: "center"
        valign: "center"
        
    ScrollView:
        size_hint_y: .8
        size_hint_x: 1
        pos_hint: {"center_y": 0.5, "center_x": 0.5}
            
        MDList:
            id: container

<SignIn>
    name: "sign_in"
                    
    MDFloatLayout:
        id: logo
        pos_hint: {"center_x": .5, "center_y": .67}      
        canvas:
            Color:
                rgb: 1, 1, 1          
            Ellipse:
                source: "media/logo.png"
                pos: [self.center_x - 305/3, self.center_y - 100/3]
                size: 200, 200
                angle_start: 0
                angle_end: 360

    MDTextField:
        id: username
        hint_text: "Username"
        icon_right: "account"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        size_hint_x: .8
        max_text_length: 14
        multiline: False

    MDTextField:
        id: password
        password: True
        hint_text: "Password"
        icon_right: "lock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        size_hint_x: .8
        max_text_length: 10
        multiline: False
        
    MDFloatLayout:    
        MDLabel:
            text: "Remember me"
            halign: "center"
            pos_hint: {'center_x': .29, 'center_y': .37} 
            font_style: "Overline"
                
        MDCheckbox:
            id: remember_me
            size: "48dp", "48dp"
            size_hint: None,None
            hint_text: "Remember me"
            on_active: app.remember_me(*args)
            pos_hint: {'center_x': .13, 'center_y': .37}  

    Button:
        text: "Sign In"
        size_hint: .43, .055
        pos_hint: {'center_x': .67, 'center_y': .37}
        background_color: 0, 0, 0, 0
        on_release: app.user_login_lookup()
        canvas.before:
            Color:
                rgb: rgba(36, 35, 36, 0.8)
                
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [5]
    
    MDLabel:
        text: "OR"
        color: rgba(0, 0, 0, 255)
        pos_hint: {"center_y": .25}
        font_size: "13sp"
        halign: "center"
    
    MDFloatLayout:
        md_bg_color: rgba(0, 0, 0, 255)
        size_hint: .32, .002
        pos_hint: {"center_x": .3, "center_y": .25}
    
    MDFloatLayout:
        md_bg_color: rgba(0, 0, 0, 255)
        size_hint: .32, .002
        pos_hint: {"center_x": .7, "center_y": .25}
    
    Button:
        text: "Sign In With Google"
        size_hint: .66, .065
        pos_hint: {'center_x': 0.5, 'center_y': 0.17}
        background_color: 0, 0, 0, 0
        on_release: app.google_login()
        canvas.before:
            Color:
                rgb: rgba(36, 35, 36, 0.8)
                
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [5]
                    
    MDTextButton:
        text: "Create an account"
        font_style: "Subtitle2"
        pos_hint: {'center_x': 0.5, 'center_y': 0.12}
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
    
    Button:
        text: "Create Account"
        size_hint: .66, .065
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
        background_color: 0, 0, 0, 0
        on_release: app.add_user_to_database()
        canvas.before:
            Color:
                rgb: rgba(36, 35, 36, 0.8)
                
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [5]
                
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
                name: "schedule"
                text: "Schedule"
                icon: "clock-outline"
                on_tab_release: app.check_appointments()

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
        on_release: root.manager.current = "calendar"

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
        on_release: app.sign_out_settings_fix()

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
                multiline: True
                on_text_validate:
                    app.send_message(self)

            MDIconButton:
                icon: "folder-multiple-image"
                icon_size: "64sp"
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                on_release: app.show_example_grid_bottom_sheet()

            MDIconButton:
                icon: "send-circle"
                icon_size: "64sp"
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
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