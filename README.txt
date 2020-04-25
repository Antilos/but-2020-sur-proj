SUR Image and Sound recogniction software

Team members: xdrabe09, xkocal00, xlebod00, xstrna14, xzilka11

The program attempts to match an audio sample of a person's voice and an image of their face to the corresponding person.
For audio detection we chose the HMM clasificator and for image recogniction we chose the lightgbm clasificator.

Results can be found in:
	audio_only_classification
	image_only_classification
	audio_and_image_classification

How to run: (all need to be run from src/ dir!)

Required packages and their version can be found in the requirements.txt file.
If any packages are missing or are of an incorrect version please run:

> pip install -r src/requirements.txt

If .model files are missing or the models need re-training

> python make.py train

For training place training data in the target_train/ or non_target_train/ folders based on whether the data
is to be expected to be a hit or not.

To run evaluation:

> python make.py eval

For evaluation the required data is to be placed in eval/ folder