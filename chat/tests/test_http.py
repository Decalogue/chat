#!/usr/bin/env python3
import sys
import uuid
import io, os, subprocess, wave, base64
import math, audioop, collections, threading
import platform, stat
import json
import requests

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode, quote  

class WaitTimeoutError(Exception): pass
class RequestError(Exception): pass
class UnknownValueError(Exception): pass 

def send():
    url_post_base = "http://192.168.2.32:8080/wx"
    headers = {"Content-Type": "application/json"}
    # Obtain audio transcription results
    try:
        response = requests.get(url_post_base, headers=headers)
    except HTTPError as e:
        raise RequestError("recognition request failed: {0}".format(getattr(e, "reason", "status {0}".format(e.code)))) 
    except URLError as e:
        raise RequestError("recognition connection failed: {0}".format(getattr(e, "reason", "status {0}".format(e.code))))
        
    print(response.headers)	

if __name__ == "__main__":	
    send()