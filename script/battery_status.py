import json
import os
import time
import psutil
from win10toast import ToastNotifier
from twilio.rest import Client


class BatteryNotifier:
    def __init__(self):
        relative_filepath = os.path.join('..', 'resources', 'settings.json')
        with open(relative_filepath) as file_handler:
            self.settings = json.load(file_handler)
        self.client = Client(self.settings['account_sid'], self.settings['authtoken'])
        self.toaster = ToastNotifier()

    def notify_status(self):
        while True:
            battery = psutil.sensors_battery()
            if battery.percent >= self.settings['maxbattery_percentage'] and battery.power_plugged:
                self.toaster.show_toast("Battery Percentage " + str(battery.percent))
                self.twilio_notifier(battery.percent)
            elif not battery.power_plugged:
                exit(0)
            time.sleep(10)

    def twilio_notifier(self, battery_percent: int):
        msg_body = "Battery Percentage " + str(battery_percent)
        self.client.messages.create(from_=self.settings['twilio_phone'], to=self.settings['self_phone'], body=msg_body)
