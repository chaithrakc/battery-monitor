import json
import os
import time
import psutil
from win10toast import ToastNotifier
from twilio.rest import Client


class BatteryNotifier:
    def __init__(self):
        relative_filepath = os.path.join('..', 'resources', 'settings.json')
        self.iconpath = os.path.join('..', 'resources', 'battery-charging.ico')
        with open(relative_filepath) as file_handler:
            self.settings = json.load(file_handler)
        self.client = Client(self.settings['account_sid'], self.settings['authtoken'])
        self.toaster = ToastNotifier()

    def notify_status(self):
        while True:
            battery = psutil.sensors_battery()
            if battery.percent >= self.settings['maxbattery_percentage'] and battery.power_plugged:
                self.send_notification(battery)
            elif not battery.power_plugged:
                self.toaster.show_toast('Battery (unplugged) ', str(battery.percent)+'%', self.iconpath)
                exit(0)
            time.sleep(15)

    def send_notification(self, battery):
        msg = 'Battery ' + str(battery.percent) + '% (plugged in)'
        self.toaster.show_toast(msg, 'disconnect!', self.iconpath)
        self.client.messages.create(from_=self.settings['twilio_phone'], to=self.settings['self_phone'], body=msg)


if __name__ == '__main__':
    batteryNotifier = BatteryNotifier()
    batteryNotifier.notify_status()
