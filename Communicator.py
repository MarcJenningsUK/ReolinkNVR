import json
import requests

class Communicator:
    proxies = None

    @staticmethod
    def send(url: str, data, params=None) -> requests.Response or None:
        try:
            headers = {'content-type': 'application/json'}
            r = requests.post(url, verify=False, params=params, json=data, headers=headers, proxies=None)
            if r.status_code == 200:
                return r
            else:
                raise ValueError("Status: ", r.status_code)
        except Exception as e:
            print("Post Error\n", e)
            raise

