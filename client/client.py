import requests

def get_recommendations(server_url, songs):
    payload = {"songs": songs}
    try:
        response = requests.post(
            f"{server_url}/api/recommend",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            data = response.json()
            print("\nRecomendações recebidas:")
            print("Músicas recomendadas:", data.get("songs", []))
            print("Data do modelo:", data.get("model_date", "Desconhecida"))
            print("Versão da API:", data.get("version", "Desconhecida"))
        else:
            print(f"Erro ao acessar a API: {response.status_code}")
    except Exception as e:
        print(f"Erro durante a requisição: {e}")

if __name__ == "__main__":
    print("Bem-vindo ao cliente de recomendação de playlists!")
    server_url = input("Digite o URL do servidor (ex.: http://127.0.0.1:30502): ").strip()
    songs = input("Digite as músicas separadas por vírgula (ex.: Yesterday, Bohemian Rhapsody): ").split(",")
    songs = [song.strip() for song in songs]
    get_recommendations(server_url, songs)