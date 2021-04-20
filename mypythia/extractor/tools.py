import configparser
import hashlib
import json
import os
from datetime import datetime as dt
from datetime import timedelta

import pytz
from pymongo import MongoClient

from mypythia.extractor.tinkoff import Tinkoff

CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")


def preprocess_message(message) -> dict:
    decoded = message.data().decode("utf-8")
    preprocessed = json.loads(decoded)
    return preprocessed


def process_message(message: dict) -> list:
    figi = message["figi"]
    interval = message["interval"]
    t_end = (dt.utcnow() + timedelta(hours=3)).replace(
        tzinfo=pytz.timezone("Etc/GMT-3")
    )
    t_start = t_end - timedelta(hours=1)
    api = Tinkoff(os.getenv("TINKOFF_TOKEN"))
    candles = api.get_stock_history(
        figi=figi, start=t_start, end=t_end, interval=interval
    )
    return candles


def generate_id(ticker: str, candle: dict) -> str:
    full_string = "_".join([ticker, candle["figi"], candle["interval"], candle["time"]])
    return hashlib.md5(full_string.encode("utf-8")).hexdigest()


def process_candle(ticker: str, candle: dict) -> dict:
    processed_candle = {
        "_id": generate_id(ticker, candle),
        "ticker": ticker,
        "figi": candle["figi"],
        "interval": candle["interval"],
        "ts": candle["time"],
        "open": candle["o"],
        "close": candle["c"],
        "high": candle["h"],
        "low": candle["l"],
        "volume": candle["v"],
    }
    return processed_candle


def upload_candle(candle: dict):
    mongo = MongoClient(
        CONFIG["urls"]["UrlDB"].format(
            user=os.getenv("MONGO_USER"),
            pwd=os.getenv("MONGO_PASS"),
        )
    )
    try:
        collection = mongo[CONFIG["db"]["Name"]][CONFIG["db"]["CollectionCandles"]]
        if collection.find_one({"_id": candle["_id"]}) is None:
            collection.insert_one(candle)
        upload_result = True
    except Exception:
        upload_result = False
    finally:
        mongo.close()
    return upload_result
