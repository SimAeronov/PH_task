# IMPORTANT! opencv-python==4.5.5.62
from cv2 import cv2


async def take_webcam_picture():
    """
    Simple function that I use to take a webcam picture and return np.array
    :return: image as -> np.array
    """

    my_web_camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Camera needs some time to adjust
    dada, image = my_web_camera.read()

    cv2.imshow("Press any KEY to Close window", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    my_web_camera.release()
    return image


async def save_webcam_picture(cv2_image):
    with open("image_test.jpg", 'wb') as file:
        file.write(cv2_image[0])

