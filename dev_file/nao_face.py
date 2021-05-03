#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Get an image. Display it and save it using PIL."""
from subprocess import check_output

import qi
import argparse
import sys
import time
#import Image
from PIL import Image
from naoqi import ALProxy

#
# Module 1: Get Image from Nao Camera
def main(session):
    """
    First get an image, then show it on the screen with PIL.
    """
    # Get the service ALVideoDevice.

    video_service = session.service("ALVideoDevice")
    resolution = 2    # VGA
    colorSpace = 11   # RGB

    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)

    t0 = time.time()

    # Get a camera image.
    # image[6] contains the image data passed as an array of ASCII chars.
    naoImage = video_service.getImageRemote(videoClient)

    t1 = time.time()

    # Time the image transfer.
    print ("acquisition delay ", t1 - t0)

    video_service.unsubscribe(videoClient)


    # Now we work with the image returned and save it as a PNG  using ImageDraw
    # package.

    # Get the image size and pixel array.
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    image_string = str(bytearray(array))

    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

    # Save the image.
    im.save("./img/face.png", "PNG")

    im.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.86.31",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    switch = None
    while switch is None:
        switch = memProxy.getData("switch")

    main(session) 

# if face image, get person sex, age, emotion 

#
    response = check_output("python3 face_prediction.py ", shell=True)
    print(response)

    # slicing the list (negative index means index from the end)
    # -1 means the last element of the list
    face_emotion = response.split()[-1]
    face_age = response.split()[-3]
    face_sex = response.split()[-5]
    
    print(face_emotion)
    print(face_age)
    print(face_sex)


    # create proxy on ALMemory
    memProxy = ALProxy("ALMemory","192.168.86.31",9559)

    #insertData. Value can be int, float, list, string
    memProxy.insertData("face_emotion", face_emotion)
    memProxy.insertData("face_age", face_age)
    memProxy.insertData("face_sex", face_sex)

    #getData
    print("The value of this guy is", memProxy.getData("face_emotion"))
    print("The value of this guy is", memProxy.getData("face_age"))
    print("The value of this guy is", memProxy.getData("face_sex"))




