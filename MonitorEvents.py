"""
https://stackoverflow.com/questions/48720924/python-3-detect-monitor-power-state-in-windows
"""
import threading

import win32con
import win32api
import win32gui
import time
from ctypes import POINTER, windll, Structure, cast, CFUNCTYPE, c_int, c_uint, c_void_p, c_bool
from comtypes import GUID
from ctypes.wintypes import HANDLE, DWORD

PBT_POWERSETTINGCHANGE = 0x8013
GUID_CONSOLE_DISPLAY_STATE = '{6FE69556-704A-47A0-8F24-C28D936FDA47}'
GUID_ACDC_POWER_SOURCE = '{5D3E9A59-E9D5-4B00-A6BD-FF34FF516548}'
GUID_BATTERY_PERCENTAGE_REMAINING = '{A7AD8041-B45A-4CAE-87A3-EECBB468A9E1}'
GUID_MONITOR_POWER_ON = '{02731015-4510-4526-99E6-E5A17EBD1AEA}'
GUID_SYSTEM_AWAYMODE = '{98A7F580-01F7-48AA-9C0F-44352C29E5C0}'


class POWERBROADCAST_SETTING(Structure):
    _fields_ = [("PowerSetting", GUID),
                ("DataLength", DWORD),
                ("Data", DWORD)]


class MonitorEvents(threading.Thread):
    # MONITOR EVENTS
    POWER_STATUS_CHANGED = 0
    SYSTEM_RESUME = 1
    SYSTEM_RESUME_BY_USER_INPUT = 2
    SYSTEM_SUSPEND = 3
    POWER_SETTING_CHANGED = 4
    DISPLAY_OFF = 5
    DISPLAY_ON = 6
    DISPLAY_DIMMED = 7
    AC_POWER = 8
    BATTERY_POWER = 9
    SHORT_TERM_POWER = 10
    BATTERY_REMAINING = 11
    MONITOR_OFF = 12
    MONITOR_ON = 13
    EXITING_AWAY_MODE = 14
    ENTERING_AWAY_MODE = 15
    UNKNOWN_GUID = 16
    def __init__(self, monitorEventHandler):
        threading.Thread.__init__(self)
        self.eventHandler = monitorEventHandler

    def wndproc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_POWERBROADCAST:
            if wparam == win32con.PBT_APMPOWERSTATUSCHANGE:
                # Power status has changed
                pass
            if wparam == win32con.PBT_APMRESUMEAUTOMATIC:
                # System resume
                pass
            if wparam == win32con.PBT_APMRESUMESUSPEND:
                # System resume by user input
                pass
            if wparam == win32con.PBT_APMSUSPEND:
                # System suspend
                pass
            if wparam == PBT_POWERSETTINGCHANGE:
                # Power setting changed

                settings = cast(lparam, POINTER(POWERBROADCAST_SETTING)).contents
                power_setting = str(settings.PowerSetting)
                data_length = settings.DataLength
                data = settings.Data
                if power_setting == GUID_CONSOLE_DISPLAY_STATE:
                    if data == 0:
                        # Display off
                        self.eventHandler.handleEvent(MonitorEvents.DISPLAY_OFF)
                    if data == 1:
                        # Display on
                        self.eventHandler.handleEvent(MonitorEvents.DISPLAY_ON)
                    if data == 2:
                        # Display dimmed
                        pass
                elif power_setting == GUID_ACDC_POWER_SOURCE:
                    if data == 0:
                        # AC power
                        pass
                    if data == 1:
                        # Battery power
                        pass
                    if data == 2:
                        # Short term power
                        pass
                elif power_setting == GUID_BATTERY_PERCENTAGE_REMAINING:
                    # battery remaining: %s' % data
                    pass
                elif power_setting == GUID_MONITOR_POWER_ON:
                    if data == 0:
                        # Monitor off
                        pass
                    if data == 1:
                        # Monitor on
                        pass
                elif power_setting == GUID_SYSTEM_AWAYMODE:
                    if data == 0:
                        # Exiting away mode
                        pass
                    if data == 1:
                        # Entering away mode
                        pass
                else:
                    # unknown GUID
                    pass
            return True

        return False

    def run(self):
        hinst = win32api.GetModuleHandle(None)
        wndclass = win32gui.WNDCLASS()
        wndclass.hInstance = hinst
        wndclass.lpszClassName = "testWindowClass"
        CMPFUNC = CFUNCTYPE(c_bool, c_int, c_uint, c_uint, c_void_p)
        wndproc_pointer = CMPFUNC(self.wndproc)
        wndclass.lpfnWndProc = {win32con.WM_POWERBROADCAST: wndproc_pointer}
        try:
            myWindowClass = win32gui.RegisterClass(wndclass)
            hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT,
                                           myWindowClass,
                                           "testMsgWindow",
                                           0,
                                           0,
                                           0,
                                           win32con.CW_USEDEFAULT,
                                           win32con.CW_USEDEFAULT,
                                           0,
                                           0,
                                           hinst,
                                           None)
        except Exception as e:
            #print("Exception: %s" % str(e))
            pass

        if hwnd is None:
            #print("hwnd is none!")
            pass
        else:
            #print("hwnd: %s" % hwnd)
            pass

        guids_info = {
            'GUID_MONITOR_POWER_ON': GUID_MONITOR_POWER_ON,
            'GUID_SYSTEM_AWAYMODE': GUID_SYSTEM_AWAYMODE,
            'GUID_CONSOLE_DISPLAY_STATE': GUID_CONSOLE_DISPLAY_STATE,
            'GUID_ACDC_POWER_SOURCE': GUID_ACDC_POWER_SOURCE,
            'GUID_BATTERY_PERCENTAGE_REMAINING': GUID_BATTERY_PERCENTAGE_REMAINING
        }
        for name, guid_info in guids_info.items():
            result = windll.user32.RegisterPowerSettingNotification(HANDLE(hwnd), GUID(guid_info), DWORD(0))
            #print('registering', name)
            #print('result:', hex(result))
            #print('lastError:', win32api.GetLastError())
            #print()

        #print('\nEntering loop')
        while True:
            win32gui.PumpWaitingMessages()
            time.sleep(1)
