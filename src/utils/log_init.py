import os
import logging
import logging.config
import yaml


def initialize_logs(name):
    """Initialize logs from the config file"""

    # print current working directory
    # print(os.getcwd())
    # os.chdir('ENSAI-2A-projet-info-template')

    # Create the logs folder at the root if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    with open("logging_config.yml", encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)

    logging.info("-" * 50)
    logging.info(f"Starting {name}                           ")
    logging.info("-" * 50)
