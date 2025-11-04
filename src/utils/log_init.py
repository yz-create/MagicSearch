import os
import logging
import logging.config
import yaml


def initialize_logs(name):
    """Initialize logs from the config file"""
    os.makedirs("logs", exist_ok=True)

    with open("src/logging_config.yml", encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)

    logging.info("-" * 50)
    logging.info(f"Starting {name}                           ")
    logging.info("-" * 50)
