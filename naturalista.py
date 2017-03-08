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
#print "RESPONSE"
#print response.content
#print
# response will be a chunk of JSON looking like
# {
#   "access_token":"xxx",
#   "token_type":"bearer",
#   "expires_in":null,
#   "refresh_token":null,
#   "scope":"write"
# }

# Store the token (access_token) in your app. You can now use it to make authorized
# requests on behalf of the user, like retrieving profile data:
token = response.json()["access_token"]
headers_observations = {"Content Type": "application/x-www-form-urlencoded","Authorization": "Bearer %s" % token}
headers_photo = {"Authorization": "Bearer %s" % token}
#print "GET %s/users/edit.json, headers: %s" % (site, headers)
#print "RESPONSE"
#print requests.get(("%s/users/edit.json" % site), headers=headers).content
#print requests.get(("%s/observations/5154583.json" % site), headers=headers).content
#print

############
#
# Appending data into Naturalist account
#
############

#Getting the information from SNMB database
#url = "http://coati.conabio.gob.mx/api/v1/naturalista"
#response = urllib.urlopen(url)
#snmb_data = json.loads(response.read())
#print snmb_data

payload = [
       {
            "observation[species_guess]": "Sylvilagus cunicularius",
            "observation[observed_on_string]": "2014-08-19T05:00:00.000Z",
            "observation[latitude]": 19.7361666666667,
            "observation[longitude]": -103.092666666667,
            "observation[place_guess]": "Jalisco, Tamazula",
            "observation[tag_list]": "conglomerado_muestra_id: 256, conglomerado_nombre: 59000, archivo_camara_id: 304, monitoreo_tipo: SAC-MOD",
            "local_photos[0]": "./132145/2015_09/fotos_videos/Archivo_camara.acb3860a43ead0dc.JPG"
        },
        {
            "observation[species_guess]": "campyylorhynchus brunneicapillus",
            "observation[observed_on_string]": "2015-11-23T06:00:00.000Z",
            "observation[latitude]": 23.5254166666667,
            "observation[longitude]": -110.048166666667,
            "observation[place_guess]": "Baja California Sur, La Paz, SIERRA LA LAGUNA",
            "observation[tag_list]": "conglomerado_muestra_id: 1055, conglomerado_nombre: 40429, archivo_camara_id: 191962, monitoreo_tipo: SAR-MOD",
            "local_photos[0]": "./40429/2015_11/fotos_videos/Archivo_camara.831eb8a44cf4bb80.JPG"
        }
]

#for item in snmb_data["data"]:
for item in payload:
    response = requests.post(("%s/observations.json" % site), item, headers=headers_observations)
    print '==================='
    print response.content
    data = json.loads(response.content)
    observation_id = data[0]['id']
    location_file = './'
    filename = location_file + item['local_photos[0]']
    payload2 = {"observation_photo[observation_id]" : observation_id}
    response = requests.post("%s/observation_photos.json" % site, data=payload2, files={'file': (os.path.basename(filename), open(filename, 'rb'), 'multipart/form-data')}, headers=headers_photo)
    print response.content
    print '==================='
    print
    print filename
