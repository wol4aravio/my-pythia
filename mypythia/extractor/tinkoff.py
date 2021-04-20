import requests


class Tinkoff:
    def __init__(self, token):
        self._basic_url = "https://api-invest.tinkoff.ru/openapi"
        self._token = token
        self._auth_header = {"Authorization": "Bearer {}".format(self._token)}

    def get_stocks_list(self):
        url = self._basic_url + "/market/stocks"
        request_result = requests.get(url, headers=self._auth_header)
        if request_result.status_code != 200:
            raise Exception(request_result.text)
        return request_result.json()["payload"]["instruments"]

    def get_stock_info(self, figi=None, ticker=None):
        if figi:
            parameters = {"figi": figi}
        else:
            parameters = {"ticker": ticker}
        key = list(parameters.keys())[0]
        url = self._basic_url + "/market/search/by-{}".format(key)
        request_result = requests.get(
            url,
            data=parameters,
            headers=self._auth_header,
        )
        if request_result.status_code != 200:
            raise Exception(request_result.text)
        data = request_result.json()["payload"]
        if ticker:
            return data["instruments"][0]
        return data

    def get_stock_history(
        self, figi=None, ticker=None, start=None, end=None, interval="hour"
    ):
        if not figi:
            figi = self.get_stock_info(ticker=ticker)["figi"]
        url = self._basic_url + "/market/candles"
        parameters = {
            "figi": figi,
            "from": start.isoformat(),
            "to": end.isoformat(),
            "interval": interval,
        }
        request_result = requests.get(
            url,
            params=parameters,
            headers=self._auth_header,
        )
        if request_result.status_code != 200:
            raise Exception(request_result.text)
        return request_result.json()["payload"]["candles"]
