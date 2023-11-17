from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
import requests

class MyKivyApp(App):
    def build(self):
        self.text_input = TextInput(text='1')
        self.send_button = Button(text='Отправить', on_press=self.send_data)
        self.line = BoxLayout()
        self.line.add_widget(self.text_input)
        self.line.add_widget(self.send_button)
        return self.line

    def send_data(self, instance):
        url = 'http://127.0.0.1:5000/api'  # Замените на адрес своего сервера
        data_to_send = {'data': self.text_input.text}

        try:
            response = requests.post(url, json=data_to_send)
            if response.status_code == 200:
                print('Данные успешно отправлены на сервер')
            else:
                print(f'Ошибка при отправке данных. Код ответа: {response.status_code}')
        except Exception as e:
            print(f'Произошла ошибка: {e}')

if __name__ == '__main__':
    MyKivyApp().run()