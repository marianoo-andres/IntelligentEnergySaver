import json
from Logger import Logger
from MonitorEvents import MonitorEvents
from ScreenSaver import ScreenSaver
from SystemTrayIcon import SystemTrayIcon

systemTrayIcon = SystemTrayIcon(title='Intelligent Energy Saver')


class ScreenSaverApp():
    def __init__(self):
        with open('config.json') as file:
            self.config = json.load(file)

        if not self.debugModeEnabled():
            Logger.getInstance().disable()

    def debugModeEnabled(self):
        return self.config["modo_debug"].lower() == "si"

    def start(self):
        screenSaver = ScreenSaver(self.config)
        Logger.getInstance().debug("Starting ScreenSaver")
        screenSaver.start()

        monitorEvents = MonitorEvents(screenSaver)
        Logger.getInstance().debug("Starting MonitorEvents")
        monitorEvents.start()


def main():
    try:
        screenSaverApp = ScreenSaverApp()
        screenSaverApp.start()
    except Exception as e:
        Logger.getInstance().error("Critical error: {}".format(e))


main()
