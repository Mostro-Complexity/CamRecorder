# coding:utf-8
import cv2
import argparse
from camera import Camera
from draw import Gravity, put_text

if __name__ == '__main__':
    camera_dict = {'gray': 0, 'openni': cv2.CAP_OPENNI,
                   'openni2': cv2.CAP_OPENNI2}

    parser = argparse.ArgumentParser(
        description='Run the camera(sensor) to record some data')
    parser.add_argument('-o', '--out',
                        help='Your record filename including path')
    parser.add_argument('-c', '--camera', choices=[
                        'gray', 'openni', 'openni2'], default='gray',
                        help='Your choice of the kind of camera to use')

    args = parser.parse_args()

    with Camera(camera_dict[args.camera]) as cam:
        def callback(frame, depth, fps):
            # Unable to retrieve correct frame, it's still depth here
            put_text(frame, "{1}x{0}".format(*frame.shape), Gravity.TOP_LEFT)

            cv2.imshow('frame', frame)
            frameCapWriter.write(frame)
            if(depth is not None):
                # Unable to retrieve correct frame, it's still depth here
                put_text(depth, "{1}x{0}".format(
                    *depth.shape), Gravity.TOP_LEFT)
                put_text(depth, "%.1f" % fps, Gravity.TOP_RIGHT)
                cv2.imshow('depth', depth)
                depthCapWriter.write(depth)
            pass

        frameCapWriter = cv2.VideoWriter(
            args.out + '.rgb.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), cam.fps, cam.size())
        depthCapWriter = cv2.VideoWriter(
            args.out + '.d.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), cam.fps, cam.size())


        print("Camera: %dx%d, %d" % (
            cam.get(cv2.CAP_OPENNI_IMAGE_GENERATOR +
                    cv2.CAP_PROP_FRAME_WIDTH),
            cam.get(cv2.CAP_OPENNI_IMAGE_GENERATOR +
                    cv2.CAP_PROP_FRAME_HEIGHT),
            cam.get(cv2.CAP_OPENNI_IMAGE_GENERATOR + cv2.CAP_PROP_FPS)))

        print("Press Esc or Q to quit")

        cam.capture(callback, False)

    cv2.destroyAllWindows()
