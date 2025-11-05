import os
import logging
import logging.config
import yaml

def initialize_logs(name: str):
    """Initialize logs from the config file"""
    
    os.makedirs("logs", exist_ok=True)

    # base_dir = /home/onyxia/work/MagicSearch/src
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, "logging_config.yml")  # <-- CORRECT

    # Vérification
    print("Looking for logging_config.yml at:", config_path)

    with open(config_path, encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    logging.config.dictConfig(config)
    logging.info("-" * 50)
    logging.info(f"Starting {name}")
    logging.info("-" * 50)

    return logging