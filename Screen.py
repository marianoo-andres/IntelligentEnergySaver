import win32gui

import time
import win32con
import win32api
from os import getpid, system
from threading import Timer

from Logger import Logger


class Screen():
    def turnOff(self):
        SC_MONITORPOWER = 0xF170
        Logger.getInstance().debug("Empiezo a mandar el mensaje de apagado")
        tick = time.clock()
        win32gui.SendMessageTimeout(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2, 0, 5000)
        # win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2)
        Logger.getInstance().debug("Termine de mandar mensaje de apagado. Tarde {} segundos".format(time.clock() - tick))

    def turnOn(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, 0, 0)
