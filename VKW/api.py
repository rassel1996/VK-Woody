#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import vk_auth
import json
import urllib2
from urllib import urlencode

def call_api(method, params, token):
    params.append(("access_token", token))

    url      = "https://api.vk.com/method/%s?%s" % (method, urlencode(params))
    response = json.loads(urllib2.urlopen(url).read())

    if "response" not in response:
    	return {"error_code": response["error"]["error_code"]}
    else:
    	return response["response"]

def execute(method, token):
	return json.loads(urllib2.urlopen("https://api.vk.com/method/execute.%s?%s" % (method, urlencode([("access_token", token)]))).read())