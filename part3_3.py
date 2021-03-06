# -*- coding: utf-8 -*-

import os
import sys
# This try-catch is a workaround for Python3 when used with ROS; it is not needed for most platforms
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
    pass
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal as mvn
prev_centroid = []
thresold = np.array([.00025])
def get_thresholded_pdf(frame, p1):
    frame[p1 == True] = 255
    frame[p1 == False] = 0
    return frame

def draw_buoy_contour(original_frame, reference_frame, color):
    global prev_centroid
    contours, hier = cv2.findContours(reference_frame, 1, 2)
    radius_r = []
    if contours:
        for c in contours:
            point,radius = cv2.minEnclosingCircle(c)
            radius_r.append(int(radius))
        max_r = np.argmax(radius_r)
        cnt = contours[max_r]
        moments = [cv2.moments(cnt)]
        centroids = [(int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])) for M in moments]
        #print(prev_centroid)
        for c in centroids:
            if not prev_centroid:
                cv2.circle(original_frame, c, radius_r[max_r], color, thickness=2)
            elif  np.sqrt((prev_centroid[0][1] - c[1])**2 + (prev_centroid[0][0] - c[0])**2) < 200:        #red 100
                cv2.circle(original_frame, c, radius_r[max_r], color, thickness=2)
            else:
                return original_frame
            # else:
            #     print('dist: ',np.sqrt((prev_centroid[0][1] - c[1])**2 + (prev_centroid[0][0] - c[0])**2) )
            #     cv2.circle(original_frame, c, radius_r[max_r], color, thickness=2)
    else:
        centroids = prev_centroid
    prev_centroid = centroids
    return original_frame

def detectTuning(log_likelihood, img, i):
    #log_likelihood = get_thresholded_pdf(log_likelihood, log_likelihood > 0.65*np.max(log_likelihood))
    if (i==2):
        kernel = np.ones((7,7),np.uint8)
        thresh = np.max(log_likelihood)
        # element = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,1))
        # log_likelihood = cv2.erode(log_likelihood,element)
        # cv2.imshow('eroded',log_likelihood)
        # op = (log_likelihood > .99*thresh  and log_likelihood > .000012)
        op = np.bitwise_and(log_likelihood > 0.5*thresh, log_likelihood > .0000129)
        #print('op',op)
        ind = np.unravel_index(np.argmax(op, axis=None), log_likelihood.shape)
        #ind = np.unravel_index(np.argwhere(log_likelihood == np.amax(log_likelihood)), log_likelihood.shape)
        #print('indices:',ind)
        print('thresh:', thresh)
        mask = np.zeros(log_likelihood.shape, dtype = "uint8")
        #print('thresh',thresh)
        cv2.circle(mask, (ind[1],ind[0]), 50, (255,255,255), -1)
        cv2.imshow('Greenmask',mask)
        print('Inside Green')
        op1= np.bitwise_and(log_likelihood > 0.3*thresh, mask)
        log_likelihood = get_thresholded_pdf(log_likelihood, (op))
        log_likelihood = cv2.dilate(log_likelihood,kernel,iterations = 1)
    if (i==0):
        kernel = np.ones((7,7),np.uint8)
        thresh = np.max(log_likelihood)
        op = np.bitwise_and(log_likelihood > 0.5*thresh, log_likelihood > .000025)
        log_likelihood = get_thresholded_pdf(log_likelihood, (op))
        log_likelihood = cv2.dilate(log_likelihood,kernel,iterations = 1)
    if i==1:
        kernel = np.ones((7,7),np.uint8)


        thresh = np.max(log_likelihood)
        op = np.bitwise_and(log_likelihood > 0.8*thresh, log_likelihood > .000012)

        ind = np.unravel_index(np.argmax(op, axis=None), log_likelihood.shape)
        mask = np.zeros(log_likelihood.shape, dtype = "uint8")
        cv2.circle(mask, (ind[1],ind[0]), 50, (255,255,255), -1)
        cv2.imshow('mask',mask)
        #
        op1= np.bitwise_and(log_likelihood > 0.3*thresh, op)
        log_likelihood = get_thresholded_pdf(log_likelihood, op1)

        log_likelihood = cv2.dilate(log_likelihood,kernel,iterations = 1)
        #cv2.imshow('log_likelihood', log_likelihood)

    return log_likelihood

def detectbuoy(img):
    K = 4
    colors = ['Red', 'Yellow', 'Green']
    colors_value = [(0,0,255),(0,255,255),(0,255,0)]
    # prev_centroid = []
    for i in range(0,3):
        w=np.load('parameters/weights_' +colors[i] + '.npy')
        Sigma=np.load('parameters/cv_' +colors[i] + '.npy')
        mean=np.load('parameters/mean_' +colors[i] + '.npy')
        nr, nc, d = img.shape
        n=nr*nc
        xtest=np.reshape(img,(n,d))
        likelihoods=np.zeros((K,n))
        log_likelihood=np.zeros(n)
        for k in range(K):
            likelihoods[k] = w[k] * mvn.pdf(xtest, mean[k], Sigma[k],allow_singular=True)
            log_likelihood = likelihoods.sum(0)
        log_likelihood = np.reshape(log_likelihood, (nr, nc))
        log_likelihood = detectTuning(log_likelihood, img, i)
        log_likelihood = log_likelihood.astype(np.uint8)
        frame = draw_buoy_contour(img, log_likelihood, colors_value[i])

    return img

def main():
    cap = cv2.VideoCapture("detectbuoy.avi")
    count =0
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('output_part_3.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame_width,frame_height))
    while cap.isOpened():
        ret, img = cap.read()
        if img is not None :
            #img = cv2.GaussianBlur(img,(5,5),0)
            #img = cv2.medianBlur(img,7)
            frame = detectbuoy(img)
            cv2.imshow('Buoy Deection', frame)
            out.write(frame)
            count = count +1
            print(count)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
