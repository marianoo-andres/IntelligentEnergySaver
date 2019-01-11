import cv2
import face_recognition
import time


class FaceDetector():
    def detect(self, image, imageMode='BGR', resize=False, resizeProportion=1):
        """
        :param image: in np array rgb format
        :param imageMode: BGR or RGB
        :param resize: if true resize the image
        :param resizeProportion: i.e 0.25 to downscale the image to 1/4 of original size
        :return: faces locations. Empty list if no faces detected
        """
        # Resize image for faster face recognition processing
        if resize:
            image = cv2.resize(image, (0, 0), fx=resizeProportion, fy=resizeProportion)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        if imageMode == 'BGR':
            image = image[:, :, ::-1]

        # Get face locations
        face_locations = face_recognition.face_locations(image)

        # Scale back up face locations since the image we detected was resized
        if resize:
            original_face_locations = []
            for face_location in face_locations:
                top = face_location[0] * int(1/resizeProportion)
                right = face_location[1] * int(1/resizeProportion)
                bottom = face_location[2] * int(1/resizeProportion)
                left = face_location[3] * int(1/resizeProportion)
                original_face_locations.append((top,right,bottom,left))
            face_locations = original_face_locations
        return face_locations
