import cv2


class Camera():
    def __init__(self):
        self.videoCapture = None
        self.started = False

    def start(self):
        self.videoCapture = cv2.VideoCapture(0)
        self.started = True

    def takePictureToFile(self, filename):
        if not self.started:
            raise Exception('Camera should be started')
        success, frame = self.videoCapture.read()
        if not success:
            raise ValueError("Can't read frame")
        cv2.imwrite(filename, frame)

    def takePicture(self):
        if not self.started:
            raise Exception('Camera should be started')
        success, frame = self.videoCapture.read()
        if not success:
            raise ValueError("Can't read frame")
        return frame

    def stop(self):
        self.videoCapture.release()
