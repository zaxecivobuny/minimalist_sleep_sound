import time
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner


class SoundApp(App):
    def build(self):
        self.layout = GridLayout(cols=2)

        self.layout.add_widget(Label(text='Hours:'))
        self.hours_dropdown = DropDown()
        for i in range(1, 13):
            self.hours_dropdown.add_widget(
                Button(text=str(i), size_hint_y=None, height=30))
        self.hours_spinner = Spinner(
            text='1',
            values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')) # noQA
        self.hours_spinner.bind(on_release=self.hours_dropdown.open)
        self.hours_dropdown.bind(on_select=lambda instance, x: setattr(self.hours_spinner, 'text', x))
        self.layout.add_widget(self.hours_spinner)

        self.layout.add_widget(Label(text='Minutes:'))
        self.minutes_dropdown = DropDown()
        for i in range(0, 60, 5):
            self.minutes_dropdown.add_widget(Button(text=str(i), size_hint_y=None, height=30))
        self.minutes_spinner = Spinner(text='0', values=('0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'))
        self.minutes_spinner.bind(on_release=self.minutes_dropdown.open)
        self.minutes_dropdown.bind(on_select=lambda instance, x: setattr(self.minutes_spinner, 'text', x))
        self.layout.add_widget(self.minutes_spinner)

        self.layout.add_widget(Label(text='AM/PM:'))
        self.am_pm_spinner = Spinner(text='AM', values=('AM', 'PM'))
        self.layout.add_widget(self.am_pm_spinner)

        self.layout.add_widget(Label(text='End Time:'))
        self.end_time = TextInput(text='', multiline=False)
        self.layout.add_widget(self.end_time)

        self.layout.add_widget(Label(text=''))
        self.play_button = Button(text='Play sound', on_press=self.play_sound)
        self.layout.add_widget(self.play_button)

        self.layout.add_widget(Label(text=''))
        self.stop_button = Button(text='Stop sound', on_press=self.stop_sound, disabled=True)
        self.layout.add_widget(self.stop_button)

        self.layout.add_widget(Label(text=''))
        self.snooze_10_button = Button(text='Snooze +10', on_press=self.snooze_10)
        self.layout.add_widget(self.snooze_10_button)

        self.layout.add_widget(Label(text=''))
        self.snooze_15_button = Button(text='Snooze +15', on_press=self.snooze_15)
        self.layout.add_widget(self.snooze_15_button)

        return self.layout

    def play_sound(self, instance):
        # Convert user input to seconds
        hours = int(self.hours_spinner.text) % 12
        minutes = int(self.minutes_spinner.text)
        am_pm = self.am_pm_spinner.text
        if am_pm == 'PM':
            hours += 12
        current_time = datetime.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)

        if current_time < datetime.now():
            current_time += timedelta(days=1)

        # Set end time if provided
        if self.end_time.text:
            end_time = datetime.strptime(self.end_time.text, '%H:%M')
            time_delta = end_time - datetime.now()
            total_time = time_delta.seconds

        self.stop_button.disabled = False
        self.play_button.disabled = True

        # Play sound for specified time
        for i in range(total_time):
            # Check if snooze button has been pressed
            if hasattr(self, 'snooze') and self.snooze:
                snooze_time = self.snooze - datetime.now()
                if snooze_time.seconds > 0:
                    time.sleep(snooze_time.seconds)
                self.snooze = None
            else:
                time.sleep(1)

            # Check if stop button has been pressed
            if not self.stop_button.disabled:
                self.stop_sound(None)
                break

        self.stop_button.disabled = True
        self.play_button.disabled = False

    def stop_sound(self, instance):
        self.stop_button.disabled = True

    def snooze_10(self, instance):
        self.snooze = datetime.now() + timedelta(minutes=10)

    def snooze_15(self, instance):
        self.snooze = datetime.now() + timedelta(minutes=15)

if __name__ == '__main__':
    SoundApp().run()
