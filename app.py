from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from src.pipelines.predict_pipeline import PredictPipeline, CustomData

application = Flask(__name__)
app = application

# Route for a home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['GET', 'POST'])
def input_data_prediction():
    if request.method == "GET":
        return render_template('prediction_page.html')
    else:
        cus_obj = CustomData(
            item_weight               = float(request.form.get('item_weight')),
            item_visibility           = float(request.form.get('item_visibility')),
            item_mrp                  = float(request.form.get('item_mrp')),
            outlet_establishment_year = int(request.form.get('outlet_establishment_year')),
            item_fat_content          = request.form.get('item_fat_content'),
            item_type                 = request.form.get('item_type'),
            outlet_size               = request.form.get('outlet_size'),
            outlet_location_type      = request.form.get('outlet_location_type'),
            outlet_type               = request.form.get('outlet_type')
        )
        input_dataframe = cus_obj.transform_input()
        print(input_dataframe.head())
        pipeline_obj = PredictPipeline()
        prediction = pipeline_obj.predict_input(input_dataframe)
        print("Prediction: ",prediction)
        return render_template('prediction_page.html', results = prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)