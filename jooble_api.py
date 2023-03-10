import http.client
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonrpclib import Server
import time
import threading
import cgi
import random
host = 'jooble.org'
key = '290e9824-d65f-4b8c-94cc-c2cba6e290f5'

connection = http.client.HTTPConnection(host)
headers = {"Content-type": 'application/json,text/javascript, */*',
'Content-Type': 'application/x-www-form-urlencoded'}

class job: 
    
#request headers

#json query
    def jobposting():

        body = '{ "keywords": "Computer",}'
        connection.request('POST','/api/' + key, body, headers)
        response = connection.getresponse()
        title_data = []
        job_location = []
        job_description = []
        print(response.status, response.reason)
        data = response.read()
        #print(data)
        data_load = json.loads(data)
        regex = r'[\r\n\t\s]+|&nbsp;|<b>|</b>'

        #print("----------------------")
        for i in data_load["jobs"]:
            title_data.append(i["title"])
            #print("job title:",i["title"])
            #print("job location:",i["location"])
            job_location.append(i['location'])
            i["snippet"] = re.sub(regex, ' ', i["snippet"])
            job_description.append(i["snippet"])
        
        #print(type(title_data))
        #title_data = 'x' 
        #job_location = 'y'
        return (title_data, job_location,job_description)


if __name__== "__main__":
    job.jobposting()


