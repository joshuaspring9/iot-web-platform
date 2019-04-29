
CLIENT_ID = 'change me'
CLIENT_SECRET = 'change me'
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


import glob
import json
import os
import time
import urllib2
import urlparse
import oauth2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


class UploadDataFile:
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        self.consumer = oauth2.Consumer(consumer_key, consumer_secret)
        self.token = oauth2.Token(oauth_token, oauth_token_secret)
        self.url = "http://localhost:8000/api/datafiles"

    def parse_response(self, result):
        content = json.loads(result)
        return content["response"]

    def uploadDataFile(self, post):

        img_file = post['data']
        del(post['data'])
        req = oauth2.Request.from_consumer_and_token(self.consumer,
                                                 token=self.token,
                                                 http_method="POST",
                                                 http_url=self.url,
                                                 parameters=post)
        req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        compiled_postdata = req.to_postdata()
        all_upload_params = urlparse.parse_qs(compiled_postdata, keep_blank_values=True)

        for key, val in all_upload_params.iteritems():
            all_upload_params[key] = val[0]

        all_upload_params['data'] = open(img_file, 'rb')
        datagen, headers = multipart_encode(all_upload_params)
        request = urllib2.Request(self.url, datagen, headers)

        try:
            respdata = urllib2.urlopen(request).read()
        except urllib2.HTTPError as ex:
            return 'Received error code: ', ex.code

        return self.parse_response(respdata)
        



api = UploadDataFile(CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

datafile = './test.pcap'
date  = time.gmtime(os.path.getmtime(datafile))
post = {
    'end_time' : time.strftime ("%Y-%m-%d %H:%M:%S", date),
    'data_file' : datafile,
    'devices_captured' : {
        1,
    },
    'data_capturing_device': 1,
}

try:
    response = api.uploadDataFile(post)
    print(response)
        
except:
    print("Error")

print("Done!")