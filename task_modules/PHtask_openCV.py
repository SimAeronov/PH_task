# IMPORTANT! opencv-python==4.5.5.62
from cv2 import cv2
import asyncio


async def take_webcam_picture():
    """
    Simple function that I use to take a webcam picture and return np.array
    :return: image as -> np.array
    """

    # Set captured_image=0 so that if there is an error with the image capturing, return value will be 0
    captured_image = 0
    my_web_camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # If the camera is currently being used, it won't oppen
    if my_web_camera.isOpened():
        # Camera needs some time to adjust
        await asyncio.sleep(0.5)
        successful_capture, captured_image = my_web_camera.read()



    cv2.imshow("Press any KEY to Close window", captured_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    my_web_camera.release()
    return captured_image

