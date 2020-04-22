import os
import glob
import argparse

import numpy as np

from scipy.io import wavfile
from python_speech_features import mfcc
from hmmlearn import hmm

import cv2
import lightgbm as lgbm

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

def loadEdgesDataFromDirs(**dirNames):
    #Image dimensions
    imH = 80
    imW = 80
    
    #Thresholding for canny edge detection
    minVal = 50
    maxVal = 250


    X = np.array([])
    y = []
    
    for label, dirName in dirNames.items():
        for f in glob.glob(dirName + '/*.png'):
            img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
            img = img[:imH+1, :imW+1] #crop
            edges = cv2.Canny(img, minVal, maxVal) #extract edges
            edges = edges.reshape(np.prod(edges.shape)) #flatten
            
            #append
            if len(X) == 0:
                X = edges
            else:
                X = np.vstack((X, edges))
            
            assert label in ('target', 'nonTarget')
            if(label == 'target'):
                y.append(1)
            elif(label == 'nonTarget'):
                y.append(0)

    return X, y



def handleArguments():
    parser = argparse.ArgumentParser()

    #add arguments
    parser.add_argument("--imageTargetTrainDir")
    parser.add_argument("--imageNonTargetDir")

    return parser.parse_args()

def main():
    args = handleArguments()

#Read target data
XTrain, yTrain = loadEdgesDataFromDirs(target=args.imageTargetTrainDir, nonTarget=args.imageNonTargetTrainDir)

main()