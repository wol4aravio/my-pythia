import configparser

from mypythia.extractor.tools import (
    preprocess_message,
    process_candle,
    process_message,
    upload_candle,
)
from mypythia.processors.pulsar_processor import PulsarProcessor

CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")


with PulsarProcessor() as pulsar:
    consumer = pulsar.subscribe(
        CONFIG["topics"]["TopicRequest"], name="my_pythia_extractor"
    )

    while True:
        msg = consumer.receive()
        try:
            preprocessed_msg = preprocess_message(msg)
            candles = process_message(preprocessed_msg)
            candles = [process_candle(preprocessed_msg["ticker"], c) for c in candles]
            for c in candles:
                upload_candle(c)
            consumer.acknowledge(msg)
        except Exception:
            consumer.negative_acknowledge(msg)
