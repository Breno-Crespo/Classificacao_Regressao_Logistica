from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import joblib

# Criar a instancia do FastAPI
app = FastAPI()

# Criar uma classe que terá os dados do request
class request_body(BaseModel):
    A_id: int
    Size: float
    Weight: float
    Sweetness: float
    Crunchiness: float
    Juiciness: float
    Ripeness: float
    Acidity: float

# Carregar o modelo para realizar a classificação 
modelo_qualidade = joblib.load('./modelo_qualidade_frutas.pkl')

@app.post('/classify')
def predict(data: request_body):
    # Preparar features
    input_features = [[data.Size, data.Weight, data.Sweetnes, 
                       data.Crunchiness, data.Juicines, data.Ripeness,
                       data.Acidity]]
    
    # Classificar Fruta
    y_pred = modelo_qualidade.predict(input_features)[0].astype(int)
    y_prob = modelo_qualidade.predict_proba(input_features).astype(float)

    resposta = 'Boa' if y_pred == 1 else 'Ruim'
    probabilidade = y_prob[y_pred]

    return {'qualidade': resposta, 'probabilidade': probabilidade}
