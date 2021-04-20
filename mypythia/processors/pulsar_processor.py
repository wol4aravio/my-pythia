import configparser
from uuid import uuid4

import pulsar

from mypythia.processors.template import AbstractProcessor


class PulsarProcessor(AbstractProcessor):
    def __init__(self, url=None):
        if url is None:
            config = configparser.ConfigParser()
            config.read("config.ini")
            url_ = config["urls"]["UrlPulsar"]
        else:
            url_ = url
        self._pulsar_client = pulsar.Client(url_)

    def __enter__(self, url=None):
        return self

    def __exit__(self, _, __, ___):
        self.close()

    def close(self):
        self._pulsar_client.close()

    def send(self, message: str, topic: str, *args, **kwargs):
        producer = self._pulsar_client.create_producer(topic)
        producer.send(message.encode("utf-8"))

    def subscribe(self, topic, *args, **kwargs):
        consumer = self._pulsar_client.subscribe(
            topic, subscription_name=kwargs.get("name", str(uuid4()))
        )
        return consumer
