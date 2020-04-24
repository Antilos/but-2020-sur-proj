import os
import glob
import argparse
import pickle

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

from sur_hmm_model import HMMTrainer
from sur_hmm_model import HMMBinaryModel

def handleArguments():
    parser = argparse.ArgumentParser()

    #add arguments
    parser.add_argument("--targetTrainDir", required=True, help="Relative path to the directory containing training target data.")
    parser.add_argument("--nonTargetTrainDir", required=True, help="Relative path to the directory containing training non-target data.")
    parser.add_argument("--hmmModelOutput", type=argparse.FileType('wb'), help="Output file for HMM Model")
    parser.add_argument("--lgbmModelOutput", type=argparse.FileType('wb'), help="Output file for LigthGBM Model")

    return parser.parse_args()

def main():
    args = handleArguments()

    #Rea ddata
    XImgTrain, yImgTrain = loadEdgesDataFromDirs(True, target=args.targetTrainDir, nonTarget=args.nonTargetTrainDir)

    XAudioTargetTrain = extractMFCCFromDir(args.targetTrainDir)
    # yAudioTargetTrain = [1 for i in range(len(XAudioTargetTrain))]
    XAudioNonTargetTrain = extractMFCCFromDir(args.nonTargetTrainDir)
    # yAudioNonTargetTrain = [0 for i in range(len(XAudioNonTargetTrain))]

    #train and pickle
    if(args.hmmModelOutput):
        hmmClassifier = HMMBinaryModel()
        hmmClassifier.fit(XAudioTargetTrain, XAudioNonTargetTrain)
        pickle.dump(hmmClassifier, args.hmmModelOutput)

    if(args.lgbmModelOutput):
        gbmClassifier = lgbm.LGBMModel(objective='binary', random_state=42)
        gbmClassifier.fit(XImgTrain, yImgTrain)
        pickle.dump(gbmClassifier, args.lgbmModelOutput)


main()