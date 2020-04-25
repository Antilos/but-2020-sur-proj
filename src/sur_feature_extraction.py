import glob

import numpy as np

import cv2

from scipy.io import wavfile
from python_speech_features import mfcc

from sur_output_log import add_audio_file, add_image_file

def loadEdgesDataFromDirsUnsorted(**dirNames):
    # Image dimensions
    imH = 80
    imW = 80
    # Thresholding for canny edge detection
    minVal = 50
    maxVal = 250
    X = np.array([])

    for label, dirName in dirNames.items():
        for f in glob.glob(dirName + '/*.png'):
            # adds log about the file for output
            add_image_file(f)
            img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
            img = img[:imH + 1, :imW + 1]  # crop
            edges = cv2.Canny(img, minVal, maxVal)  # extract edges
            edges = edges.reshape(np.prod(edges.shape))  # flatten

            # append
            if len(X) == 0:
                X = edges
            else:
                X = np.vstack((X, edges))

    return X

def loadEdgesDataFromDirs(train, **dirNames):
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
            if not train:
                # adds log about the file for output
                add_image_file(f)
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

def extractMFCCFromDir(dirName):
    # gets called while train
    X = np.array([])
    for f in glob.glob(dirName + '/*.wav'):
        fs, s = wavfile.read(f)
        mfcc_features = mfcc(s, fs)
        
        if len(X) == 0:
            X = mfcc_features
        else:
            X = np.append(X, mfcc_features, axis=0)
    
    return X

def extractListOfMFCCFromDir(dirName):
    # gets called from eval
    result = []
    for f in glob.glob(dirName + '/*.wav'):
        # adds file to log for output, counts on this being called on evaluating file
        add_audio_file(f)
        fs, s = wavfile.read(f)
        result.append(mfcc(s, fs))
    
    return result
