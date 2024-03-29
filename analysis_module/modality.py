from datetime import datetime, timedelta
import requests
from typing import Literal, Optional


MethodLiteral = Literal["GET", "POST"]
ModalityLiteral = Literal["speed", "smoothness", "rotation", "proxemics"]


class Modality(object):
    def __init__(
        self,
        name: ModalityLiteral,
        threshold: float,
        base_url: str,
        increase_path: str,
        decrease_path: str = None,
        neutral_path: str = None,
        increase_method: MethodLiteral = "POST",
        decrease_method: MethodLiteral = "POST",
        neutral_method: MethodLiteral = "POST",
        cooldown_duration: int = 5,
        **kwargs,
    ):
        self.name = name
        self.threshold = threshold
        self.base_url = base_url
        self.increase_path = increase_path
        self.increase_method = increase_method
        self.decrease_path = decrease_path
        self.decrease_method = decrease_method
        self.neutral_path = neutral_path
        self.neutral_method = neutral_method
        self.cooldown_duration = cooldown_duration
        self._cooldown_end = datetime.now()

    def _get(self, url: str):
        response = requests.get(url)
        return response

    def _post(self, url: str, body: dict = None):
        response = requests.post(url, json=body) if body else requests.post(url)
        return response

    def _set_cooldown(self):
        now = datetime.now()
        self._cooldown_end = now + timedelta(seconds=self.cooldown_duration)

    def increase(self, body: dict = None):
        if self._cooldown_end > datetime.now():
            print("cooldown for {} not over, increase".format(self.name), flush=True)
            return None
        print("would increase {}".format(self.name), flush=True)
        self._set_cooldown()
        if self.increase_method == "POST":
            result = self._post(self.base_url + self.increase_path, body)
            self._set_cooldown()
            return result
        else:
            # GET
            result = self._get(self.base_url + self.increase_path)
            self._set_cooldown()
            return result

    def decrease(self, body: dict = None):
        if self._cooldown_end > datetime.now():
            print("cooldown for {} not over, decrease".format(self.name), flush=True)
            return None
        print("would decrease {}".format(self.name), flush=True)
        self._set_cooldown()
        if self.decrease_method == "POST":
            result = self._post(self.base_url + self.decrease_path, body)
            self._set_cooldown()
            return result
        else:
            # GET
            result = self._get(self.base_url + self.decrease_path)
            self._set_cooldown()
            return result

    def neutral(self, body: dict = None):
        if self._cooldown_end > datetime.now():
            print("cooldown for {} not over, neutral".format(self.name), flush=True)
            return None
        if self.neutral_path is None:
            print("no neutral path for {}".format(self.name), flush=True)
            return None
        print("would neutral {}".format(self.name), flush=True)
        if self.neutral_method == "POST":
            result = self._post(self.base_url + self.neutral_path, body)
            return result
        else:
            # GET
            result = self._get(self.base_url + self.neutral_path)
            return result
