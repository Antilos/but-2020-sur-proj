import numpy as np
from hmmlearn import hmm

# Class to handle all HMM related processing
class HMMTrainer(object):
    def __init__(self, model_name='GaussianHMM', n_components=4, cov_type='diag', n_iter=1000, seed=42):
        self.model_name = model_name
        self.n_components = n_components
        self.cov_type = cov_type
        self.n_iter = n_iter
        self.models = []

        if self.model_name == 'GaussianHMM':
            self.model = hmm.GaussianHMM(n_components=self.n_components, 
                    covariance_type=self.cov_type, n_iter=self.n_iter, random_state=seed)
        else:
            raise TypeError('Invalid model type')

    # X is a 2D numpy array where each row is 13D
    def train(self, X):
        np.seterr(all='ignore')
        self.models.append(self.model.fit(X))

    # Run the model on input data
    def get_score(self, input_data):
        return self.model.score(input_data)

class HMMBinaryModel:
    def __init__(self, model_name='GaussianHMM', n_components=4, cov_type='diag', n_iter=1000, seed=42):
        self.target_hmm_trainer = HMMTrainer(model_name, n_components, cov_type, n_iter, seed)
        self.non_target_hmm_trainer = HMMTrainer(model_name, n_components, cov_type, n_iter, seed)

    def fit(self, TargetX, NonTargetX):
        self.target_hmm_trainer.train(TargetX)
        self.non_target_hmm_trainer.train(NonTargetX)

    def predict(self, X):
        # X is a list of numpy arrays (sample_len, n_features)
        targetScores = []
        nonTargetScores = []
        for x in X:
            targetScores.append(self.target_hmm_trainer.get_score(x))
            nonTargetScores.append(self.non_target_hmm_trainer.get_score(x))

        predictions = []
        for targetScore, nonTargetScore in zip(targetScores, nonTargetScores):
            if(targetScore > nonTargetScore):
                predictions.append(1)
            else:
                predictions.append(0)
        
        return predictions