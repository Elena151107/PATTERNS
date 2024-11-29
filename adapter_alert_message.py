## adapter_home_work.py
""" Задание: Создать систему оповещений для различных устройств, которые поддерживают разные интерфейсы.
Условия задачи:
1. Интерфейс IAlert — описывает метод send_alert(message: str), который используется для отправки уведомлений. Этот интерфейс должен поддерживаться всеми устройствами.
2. Устройства для оповещений:
◦ Телефон — поддерживает метод send_sms(text: str), который отправляет текстовое сообщение.
◦ Электронная почта — поддерживает метод send_email(subject: str, body: str), где subject — тема письма, а body — текст письма.
◦ Система громкой связи — поддерживает метод broadcast(message: str), который озвучивает сообщение через громкоговоритель.
3. Адаптеры — для каждого устройства (Телефон, Электронная почта, Система громкой связи) создать отдельный адаптер, который реализует интерфейс IAlert
и приводит методы этих устройств к единому виду send_alert.
4. Клиентский код — написать функцию, которая принимает список устройств с интерфейсом IAlert и отправляет оповещение всем устройствам через метод send_alert. """

from abc import ABC, abstractmethod


# target

class IAlert(ABC):
    @abstractmethod
    def send_alert(self, message: str):
        pass

# интерфейсы, который хотим адаптировать

class Telephone():
    def send_sms(self, text: str):
        print(f'Вам отправлено сообщение: [{text}]')

class Email():
    def send_email(self, subject: str, body: str):
        print(f'{subject}, вам отправлено письмо: [{body}]')

class Speakerphone():
    def broadcast(self, message: str):
        print(f'Внимание всех слушателей! Прослушайте следующее сообщение: [{message}]')


# адаптеры

class TelephoneAdapter(IAlert):
    def __init__(self, adapt: Telephone):
        self.adapt = adapt

    def send_alert(self, message: str):
        self.adapt.send_sms(message)

class EmailAdapter(IAlert):
    def __init__(self, adapt: Email):
        self.adapt = adapt
        self.subject = 'Manager_name'

    def send_alert(self, message: str):
        self.adapt.send_email(self.subject, message)

class SpeakerphoneAdapter(IAlert):
    def __init__(self, adapt: Speakerphone):
        self.adapt = adapt

    def send_alert(self, message: str):
        self.adapt.broadcast(message)


# клиентский код

def send_alert_device(device: IAlert, message: str):
    device.send_alert(message)

phone = Telephone()
mail = Email()
speaker = Speakerphone()
a_phone = TelephoneAdapter(phone)
a_mail = EmailAdapter(mail)
a_speaker = SpeakerphoneAdapter(speaker)
send_alert_device(a_phone, 'Сегодня в 13:00 всем сотрудникам пройти в конференц-зал!')
send_alert_device(a_mail, 'Сегодня в 13:00 всем сотрудникам пройти в конференц-зал!')
send_alert_device(a_speaker, 'Сегодня в 13:00 всем сотрудникам пройти в конференц-зал!')


#####
""" Вам отправлено сообщение: [Сегодня в 13:00 всем сотрудникам пройти в конференц-зал!]
Manager_name, вам отправлено письмо: [Сегодня в 13:00 всем сотрудникам пройти в конференц-зал!]
Внимание всех слушателей! Прослушайте следующее сообщение: [Сегодня в 13:00 всем сотрудникам пройти в конференц-зал!] """
