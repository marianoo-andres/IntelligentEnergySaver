import json
import threading
import time
from Camera import Camera
from FaceDetector import FaceDetector
from Logger import Logger
from MonitorEvents import MonitorEvents
from Screen import Screen


class ScreenSaver(threading.Thread):
    def handleEvent(self, event, data=None):
        if event == MonitorEvents.DISPLAY_OFF:
            Logger.getInstance().debug("Handle event SCREEN TURNED OFF")
            # Screen turned off
            self.screenOn = False
            # Reset time count
            self.lastTick = time.clock()
        elif event == MonitorEvents.DISPLAY_ON:
            Logger.getInstance().debug("Handle event SCREEN TURNED ON")
            # Screen turned on
            self.screenOn = True
            # Reset time count
            self.lastTick = time.clock()

    def validateConfig(self, config):
        timeOff = config['tiempo_apagado_en_minutos']
        try:
            int(timeOff)
        except:
            raise Exception("tiempo_apagado_en_minutos tiene que ser un número entero")
        if type(timeOff) == float:
            raise Exception("tiempo_apagado_en_minutos tiene que ser un número entero")
        if int(timeOff) <= 0:
            raise Exception("tiempo_apagado_en_minutos tiene que ser mayor o igual a 1")
        energyMode = config['modo_ahorro_energia'].lower()
        if not energyMode == 'si' and not energyMode == 'no':
            raise Exception("modo_ahorro_energia tiene que ser 'si' o 'no'")

    def setConfig(self, config):

        # Validate fields. If error exit
        self.validateConfig(config)

        # Turn off screen if no face detected during noFaceTime seconds
        self.noFaceTime = config['tiempo_apagado_en_minutos'] * 60

        # Take picture every takePictureRateTime seconds
        self.takePictureRateTime = 10

        aux = config['modo_ahorro_energia'].lower()
        # If False then turn on screen when face detected
        self.energySaveMode = True if aux == 'si' else False

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.faceDetector = FaceDetector()
        self.screen = Screen()
        self.camera = Camera()
        # Modify by MonitorEvents
        self.screenOn = True
        # Amount of pictures to check every cycle (more pictures more precise the face detection)
        self.picturesToTake = 5

        # Set config params
        self.setConfig(config)

        # Loop variables
        self.lastTick = None
        self.restartCamera = False  # used only in energySaveMode = True
        self.screenPreviousState = 'on'  # used only in energySaveMode = True

    def faceInFrame(self, frame):
        # Detect faces
        faceLocations = self.faceDetector.detect(frame, resize=True, resizeProportion=0.5)
        return len(faceLocations) > 0

    def faceDetected(self):
        for x in range(self.picturesToTake):
            # Take the picture
            frame = self.camera.takePicture()
            # Check if there are faces in the frame
            if self.faceInFrame(frame):
                return True
        # No picture had faces
        return False

    def handleTurnOffScreen(self, elapsed):
        # If screen is off do nothing
        if not self.screenOn:
            return
        # Check if should turn off screen
        if elapsed > self.noFaceTime:

            Logger.getInstance().debug("No se detecto una cara por {} segundos. Apagando pantalla".format(self.noFaceTime))
            # Face not detected in noFaceTime seconds. Turn off screen
            self.screen.turnOff()
            """
            #Test (to see cpu usage when idle)
            Logger.getInstance().debug("Turning off screen")
            self.handleEvent(MonitorEvents.DISPLAY_OFF)
            timer = threading.Timer(30, self.handleEvent, [MonitorEvents.DISPLAY_ON])
            timer.start()
            """

    def loopEnergySaveMode(self):
        if not self.screenOn:
            if self.screenPreviousState == 'on':
                self.restartCamera = False
                self.screenPreviousState = 'off'
                self.camera.stop()
            time.sleep(1)
            return
        else:
            if self.screenPreviousState == 'off':
                self.screenPreviousState = 'on'
                self.restartCamera = True

        if self.restartCamera:
            Logger.getInstance().debug("restarting camera")
            self.camera.start()
            self.restartCamera = False

        # Check if there is a face
        Logger.getInstance().debug("Detectando cara...")
        if self.faceDetected():
            Logger.getInstance().debug("Cara detectada")
            # Reset time count
            self.lastTick = time.clock()
        else:
            Logger.getInstance().debug("Cara no detectada")
        # Time elapsed from last face detected
        elapsed = time.clock() - self.lastTick

        # Turn off screen if no face detected in time specified
        self.handleTurnOffScreen(elapsed)

        # Sleep to take picture every takePictureRateTime seconds
        time.sleep(self.takePictureRateTime)

    def loopNoEnergySaveMode(self):
        # Check if there is a face
        Logger.getInstance().debug("Detectando cara...")
        if self.faceDetected():
            if not self.screenOn:
                self.screen.turnOn()
            Logger.getInstance().debug("Cara detectada")
            # Reset time count
            self.lastTick = time.clock()
        else:
            Logger.getInstance().debug("Cara no detectada")
        # Time elapsed from last face detected
        elapsed = time.clock() - self.lastTick

        # Turn off screen if no face detected in time specified
        self.handleTurnOffScreen(elapsed)

        if self.screenOn:
            # Sleep to take picture every takePictureRateTime seconds
            time.sleep(self.takePictureRateTime)

    def run(self):
        self.camera.start()
        self.lastTick = time.clock()

        if self.energySaveMode:
            loop = self.loopEnergySaveMode
        else:
            loop = self.loopNoEnergySaveMode
        while True:
            loop()

    def stop(self):
        self.camera.stop()
