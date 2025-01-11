from flask import Flask, request, jsonify
import pickle
import os
from datetime import datetime

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configurações da API
MODEL_PATH = "/models/rules.pkl"  # Caminho do modelo gerado na Parte 1
API_VERSION = "1.0.0"  # Versão da API

# Carrega o modelo de recomendação
def load_model():
    try:
        with open(MODEL_PATH, "rb") as file:
            model = pickle.load(file)
            model_date = datetime.fromtimestamp(os.path.getmtime(MODEL_PATH)).strftime("%Y-%m-%d %H:%M:%S")
            return model, model_date
    except FileNotFoundError:
        print(f"Modelo não encontrado no caminho: {MODEL_PATH}")
        return None, None

# Inicializa o modelo ao iniciar o servidor
app.model, app.model_date = load_model()

# Endpoint para recomendações
@app.route("/api/recommend", methods=["POST"])
def recommend():
    if not app.model:
        return jsonify({"error": "Modelo de recomendação não carregado"}), 500

    # Obtém os dados da requisição
    data = request.get_json(force=True)
    user_songs = data.get("songs", [])

    if not user_songs or not isinstance(user_songs, list):
        return jsonify({"error": "Campo 'songs' inválido ou ausente"}), 400

    # Gera recomendações com base nas regras do modelo
    recommendations = []
    for rule in app.model:
        antecedent, consequent, confidence = rule
        if antecedent.issubset(set(user_songs)):
            recommendations.extend(consequent)

    # Remove duplicatas das recomendações
    recommendations = list(set(recommendations) - set(user_songs))

    # Retorna a resposta em JSON
    return jsonify({
        "songs": recommendations,
        "version": API_VERSION,
        "model_date": app.model_date
    })

# Executa a aplicação na porta especificada
if __name__ == "__main__":
    PORT = 30502
    app.run(host="0.0.0.0", port=PORT)
