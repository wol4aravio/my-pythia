import configparser
import json

from mypythia.processors.pulsar_processor import PulsarProcessor

CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")


def load_config(filename: str = "settings.json") -> list:
    with open(filename, "r") as file:
        return json.load(file)


def process_message(message: dict) -> None:
    with PulsarProcessor() as pulsar:
        pulsar.send(json.dumps(message), topic=CONFIG["topics"]["TopicRequest"])
