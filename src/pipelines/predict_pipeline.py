import sys
import pandas as pd

from  src.exception import CustomException
from src.exception import logging
from src import utils

class PredictPipeline:

    def __init__(self):
        pass

    def predict_input(self, input_features):
        try:
            # Loading the column transformer preprocessor and model object from the pickle file
            preprocessor_path = 'artifacts\preprocessor.pkl'
            model_path        = 'artifacts\model.pkl'
            preprocessor      = utils.load_pickle_object(preprocessor_path)
            model             = utils.load_pickle_object(model_path)

            # First transforming the data and then predicting the output
            transformed_input_features = preprocessor.transform(input_features)
            input_prediction           = model.predict(transformed_input_features)
            return  input_prediction

        except Exception as e:
            raise  CustomException(e, sys)

class CustomData():

    def __init__(self,item_weight,item_visibility,item_mrp,outlet_establishment_year,item_fat_content,item_type,outlet_size,outlet_location_type,outlet_type):
        self.item_weight               = item_weight
        self.item_visibility           = item_visibility
        self.item_mrp                  = item_mrp
        self.outlet_establishment_year = outlet_establishment_year
        self.item_fat_content          =  item_fat_content
        self.item_type                 =  item_type
        self.outlet_size               =  outlet_size
        self.outlet_location_type      =  outlet_location_type
        self.outlet_type               =  outlet_type


    def transform_input(self):
        try:
            input_data_dict = {
                "Item_Weight":                [self.item_weight],
                "Item_Visibility":            [self.item_visibility],
                "Item_MRP":                   [self.item_mrp],
                "Outlet_Establishment_Year":  [self.outlet_establishment_year],
                "Item_Fat_Content":           [self.item_fat_content],
                "Item_Type":                  [self.item_type],
                "Outlet_Size":                [self.outlet_type],
                "Outlet_Location_Type":       [self.outlet_location_type],
                "Outlet_Type":                [self.outlet_type]
            }
            return  pd.DataFrame(input_data_dict)

        except Exception as e:
            raise CustomException(e, sys)




