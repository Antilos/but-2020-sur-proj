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
from sur_feature_extraction import loadEdgesDataFromDirsUnsorted
from sur_feature_extraction import extractMFCCFromDir
from sur_feature_extraction import extractListOfMFCCFromDir

from sur_hmm_model import HMMTrainer
from sur_hmm_model import HMMBinaryModel

from sur_output_log import work_results
from sur_output_log import add_image_scores

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
    parser.add_argument("--targetDevDir", required=False, help="Relative path to the directory containing target data to classify.")
    parser.add_argument("--nonTargetDevDir", required=False, help="Relative path to the directory containing non-target data to classify.")
    parser.add_argument("--testDir", required=False, help="Relative path to the directory containing unsorted datat to classify, must be combined with --unsorted")
    parser.add_argument("--hmmModel", required=True, type=argparse.FileType('rb'), help="File with HMM Model")
    parser.add_argument("--lgbmModel", required=True, type=argparse.FileType('rb'), help="File with LigthGBM Model")
    parser.add_argument("--unsorted", required=False, dest='unsorted', action='store_true', help="If present, only one file under --testDir will be evaluated")

    return parser.parse_args()

def main():
    args = handleArguments()

    lgbmClassifier = pickle.load(args.lgbmModel)
    hmmClassifier = pickle.load(args.hmmModel)

    if args.unsorted:
        XImgDev = loadEdgesDataFromDirsUnsorted(test=args.testDir)
        XAudioDev = extractListOfMFCCFromDir(args.testDir)
        # don't store results, because they are already logged inside the function predict
        hmmClassifier.predict(XAudioDev)
    else:
        # Read dev data
        XImgDev, yImgDev = loadEdgesDataFromDirs(False, target=args.targetDevDir, nonTarget=args.nonTargetDevDir)
        XAudioTargetDev = extractListOfMFCCFromDir(args.targetDevDir)
        yAudioTargetDev = [1 for i in range(len(XAudioTargetDev))]
        XAudioNonTargetDev = extractListOfMFCCFromDir(args.nonTargetDevDir)
        yAudioNonTargetDev = [0 for i in range(len(XAudioNonTargetDev))]

        audioPredictions = hmmClassifier.predict(XAudioTargetDev + XAudioNonTargetDev)
        imagePredictions = np.round(lgbmClassifier.predict(XImgDev))
        predictionOutput(audioPredictions, yAudioTargetDev + yAudioNonTargetDev, imagePredictions, yImgDev)

    image_score = lgbmClassifier.predict(XImgDev)
    add_image_scores(image_score, np.round(image_score))
    work_results()

main()