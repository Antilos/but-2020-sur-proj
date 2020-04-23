import os
import glob
import argparse
import pickle
import logging

import numpy as np

from scipy.io import wavfile
from python_speech_features import mfcc
from hmmlearn import hmm

import cv2
import lightgbm as lgbm

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

from sur_feature_extraction import loadEdgesDataFromDirs
from sur_feature_extraction import extractMFCCFromDir
from sur_feature_extraction import extractListOfMFCCFromDir

from sur_hmm_model import HMMTrainer
from sur_hmm_model import HMMBinaryModel

logging.basicConfig(level=logging.DEBUG)

def predictionOutput(audioPredictions, audioY, imagePredictions, imageY):
    print(f'Audio Predictions')
    print(audioPredictions)
    print(f'Confusion Matrix\n{confusion_matrix(audioY, audioPredictions)}\nAccuracy: {accuracy_score(audioY, audioPredictions)}')

    print(f'Image Predictions')
    print(imagePredictions)
    print(f'Confusion Matrix\n{confusion_matrix(imageY, imagePredictions)}\nAccuracy: {accuracy_score(imageY, imagePredictions)}')

def handleArguments():
    parser = argparse.ArgumentParser()

    #add arguments
    parser.add_argument("--targetDevDir", required=True, help="Relative path to the directory containing target data to classify.")
    parser.add_argument("--nonTargetDevDir", required=True, help="Relative path to the directory containing non-target data to classify.")
    parser.add_argument("--hmmModel", required=True, type=argparse.FileType('rb'), help="File with HMM Model")
    parser.add_argument("--lgbmModel", required=True, type=argparse.FileType('rb'), help="File with LigthGBM Model")

    return parser.parse_args()

def main():
    args = handleArguments()

    lgbmClassifier = pickle.load(args.lgbmModel)
    hmmClassifier = pickle.load(args.hmmModel)

    #Read dev data
    XImgDev, yImgDev = loadEdgesDataFromDirs(target=args.targetDevDir, nonTarget=args.nonTargetDevDir)

    XAudioTargetDev = extractListOfMFCCFromDir(args.targetDevDir)
    yAudioTargetDev = [1 for i in range(len(XAudioTargetDev))]
    XAudioNonTargetDev = extractListOfMFCCFromDir(args.nonTargetDevDir)
    yAudioNonTargetDev = [0 for i in range(len(XAudioNonTargetDev))]

    # logging.debug(np.asarray(XAudioTargetDev)[])
    # logging.debug(len(XAudioTargetDev))
    # exit()

    audioPredictions = hmmClassifier.predict(XAudioTargetDev + XAudioNonTargetDev)
    imagePredictions = np.round(lgbmClassifier.predict(XImgDev))

    predictionOutput(audioPredictions, yAudioTargetDev+yAudioNonTargetDev, imagePredictions, yImgDev)

main()