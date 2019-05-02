import os
import json
import requests


CLIENT_ID = 'U1UmRwMwq2DzSeik3N0a5kNIeXXGeUNtIXS2IAeQ'
CLIENT_SECRET = 'H7l1sLDWBDZOFyxZkwU7CWI7oltNlnebebUhyIPfhEGlUmgiJPV7VIIbA0MCnTJYxcRF3GVIVknrXvyUKRgnVzEf5BVZpYY0XKQS3hjiTl9fgU0aJwn48eJNLBbFJYGW'
OAUTH_TOKEN_FILE = 'token.txt'

class APIError(Exception):
    pass


class IOTWebPlatformAPI:

    def __init__(self, client_id, client_secret, data_files_url="http://localhost:8000/api/datafiles/", smart_devices_url="http://localhost:8000/api/smartdevices/", data_capture_devices_url="http://localhost:8000/api/capturedevices/", token_url="http://localhost:8000/api/o/token/", token_file='token.txt'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.data_files_url = data_files_url
        self.smart_devices_url = smart_devices_url
        self.capture_devices_url = data_capture_devices_url
        self.token_url = token_url
        self.token_file = token_file
        f = open(self.token_file, 'r')
        self.token = f.read()
        f.close()

    def get_new_token(self):
        data = {
            'grant_type': 'client_credentials',
            'scope': ['datafiles', 'devices']
        }
        response = requests.post(self.token_url, data=data, auth=(self.client_id, self.client_secret))
        if response.status_code >= 300:
            raise APIError("Failed to get a new access token.  Response was: " + response.text)
        else:
            response_dict = json.loads(response.text)
            if 'access_token' not in response_dict:
                raise APIError("Failed to get a new access token, even though HTTP code inidicated success.  Response: " + response.text)
            else:
                self.token = response_dict['access_token']
                f = open(self.token_file, 'w')
                f.write(self.token)
                f.close()

    def get_smart_devices(self, is_retry=False):

        if self.token == "":
            self.get_new_token()

        headers = {
            'Authorization': "Bearer " + self.token
        }

        response = requests.get(self.smart_devices_url, headers=headers)
        if response.status_code >= 300:
            if response.status_code == 401 and not is_retry:
                # token may have expired, try to fetch another one
                self.get_new_token()
                return self.get_smart_devices(True)
            else:
                raise APIError("Failed to get smart devices.  Response was: " + response.text)
        else:
            return json.loads(response.text)

    def get_capture_devices(self, is_retry=False):

        if self.token == "":
            self.get_new_token()

        headers = {
            'Authorization': "Bearer " + self.token
        }

        response = requests.get(self.capture_devices_url, headers=headers)
        if response.status_code >= 300:
            if response.status_code == 401 and not is_retry:
                # token may have expired, try to fetch another one
                self.get_new_token()
                return self.get_capture_devices(True)
            else:
                raise APIError("Failed to get smart devices.  Response was: " + response.text)
        else:
            return json.loads(response.text)

    def upload_data_file(self, file, is_retry=False):

        if self.token == "":
            self.get_new_token()

        handle = open(file, 'rb')

        smart_devices = self.get_smart_devices()
        capture_devices = self.get_capture_devices()

        if len(smart_devices) == 0:
            raise APIError("Cannot upload a data file when there are no smart devices to attach it to.")

        if len(capture_devices) == 0:
            raise APIError("Cannot upload a data file when there are no capture devices to attach it to.")
        

        bad_input = True

        while bad_input:
            bad_input = False
            print("Which devices did this data file capture?\n")
            for i in range(len(smart_devices)):
                print(str(i+1) + ". " + smart_devices[i]['name'])
            print()
            chosen_devices = input("Enter the numbers of the devices separated by spaces: ")
            print()
            if len(chosen_devices) == 0:
                print("Error: You did not enter any devices. Please try again.\n")
                bad_input = True
                continue
            captured_devices_urls = []
            seen_devices = {}

            for device in chosen_devices:
                try:
                    device_id = int(device)-1
                    if device_id >= len(smart_devices):
                        raise ValueError
                    if device_id not in seen_devices:
                        seen_devices[device_id] = 1
                        captured_devices_urls += [smart_devices[device_id]['url']]
                except ValueError:
                    print("Error: Please enter only integers representing the device id.\n")
                    bad_input = True
                    continue


        bad_input = True

        while bad_input:
            bad_input = False
            print("Which capture device was used to create this file?\n")
            for i in range(len(capture_devices)):
                print(str(i+1) + ". " + capture_devices[i]['name'])
            print()
            chosen_device = input("Enter the number of the device used: ")
            print()

            try:
                device_id = int(chosen_device)-1
                if device_id >= len(capture_devices):
                    raise ValueError
                capture_device_url = capture_devices[device_id]['url']
            except ValueError:
                print("Error: Please enter only a single integer representing the device id.\n")
                bad_input = True
                continue
                
        files = {
            'data_file': (os.path.split(file)[1], handle),
        }
        data = {
            'data_capturing_device': capture_device_url,
            'devices_captured': captured_devices_urls,
        }
        headers = {
            'Authorization': "Bearer " + self.token
        }
        response = requests.post(self.data_files_url, data=data, files=files, headers=headers)
        if response.status_code != 200:
            if response.status_code == 401 and not is_retry:
                # token may have expired, try to fetch another one
                self.get_new_token()
                self.upload_data_file(file, True)
            else:
                raise APIError("Failed to upload data file.  Response was: " + response.text)
        else:
            print("Successfully uploaded data file.  Response was: " + response.text)
        
try:
    uploader = IOTWebPlatformAPI(CLIENT_ID, CLIENT_SECRET)
    uploader.upload_data_file('test.pcap')
    #print(uploader.get_capture_devices())
except Exception as e:
    print(str(e))
