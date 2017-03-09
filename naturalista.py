# coding=utf-8

import requests
import urllib, json
import os


site = "https://www.inaturalist.org"
app_id = 'f3f000ecc92eaa050f56cf35fe60469ebc634a6a86b48fad6f6b779fa4048c7e'
app_secret = '4ea9bb0b95763fee25e71d46154156cff1cbb3062fefd6d4e0f7faac9927318f'
username = 'snmb'
password = '000999000'

# Send a POST request to /oauth/token with the username and password
payload = {
  'client_id': app_id,
  'client_secret': app_secret,
  'grant_type': "password",
  'username': username,
  'password': password
}
#print "POST %s/oauth/token, payload: %s" % (site, payload)
response = requests.post(("%s/oauth/token" % site), payload)


# Store the token (access_token) in your app. You can now use it to make authorized
# requests on behalf of the user, like retrieving profile data:
token = response.json()["access_token"]
headers_observations = {"Content Type": "application/x-www-form-urlencoded; charset=utf-8","Authorization": "Bearer %s" % token}
headers_photo = {"Authorization": "Bearer %s" % token}


# Getting the information from SNMB database
url = "http://coati.conabio.gob.mx/api/v1/naturalista"
response = urllib.urlopen(url)
snmb_data = json.loads(response.read())

# Sending observations and photos to naturalista
for item in snmb_data["data"]:
    response = requests.post(("%s/observations.json" % site), item, headers=headers_observations)
    print response.content
    data = json.loads(response.content)
    observation_id = data[0]['id']
    filename = item['local_photos[0]']
    payload2 = {"observation_photo[observation_id]" : observation_id}
    response = requests.post("%s/observation_photos.json" % site, data=payload2, files={'file': (os.path.basename(filename), open(filename, 'rb'), 'multipart/form-data')}, headers=headers_photo)
    print response.content
    print '==================='
    print

