from abc import ABC, abstractmethod

import numpy as np
from sklearn.linear_model import LogisticRegression

class Classifier(ABC):
    def __init__(
        self,
        name: str,
        random_state: int,
        **model_configs,
    ):
        """
        creates a prediction object
        Parameters
        ----------
        random_state : seed used when performing any random operation
        name : prediction model name
        model_family : family of the prediction model (e.g. neural network, trees)
        is_regression : specify if the model is a regression or classification model
        max_iteration : maximum number of iteration for training
        n_jobs : number of parallel jobs that the model can use
        """
        self.random_state = random_state
        self.name = name       
        self.model_additional_configs = model_configs
        self.model = None
        self.fitted_model = None
        self.metrics_dict = {}
        self.training_set_true = None
        self.training_set_pred = None
        self.early_stopping_enabled = False
        self.early_stopping_params = {}
        self.grid_search_enabled = False
        self.model_params = {}

    @abstractmethod
    def get_features_ranking(self) -> dict:
        """
        return features ranking
        Returns
        -------
        dict of features as keys and ranking as values
        """

    def fit(self, x_data: np.ndarray, y_data: np.ndarray, **fit_configs: dict):
        """
        fits a machine learning model a created a fitted model
        Parameters
        ----------
        x_data :  numpy array of input X_data for the model fitting
        y_data : numpy array of target data
        fit_configs : dict of additional parameters for fitting the model
        Returns
        -------
        return a fitted model
        """

        self.fitted_model = self.model.fit(x_data, y_data, **fit_configs)
        self.training_set_true = y_data
        self.training_set_pred = self.model.predict(x_data)
        return self.fitted_model

    def predict(self, x_data: np.ndarray) -> np.ndarray:
        res_array = self.fitted_model.predict(x_data)
        return res_array
    
class SVMClassifier(Classifier):
    def __init__(
        self,
        c: float = 10,
        kernel: str = "rbf",
        gamma: str = "scale",
        random_state: int = 1,
        **model_configs,
    ):
        """
        create a support vector classifier object
        Parameters
        ----------
        c : inversely related to l2 reguralisation parameter (outliers)
        kernel : kernel to use in the svm machine
        gamma : kernel coefficient
        random_state : seed used for drawing random numbers
        n_jobs : number of jobs to be used by svm
        """
        super().__init__(
            name="SVM_Classifier",
            random_state=random_state,
            **model_configs,
        )
        self.c = c
        self.kernel = kernel
        self.gamma = gamma
        self.model = SVC(
            C=self.c,
            kernel=self.kernel,
            gamma=self.gamma,
            max_iter=self.max_iteration,
            random_state=self.random_state,
            **self.model_additional_configs,
        )

    def get_features_ranking(self):
        # the code of features ranking is to be determined
        pass

    def create_object_model(self):
        # to be implemented soon
        pass



class LogisticRegressionClassifier(Classifier):
    def __init__(self, random_state: int = 1, **model_configs):
        super().__init__(
            name="Logistic_Regression",
            random_state=random_state,
            **model_configs
        )
        self.model = LogisticRegression(
            random_state=self.random_state,
            **self.model_additional_configs
        )

    def get_features_ranking(self):
        # the code of features ranking is to be determined
        pass

    def create_object_model(self):
        # to be implemented soon
        pass


if __name__ == "__main__":
    logistic_model_config = {
        "tol": 0.001,
        "max_iter": 200

    }

    logistic_regression = LogisticRegressionClassifier(**logistic_model_config)
    print(logistic_regression.__dict__)