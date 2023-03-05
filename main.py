import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView

from lxml import etree
from bs4 import BeautifulSoup
from ebooklib import epub


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add a file chooser and a button to the home screen
        layout = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserIconView(path='F:/Projects', size_hint=(1, 0.9))
        self.button = Button(text='Go to Second Screen', on_press=self.go_to_second_screen)
        layout.add_widget(self.file_chooser)
        layout.add_widget(self.button)

        self.add_widget(layout)
        

        

    def go_to_second_screen(self, instance):
        # When the button is pressed, switch to the Second screen and pass the path of the selected file
        selected_file_path = self.file_chooser.selection[0]
        self.manager.get_screen('second').update_label(selected_file_path)
        self.manager.current = 'second'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        # Add a label to the second screen that will show the path of the selected file
        self.label = Label(text='')
        self.button = Button(text='Go to Home Screen', on_press=self.go_to_home_screen)
        self.button2 = Button(text='Get Sections', on_press=self.getSections)
        layout.add_widget(self.button)
        layout.add_widget(self.button2)
        layout.add_widget(self.label)
        self.add_widget(layout)
        
    def getSections(self, instance):
        if(self.label.text.endswith('.epub')):
            book = epub.read_epub(self.label.text)
            ncx = None
            for item in book.get_items():
                if 'ncx' in item.file_name:
                    ncx = item
                    break


            if ncx:
                # parse the NCX file
                ncx_root = etree.fromstring(ncx.get_content())
                sections = ncx_root.findall('.//{*}navPoint')
                print("TOC found in the epub file. The sections are:")
                content = ''
                for section in sections:
                    if(section.find('.//{*}text').text == 'Epilogue'):
                        epilogue = book.get_item_with_href(section.find('.//{*}content').get('src'))
                        content = BeautifulSoup(epilogue.get_content(), 'html.parser')
                
                
                #Currently this is just printing the text of the epilogue. I want to be able to pass this to the third screen so that it can be read out loud.
                #Also the text is not being formatted correctly. I want to be able to format it so that it is easier to read.
                #The text must be passed line by line so it is easier to read by Tacotron
                self.manager.get_screen('third').update_tts(content)
                self.manager.current = 'third'
            else:
                print("No TOC found in the epub file.")
        else:
            print("Not an epub file.")

    def update_label(self, selected_file_path):
        # Update the label with the path of the selected file from the Home screen
        self.label.text = selected_file_path
    
    def go_to_home_screen(self, instance):
        # When the button is pressed, switch to the Home screen
        self.manager.current = 'home'



class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        self.tts = Label(text = '')
        self.button = Button(text='Go Back', on_press=self.go_to_home_screen)
        layout.add_widget(self.tts)
        layout.add_widget(self.button)
        self.add_widget(layout)
        

    def go_to_home_screen(self, instance):
        # When the button is pressed, switch to the Home screen
        self.manager.current = 'home'

    def update_tts(self, section):
        # Update the label with the path of the selected file from the Home screen
        self.tts.text = section

class ScreenManagement(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        # Create the screen manager and add the Home and Second screens to it
        screen_manager = ScreenManagement()
        screen_manager.add_widget(HomeScreen(name='home'))
        screen_manager.add_widget(SecondScreen(name='second'))
        screen_manager.add_widget(ThirdScreen(name='third'))

        return screen_manager


if __name__ == '__main__':
    MyApp().run()
