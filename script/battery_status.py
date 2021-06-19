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
                self.send_notification(battery)
            elif not battery.power_plugged:
                exit(0)
            time.sleep(10)

    def send_notification(self, battery):
        msg_body = "Battery Percentage (plugged in) : " + str(battery.percent)
        iconpath = os.path.join('..', 'resources', 'battery-charging.ico')
        toast_success = self.toaster.show_toast('Battery ' + str(battery.percent) + '% (plugged in)', 'disconnect!', iconpath)
        # if notification is not displayed, send a WhatsApp notification
        if not toast_success:
            self.client.messages.create(from_=self.settings['twilio_phone'], to=self.settings['self_phone'],
                                        body=msg_body)
