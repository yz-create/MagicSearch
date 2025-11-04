import os
import logging
import logging.config
import yaml


def initialiser_logs(nom):
    """Initialize logs from the config file"""

    # print current working directory
    # print(os.getcwd())
    # os.chdir('ENSAI-2A-projet-info-template')

    # Create the logs folder at the root if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    stream = open("logging_config.yml", encoding="utf-8")
    config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)

    logging.info("-" * 50)
    logging.info(f"Starting {nom}                           ")
    logging.info("-" * 50)
