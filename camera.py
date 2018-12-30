import cv2
import sys


class Camera(object):

    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        self.openni = index in (cv2.CAP_OPENNI, cv2.CAP_OPENNI2)
        # Tentative frame number 10
        self.fps = 10

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def release(self):
        if not self.cap:
            return
        self.cap.release()
        self.cap = None

    def _depth_capture(self, callback, gray):
        if not self.cap.grab():
            sys.exit('Grabs the next frame failed')
        ret, depth = self.cap.retrieve(cv2.CAP_OPENNI_DEPTH_MAP)
        ret, frame = self.cap.retrieve(cv2.CAP_OPENNI_GRAY_IMAGE
                                       if gray else cv2.CAP_OPENNI_BGR_IMAGE)
        # Normalize the depth for representation
        min, max = depth.min(), depth.max()
        depth = np.uint8(255 * (depth - min) / (max - min))
        return frame, depth

    def _rgb_capture(self, callback, gray):
        ret, frame = self.cap.read()
        if not ret:
            sys.exit('Reads the next frame failed')
        if gray:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame, None

    def capture(self, callback, gray=True):
        if not self.cap:
            sys.exit('The capture is not ready')

        while True:
            # t = cv2.getTickCount()
            frame, depth = None, None
            if self.openni:
                frame, depth = self._depth_capture(callback, gray)
            else:
                frame, depth = self._rgb_capture(callback, gray)
            if callback:
                callback(frame, depth, self.fps)

            # t = cv2.getTickCount() - t
            # self.fps = cv2.getTickFrequency() / t
            # self.fps = self.cap.get(cv2.CAP_PROP_FPS)

            # press esc or q to quit
            ch = cv2.waitKey(10) & 0xFF
            if ch == 27 or ch == ord('q'):
                break

    def fps(self):
        # return self.fps
        return self.cap.get(cv2.CAP_PROP_FPS)

    def get(self, prop_id):
        return self.cap.get(prop_id)

    def set(self, prop_id, value):
        self.cap.set(prop_id, value)

    def size(self):
        return (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))


if __name__ == '__main__':
    def callback(gray, fps): return cv2.imshow('gray', gray)

    with Camera(0) as cam:
        print("Camera: %dx%d, %d" % (
            cam.get(cv2.CAP_PROP_FRAME_WIDTH),
            cam.get(cv2.CAP_PROP_FRAME_HEIGHT),
            cam.get(cv2.CAP_PROP_FPS)))
        cam.capture(callback)

    cv2.destroyAllWindows()
