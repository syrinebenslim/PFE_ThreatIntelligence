from watcher.schemas.parser.data_parser import make_json

def main():
    # Chemin du fichier CSV d'entrée
    csv_file_path = "input.csv"

    # Chemin du fichier JSON de sortie
    json_file_path = "output.json"

    # Appel de la fonction pour convertir le CSV en JSON
    make_json(csv_file_path, json_file_path)

if __name__ == "__main__":
    main()