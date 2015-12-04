#!/usr/bin/env python

import numpy as np
import cv2
import sys

cascade_path="/usr/share/OpenCV/haarcascades/"
statefile="/tmp/facestatus.dat"

samples_to_keep = 6
state_change_threshold = 2  # consider the state changed if this many samples change
poll_interval_ms = 100   # time to wait between samples

camera = cv2.VideoCapture(0)

def get_image():
    retval, im = camera.read()
    return im

def done():
    print ""
    camera.release()
    cv2.destroyAllWindows()
    print "Done."
    sys.exit(0)


class RingBuffer:
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur=0
            self.__class__ = RingBufferFull
    def get(self):
        """ return a list of elements from the oldest to the newest"""
        return self.data


class RingBufferFull:
    def __init__(self,n):
        raise "you should use RingBuffer"
    def append(self,x):     
        self.data[self.cur]=x
        self.cur=(self.cur+1) % self.max
    def get(self):
        return self.data[self.cur:]+self.data[:self.cur]

def show_img(img):
        try:
            if img is not None and detected is True:
                cv2.imshow('img',img) 

        except Exception as e:
            print "Couldn't show image: %s" % e

def write_state(filename, state):
    f = open(filename, "w")
    f.write("DETECTED" if state else "")
    f.close()

face_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_frontalface_default.xml')

rbuf = RingBuffer(samples_to_keep)  # keep the last N states
prev_detect = False
write_state(statefile, prev_detect)

try:
    while True:
        img = get_image()
        newimg = None
        rect = None
        detected = False
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,
                scaleFactor=1.25,
                minNeighbors=4,
                minSize=(36,36),
                rejectLevels=[],
                levelWeights=[]
                )

        for face in faces:
            detected = True
            (x,y,w,h) = face
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        rbuf.append(detected)

        #show_img(img)

        state = np.count_nonzero(rbuf.get()) > state_change_threshold

        if state != prev_detect:
            print "State changed: ", state
            write_state(statefile, state)
            prev_detect = state

        if cv2.waitKey(poll_interval_ms) & 0xFF == ord('q'):
            done()

except KeyboardInterrupt:
    pass

done()

