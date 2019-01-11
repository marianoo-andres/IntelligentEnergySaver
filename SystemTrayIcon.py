import os

from os import path

from traybar import SysTrayIcon


class SystemTrayIcon():
    def doNothing(self, systray):
        pass

    def __init__(self, title="Titulo"):
        #basepath = path.dirname(__file__)

        #iconPath = path.abspath(path.join(basepath, "..", "icono.ico"))
        iconPath = 'icono.ico'
        hoverText = title
        quitText = "Salir"

        menuOptions = ((title, None, self.doNothing),)

        sysTrayIcon = SysTrayIcon(iconPath, hoverText, menuOptions, quit_text=quitText)
        sysTrayIcon.start()


