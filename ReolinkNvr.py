import json
import string
import sys
from urllib import request

from Communicator import Communicator

class ReolinkNvr:

    def __init__(self, ip: str, username: str, password: str, https = False, **kwargs):
        """
        Initialise the Camera API Handler (maps api calls into python)
        :param ip:
        :param username:
        :param password:
        :param proxy: Add a proxy dict for requests to consume.
        eg: {"http":"socks5://[username]:[password]@[host]:[port], "https": ...}
        More information on proxies in requests: https://stackoverflow.com/a/15661226/9313679
        """
        scheme = 'https' if https else 'http'
        self.url = f"{scheme}://{ip}/cgi-bin/api.cgi"
        self.ip = ip
        self.token = None
        self.username = username
        self.password = password
        Communicator.proxies = kwargs.get("proxy")  # Defaults to None if key isn't found

    
    def login(self) -> bool:
        """
        Login in to obtain authentication token
        :return: bool
        """
        try:
            body = [{"cmd": "Login", "action": 0,
                     "param": {"User": {"userName": self.username, "password": self.password}}}]
            param = {"cmd": "Login", "token": "null"}
            response = Communicator.send(self.url, data=body, params=param)
            if response is not None:
                data = json.loads(response.text)[0]
                code = data["code"]

                if int(code) == 0:
                    self.token = data["value"]["Token"]["name"]
                    print("Login OK")
                    return True
                return False
            else:
                print("Failed to login\nStatus Code:", response.status_code)
                return False
        except Exception as e:
            print("Login Error\n", e)
            raise

    def logout(self) -> bool:
        """
        Log out of the NVR
        :return: bool
        """
        try:
            body=[{"cmd": "Logout", "action": 0}]
            param = {"cmd": "Logout", "token": self.token}
            response = Communicator.send(self.url, data=body, params=param)
            if response is not None:
                data = json.loads(response.text)[0]
                code = data["value"]["rspCode"]
                print("Logout ", code)
                return code == 200
        except Exception as e:
            print("Logout Error \n", e)
            raise

    def getchannelstatus(self) -> json or None:
        """
        Load the status of available channels in the NVR
        :returns: json
        """
        try:
            body = [{"cmd": "GetChannelStatus","action": 0}]
            param = {"cmd": "GetChannelStatus", "token": self.token}
            response = Communicator.send(self.url, data=body, params=param)
            if response is not None:
                return response.text
            else:
                return None
        except Exception as e:
            print("Get Channel Status Error \n", e)
            raise











class AttachedCamera:
    def __init__(self, channel: str, online: bool):
        self.channel = channel
        self.online = online
