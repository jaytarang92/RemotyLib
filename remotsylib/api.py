""" Remotsy library for python
    Copyright 2018 Jorge Cisneros jorge@remotsy.com
"""
from json import dumps, loads
from urllib2 import Request, urlopen, HTTPError, URLError
import sys


class API(object):
    """ API class for the remotsy lib core """
    def __init__(self, apiurl="https://remotsy.com/rest/"):
        self.apiurl = apiurl
        self.auth_key = None

    def post(self, url, data):
        """ Generic function to do a http post """
        req = Request(self.apiurl + url)
        req.add_header('Content-Type', 'application/json')
        if self.auth_key is not None:
            data["auth_key"] = self.auth_key
        try:
            resp = urlopen(req, dumps(data))
        except HTTPError as errobj:
            print errobj
            sys.exit(-1)
        except URLError as errobj:
            print errobj
            sys.exit(-2)
        else:
            body = loads(resp.read())
            return  body

    def login(self, username, password):
        """ Function to do the login and return a auth token """
        data = {"username": username,
                "password": password}

        self.auth_key = None
        ret = self.post("session/login", data)
        if ret["status"] == "success":
            self.auth_key = ret["data"]["auth_key"]
        return self.auth_key

    def list_controls(self):
        """ Function to get the list of the remotsy controls """
        ret = self.post("controls/list", {})
        if ret["status"] == "success":
            return ret["data"]["controls"]
        return None

    def list_buttons(self, idctl):
        """ Function to get the list of the button of a control """
        ret = self.post("controls/get_buttons_control", {"id_control": idctl})
        if ret["status"] == "success":
            return ret["data"]["buttons"]
        return None

    def blast(self, iddev, idbto, ntime=1):
        """ Function to blast infrared code via remotsy """
        ret = self.post("codes/blast", {"id_dev": iddev, "code": idbto, "ntime": ntime})
        return ret["status"] == "success"
