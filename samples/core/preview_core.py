#! /usr/bin/env python3
import cv2
import numpy as np

from resconfig import *
from bar4py.debugtools import drawMarkers, drawMarkersArea, drawAxis
from bar4py import CameraParameters, Dictionary, MarkerDetector

# Core modeuls preview.
def preview(imagefilename=None, videofilename='video.avi'):
    # Open capture
    if not imagefilename:
        cap = cv2.VideoCapture(opjoin(RES_VID, videofilename))

    # Load Camera Parameters
    cameraParameters = CameraParameters()
    cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))
    print('GLPV:', cameraParameters.cvt2GLProjection((640, 480)).tolist())
    # Create Dictionary
    dictionary = Dictionary()
    dictionary.buildByDirectory(filetype='*.jpg', path=RES_MRK)
    # Create MarkerDetector
    markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)
    while True:
        # Read video data
        if imagefilename:
            frame = cv2.imread(opjoin(RES_IMG, imagefilename))
        else:
            ret, frame = cap.read()
            if not ret: break
        markers, area = markerDetector.detect(frame, enArea=True)
        for marker in markers:
            print('ID:', marker.marker_id)
            print('GLMV:')
            print(marker.cvt2GLModelView())
            print('-'*32)
        drawMarkers(markers, frame)
        drawMarkersArea(area, frame)
        drawAxis(cameraParameters, markers, frame)
        cv2.imshow('Core Preview', frame)
        key = cv2.waitKey(100) & 0xFF
        if key == 27: break
        elif key == 32: cv2.waitKey(0)

    # Desctroy and release
    cv2.destroyAllWindows()
    if not imagefilename: cap.release()

if __name__ == '__main__': preview()
