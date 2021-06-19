from script.battery_status import BatteryNotifier

if __name__ == '__main__':
    batteryNotifier = BatteryNotifier()
    batteryNotifier.notify_status()
