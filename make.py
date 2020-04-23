import subprocess
import argparse

def handleArguments():
    parser = argparse.ArgumentParser(description="Functions as a make and makefile.")

    parser.add_argument('target', help="Make target.")

    return parser.parse_args()

def main():
    args = handleArguments()

    trainingScript = "sur_train.py"
    classifyScript = "sur_classify.py"

    targetTrainDir = "target_train"
    nonTargetTrainDir = "non_target_train"
    targetDevDir = "target_dev"
    nonTargetDevDir = "non_target_dev"

    hmmModelFilename = "hmm.model"
    lgbmModelFilename = "lgbm.model"

    if(args.target == 'train'):
        print("DING")
        subprocess.run(["python", trainingScript, "--targetTrainDir", targetTrainDir, "--nonTargetTrainDir", nonTargetTrainDir, "--hmmModelOutput", hmmModelFilename, "--lgbmModelOutput", lgbmModelFilename])
    elif(args.target == 'eval'):
        subprocess.run(["python", classifyScript, "--targetDevDir", targetDevDir, "--nonTargetDevDir", nonTargetDevDir, "--hmmModel", hmmModelFilename, "--lgbmModel", lgbmModelFilename])

main()