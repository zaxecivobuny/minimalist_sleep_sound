from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
import datetime
import time


class SoundApp(GridLayout):
    def __init__(self, **kwargs):
        super(SoundApp, self).__init__(**kwargs)
        self.cols = 2
        self.padding = 10

        # Button to play the sound
        self.play_button = Button(text='Play', font_size=30, size_hint=(0.5, 0.2))
        self.play_button.bind(on_press=self.play_sound)
        self.add_widget(self.play_button)

        # Button to stop the sound
        self.stop_button = Button(text='Stop', font_size=30, size_hint=(0.5, 0.2))
        self.stop_button.bind(on_press=self.stop_sound)
        self.add_widget(self.stop_button)

        # Dropdown for selecting hours
        self.hours_dropdown = DropDown()
        for hour in range(1, 13):
            btn = Button(text=str(hour), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.hours_dropdown.select(btn.text))
            self.hours_dropdown.add_widget(btn)
        self.hours_button = Button(text='Hours', size_hint=(0.5, 0.2))
        self.hours_button.bind(on_release=self.hours_dropdown.open)
        self.hours_dropdown.bind(on_select=lambda instance, x: setattr(self.hours_button, 'text', x))
        self.add_widget(self.hours_button)

        # Dropdown for selecting minutes
        self.minutes_dropdown = DropDown()
        for minute in range(0, 60):
            btn = Button(text=str(minute), size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.minutes_dropdown.select(btn.text))
            self.minutes_dropdown.add_widget(btn)
        self.minutes_button = Button(text='Minutes', size_hint=(0.5, 0.2))
        self.minutes_button.bind(on_release=self.minutes_dropdown.open)
        self.minutes_dropdown.bind(on_select=lambda instance, x: setattr(self.minutes_button, 'text', x))
        self.add_widget(self.minutes_button)

        # Button to set the stop time
        self.set_time_button = Button(text='Set Time', font_size=30, size_hint=(0.5, 0.2))
        self.set_time_button.bind(on_press=self.set_stop_time)
        self.add_widget(self.set_time_button)

        # Button to snooze for 10 minutes
        self.snooze10_button = Button(text='Snooze +10', font_size=30, size_hint=(0.5, 0.2))
        self.snooze10_button.bind(on_press=self.snooze_10)
        self.add_widget(self.snooze10_button)

        # Button to snooze for 15 minutes
        self.snooze15_button = Button(text='Snooze +15', font_size=30, size_hint=(0.5, 0.2))
        self.snooze15_button.bind(on_press=self.snooze_15)
        self.add_widget(self.snooze15_button)

        # Label to display the stop time
        self.stop_time_label = Label(text='', font_size=20, size_hint=(0.5, 0.2))
        self.add_widget(self.stop_time_label)

        # Initialize stop time to None
        self.stop_time = None
        
        # Initialize sound file
        self.sound_file = SoundLoader.load('brown_noise.wav')
        
    def play_sound(self, instance):
        # Play sound file
        self.sound_file.play()
        
    def stop_sound(self, instance):
        # Stop sound file
        self.sound_file.stop()
        
    def set_stop_time(self, instance):
        # Get current time
        now = datetime.datetime.now()
        
        # Get selected hours and minutes from dropdowns
        hours = int(self.hours_button.text)
        minutes = int(self.minutes_button.text)
        
        # Set stop time to the next occurrence of selected time
        if now.hour > hours or (now.hour == hours and now.minute >= minutes):
            self.stop_time = datetime.datetime(now.year, now.month, now.day+1, hours, minutes)
        else:
            self.stop_time = datetime.datetime(now.year, now.month, now.day, hours, minutes)
        
        # Update stop time label
        self.stop_time_label.text = 'Sound will stop at: ' + self.stop_time.strftime('%I:%M %p')
        
    def snooze_10(self, instance):
        # Play sound for 10 minutes
        self.sound_file.play()
        time.sleep(600)
        self.sound_file.stop()
        
    def snooze_15(self, instance):
        # Play sound for 15 minutes
        self.sound_file.play()
        time.sleep(900)
        self.sound_file.stop()


class SoundAppMain(App):
    def build(self):
        return SoundApp()


if __name__ == '__main__':
    SoundAppMain().run()
