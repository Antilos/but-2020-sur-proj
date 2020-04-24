# SUR Image and Sound recogniction software

**Assignment**: https://www.fit.vutbr.cz/study/courses/SUR/public/projekt_2019-2020/SUR_projekt2019-2020.txt

## How to run:

> pip install -r requirements.txt

If .model files are missing or the models need re-training

> python make.py train

For training place training data in the *target_train/* or *non_target_train* folders based on whether the data
is to be expected to be a hit or not.

To run evaluation:

> python make.py eval

For evaluation the required data is to be placed in *eval/* folder