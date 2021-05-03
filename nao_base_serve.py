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
    
    time.sleep(4)

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
    im.save("./img/camImage.png", "PNG")

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

    # create proxy on ALMemory
    memProxy = ALProxy("ALMemory","192.168.86.31",9559)



    switch = None
    while switch != 'round1':
        try:
            switch = memProxy.getData("switch")
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        except:
            pass
            # print('.')

# if food image, get calorie value called calorie_value
    
    main(session) 

    response = check_output("python3 food.py ", shell=True)
    print(response)

    # slicing the list (negative index means index from the end)
    # -1 means the last element of the list
    calorie_value = response.split()[-1]
    type_value = response.split()[0]
    # print(type_value)
    # print(calorie_value)


    

    #insertData. Value can be int, float, list, string
    memProxy.insertData("value_food", calorie_value)
    memProxy.insertData("type_food", type_value)

    #getData
    # print("The value of food calorie is", memProxy.getData("value_food"))
    # print("The type of food is", memProxy.getData("type_food"))



