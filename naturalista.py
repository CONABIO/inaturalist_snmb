# coding=utf-8

import requests
import urllib
import json
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

# payload = [
#         {
#             "observation[species_guess]": "campyylorhynchus brunneicapillus",
#             "observation[observed_on_string]": "2015-11-23T06:00:00.000Z",
#             "observation[latitude]": 23.5254166666667,
#             "observation[longitude]": -110.048166666667,
#             "observation[place_guess]": "Baja California Sur, La Paz, SIERRA LA LAGUNA",
#             "observation[tag_list]": "conglomerado_muestra_id: 1055, conglomerado_nombre: 40429, archivo_camara_id: 191962, monitoreo_tipo: SAR-MOD",
#             "local_photos[0]": "./77594/2015_02/fotos_videos/Archivo_camara.baf6db1acc0687b5.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.a96ab84eac69a4ba.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.8e745d9a7b4b0dba.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.a02104734c2d2fd1.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.96c8374133bce9a7.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.b657d40d393f4a01.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.b16d465c08a5650b.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.aad3018a3ff09c0a.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.a9565cd592e588b1.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.b9dd87b772438b94.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.80ce123116f4562a.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.ace82d63f172081f.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.b09edf664521f88a.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.bab6ea99d49cd856.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.a4ca7b628317e9b5.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.aef7fda77e2c5549.JPG, ./77594/2015_02/fotos_videos/Archivo_camara.90ecd536b175abf5.JPG"
#         },
#        {
#             "observation[species_guess]": "Sylvilagus cunicularius",
#             "observation[observed_on_string]": "2014-08-19T05:00:00.000Z",
#             "observation[latitude]": 19.7361666666667,
#             "observation[longitude]": -103.092666666667,
#             "observation[place_guess]": "Jalisco, Tamazula",
#             "observation[tag_list]": "conglomerado_muestra_id: 256, conglomerado_nombre: 59000, archivo_camara_id: 304, monitoreo_tipo: SAC-MOD",
#             "local_photos[0]": "./100107/2016_03/referencias/Imagen_referencia_sitio.89b61caaf2b80a89.JPG"
#         }
#  ]

# Sending observations and photos to naturalista
for item in snmb_data["data"]:
#for item in payload:
  response = requests.post(("%s/observations.json" % site), item, headers=headers_observations)
  print response.content
  data = json.loads(response.content)
  observation_id = data[0]['id']
  payload2 = {"observation_photo[observation_id]" : observation_id}
  filename = item['local_photos[0]'].split(',')
# For many files
  if len(filename) > 1:
    for filename in filename:
      response = requests.post("%s/observation_photos.json" % site, data=payload2, files={'file': (os.path.basename(filename.strip()), open(filename.strip(), 'rb'), 'multipart/form-data')}, headers=headers_photo)
      print response.content
#      print filename.strip()
      print
#Just one file
  else:
    filename = item['local_photos[0]']
    response = requests.post("%s/observation_photos.json" % site, data=payload2, files={'file': (os.path.basename(filename.strip()), open(filename.strip(), 'rb'), 'multipart/form-data')}, headers=headers_photo)
    print response.content
#    print 'single file:'
#    print filename
    print
