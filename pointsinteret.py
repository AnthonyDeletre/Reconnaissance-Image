# Détecteur de points d'intérets - Pas super utilisable comme ça
import numpy as numpy
import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('hub.jpg', 0)
img2 = cv2.imread('IMG_20190514_161034.jpg', 0)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

matches = bf.match(des1, des2)

matches = sorted(matches, key = lambda x : x.distance)
print(matches)
input()
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

plt.imshow(img3), plt.show()
