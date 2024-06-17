import json
import mlflow
import os
import joblib

def init():
    global model
    model_path = os.getenv('AZUREML_MODEL_DIR')
    try:
        model = joblib.load(os.path.join(model_path, 'sim_rf_model/model.pkl'))
    except:
        model = mlflow.pyfunc.load_model(os.path.join(model_path, 'sim_rf_model/MLmodel'))

def run(data):
    try:
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, list):
            prediction = model.predict(data)
        else:
            prediction = model.predict([data])
        return json.dumps(prediction.tolist())
    except Exception as e:
        error = str(e)
        return json.dumps({"error": error})
