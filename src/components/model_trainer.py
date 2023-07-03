#
import os, sys
from dataclasses import dataclass

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor)
from catboost import CatBoostRegressor
# from xgboost import XGBRegressor

from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src import utils

@dataclass
class ModelTrainerConfig:
    model_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:

    def __init__(self):
        self.model_triner_config = ModelTrainerConfig()

    def model_training_process(self, train_array, test_array):
        try:
            logging.info("Splitting train and test data into independent and dependent part")
            # Splitting train and test data into independent and dependent part
            X_train, X_test, y_train, y_test = (train_array[:,:-1], test_array[:,:-1], train_array[:,-1], test_array[:,-1])
            models = {
                "Linear Regression": LinearRegression(),
                "Gradient Boosting Regressor": GradientBoostingRegressor(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest Regressor": RandomForestRegressor(),
                # "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest Regressor": {
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],

                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting Regressor": {
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                # "XGBRegressor": {
                #     'learning_rate': [.1, .01, .05, .001],
                #     'n_estimators': [8, 16, 32, 64, 128, 256]
                # },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [.1, .01, 0.5, .001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "K-Neighbors Regressor": {
                    'weights': ['uniform','distance'],
                    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute']
                }

            }

            prediction_report = utils.model_prediction(X_train, X_test, y_train, y_test, models, params)
            print("Report: ", prediction_report)
            max_score = max(list(prediction_report.values()))
            max_score_model_name = list(prediction_report.keys())[ list(prediction_report.values()).index(max_score) ]
            best_model = models[max_score_model_name]

            if max_score < 0.5:
                raise  CustomException("No best model found", sys)
            logging.info(f"Best model: {max_score_model_name}, R2 Score: {max_score}")

            # Saving the model
            utils.save_obj_as_pkl(self.model_triner_config.model_path, best_model)

            y_pred  = best_model.predict(X_test)
            r2_scor = r2_score(y_test, y_pred)
            return r2_scor

        except Exception as e:
            raise CustomException(e, sys)