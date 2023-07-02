# data_ingestion.py file is used to read data from different sources
# After reading the data we are splitting the dataset into train and test
import os
import sys
from  src.exception import CustomException
from  src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join('artifacts', 'train.csv')
    test_data_path  = os.path.join('artifacts', 'test.csv')
    raw_data_path   = os.path.join('artifacts', 'raw_data.csv')

class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def data_ingestion_process(self):
        # We write code to fetch data from multiple sources
        logging.info("Inside data ingestion process function")
        try:
            df = pd.read_csv(r"notebook\data\train.csv")
            # To create artifacts directory at root folder
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Saving raw data file in artifacts folder
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            # -------------  Some changes in dataframe before train test split  ----------------
            # Removing 'Item_Identifier' and 'Outlet_Identifier' columns
            df.drop( columns=['Item_Identifier', 'Outlet_Identifier'], inplace=True)
            # Replacing 'LF' and 'low fat' with 'Low Fat' and 'reg' with 'Regular' in "Item_Fat_Content" feature
            df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({'LF': 'Low Fat', 'low fat': 'Low Fat', 'reg': 'Regular'})

            # Splitting data dataset into train and test part
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Saving tarin and test data file in artifacts folder
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Data ingestion is complete.")

            # Return train and test file path as a tuple
            return self.ingestion_config.train_data_path, self.ingestion_config.test_data_path

        except Exception as e:
            raise CustomException(e, sys)

# if __name__ == "__main__":
#     obj = DataIngestion()
#     train_path, test_path =  obj.data_ingestion_process()
#     print("File path: ", (train_path, test_path) )
#
#     obj = DataTransformation()
#     train_array, test_array, preprocessor_path = obj.data_transformation_process(train_path, test_path)
#     print("Column transformer path: ", preprocessor_path)
#
#     model_trainer_obj = ModelTrainer()
#     r2_score_value    = model_trainer_obj.model_training_process(train_array, test_array)
#     print("Final R2 value: ", r2_score_value)


