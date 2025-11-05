import os
import logging
import logging.config
import yaml

def initialize_logs(name: str):
    """Initialize logs from the config file"""
    
    # Crée le dossier logs si nécessaire
    os.makedirs("logs", exist_ok=True)

    # Détermine le chemin absolu du fichier YAML
    base_dir = os.path.dirname(os.path.dirname(__file__))  # remonte à /MagicSearch
    config_path = os.path.join(base_dir, "src", "logging_config.yml")

    # Charge la configuration YAML
    with open(config_path, encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    # Initialise la configuration de logging
    logging.config.dictConfig(config)

    # Log de démarrage
    logging.info("-" * 50)
    logging.info(f"Starting {name}")
    logging.info("-" * 50)

    return logging