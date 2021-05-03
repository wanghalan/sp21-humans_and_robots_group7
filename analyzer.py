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
from datetime import datetime

# location= 

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

    file_loc = '%s.txt' % datetime.now().strftime('%Y%m%d_%H%M')
    print('-'*80)
    print(file_loc)
    while True:
        try:
            stamp = memProxy.getData("stamp")
            if stamp == 'yes':
                now = datetime.now().strftime('%Y%m%d_%H%M%S')
                with open(file_loc, 'a') as f:
                    event = memProxy.getData('event')
                    f.write("%s: %s\n"%(now, event))
                print('\twrote: %s %s' % (now, event))
                memProxy.insertData("stamp", 'no')

        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        except:
            pass

    # #insertData. Value can be int, float, list, string
    # memProxy.insertData("value_food", calorie_value)


