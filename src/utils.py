import os
import sys
import pickle
# import dill
import  pandas as pd
import  numpy as np

from src.exception import CustomException
from src.logger import logging
from sklearn.metrics import  r2_score

def save_obj_as_pkl(path, obj):
    try:
        dir_name = os.path.dirname(path)
        # Creating the directory
        os.makedirs(dir_name, exist_ok=True)

        # Saving object as pkl file
        pickle.dump(object, open(path, mode='wb'))

        # with open(path, 'wb') as file_obj:
        #     dill.dump(object, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def model_prediction(X_train, X_test, y_train, y_test, models):
    try:
        result = {}

        for i in range(len(models.values())):
            model_name = list(models.keys())[i]
            model      = models[model_name]

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred  = model.predict(X_test)

            train_score  = r2_score(y_train, y_train_pred)
            test_score   = r2_score(y_test, y_test_pred)

            result[model_name] = test_score

        return result
    except Exception as e:
        raise CustomException(e, sys)