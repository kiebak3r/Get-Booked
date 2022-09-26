from classes import *
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

screen_manager = ScreenManager()
Window.size = (300, 600)
screen_manager.add_widget(MainPage(name="main"))


styling = """
#:import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    transition: NoTransition()
    MainPage:

<MainPage>
    name: "main"
    elevation: 40
    radius: [36, ]
            
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
            image: "media/person2.jpg"
                                         
    MDLabel: 
        text: "Alex Wickham"
        font_style: "H5"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        halign: "center"
        valign: "center"
    
    MDRectangleFlatIconButton:
        text: "My Calendar"
        icon: "calendar"
        pos_hint: {'center_x': 0.5, 'center_y': 0.35}
        halign: "center"
        valign: "center"
        size_hint_x: .8
        theme_text_color: "Custom"
        text_color: "black"
        line_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"
    
    MDRectangleFlatIconButton:
        text: "My Messages"
        icon: "message"
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        size_hint_x: .8
        theme_text_color: "Custom"
        text_color: "black"
        line_color: "black"
        theme_icon_color: "Custom"
        icon_color: "black"


<ElementCard@MDCard>
    image: ''
    size_hint: None, None
    elevation: 10
    radius: dp(25)
    size_hint_y: .35
    size_hint_x: .7
    pos_hint: {"center_x": .5, "center_y": .71}
              
    orientation: 'vertical'
    Image:
        radius: dp(25)
        source: root.image
        halign: "center"
        
"""