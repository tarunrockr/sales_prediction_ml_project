import os
import sys
import pickle
# import dill
import  pandas as pd
import  numpy as np

from src.exception import CustomException
from src.logger import logging

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

