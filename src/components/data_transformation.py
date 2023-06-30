import sys, os
import  numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

from src.exception import CustomException
from src.logger import logging
from dataclasses import  dataclass
from src import utils

class DataTransformationConfig:
    preprocessor_object_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            numerical_columns   = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Establishment_Year']
            categorical_columns = ['Item_Fat_Content', 'Item_Type', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']

            numerical_pipeline = Pipeline([
                ('num_imputer', SimpleImputer(strategy='mean')),
                ('num_scaler', StandardScaler())
            ])
            logging.info('Numerical pipeline created in data transformation process.')

            categorical_pipeline = Pipeline([
                ('cat_imputer', SimpleImputer(strategy='constant', fill_value='Missing')),
                ('cat_onehot', OneHotEncoder(sparse=False, handle_unknown='ignore'))
            ])
            logging.info('Categorical pipeline created in data transformation process.')

            # Creating the column transformer
            ct = ColumnTransformer([
                ('num_pipeline', numerical_pipeline, numerical_columns),
                ('cat_pipeline', categorical_pipeline, categorical_columns)
            ])
            return ct

        except Exception as e:
            raise  CustomException(e, sys)

    def data_transformation_process(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df  = pd.read_csv(test_path)

            logging.info("Getting preprocessor object")
            preprocessor_obj = self.get_data_transformation_object()

            # Seperating independent(input) and dependent(output) columns
            outout_column_name = "Item_Outlet_Sales"
            input_train_df  = train_df.drop(outout_column_name, axis=1)
            output_train_df = train_df[outout_column_name]
            input_test_df = test_df.drop(outout_column_name, axis=1)
            output_test_df = test_df[outout_column_name]

            # Transforming the tarin and test independent features
            logging.info("Transforming train and test independent features")
            input_train_df_transformed = preprocessor_obj.fit_transform(input_train_df)
            input_test_df_transformed  = preprocessor_obj.transform(input_test_df)

            # Concatenating independent features and dependent feature in train dataframe
            # train_array = np.concatenate((input_train_df_transformed, np.array(output_train_df).reshape((6818,1)) ), axis=1)
            train_array   = np.c_[input_train_df_transformed, np.array(output_train_df)]

            # test_array = np.concatenate((input_test_df_transformed, np.array(output_test_df).reshape((6818,1)) ), axis=1)
            test_array   = np.c_[input_test_df_transformed, np.array(output_test_df)]

            # Saving the preprocessor(column transformer object) object as a pickle file
            utils.save_obj_as_pkl(self.data_transformation_config.preprocessor_object_path, preprocessor_obj)

            # Returning train array, test array, and preprocessor file path
            return ( train_array, test_array, self.data_transformation_config.preprocessor_object_path)

        except Exception as e:
            raise CustomException(e, sys)