import requests
import urllib, json

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
headers = {"Authorization": "Bearer %s" % token}
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
url = "http://coati.conabio.gob.mx/api/v1/naturalista"
response = urllib.urlopen(url)
snmb_data = json.loads(response.read())
#print snmb_data

#TODO: add the file using multipart/jpeg file
payload = [{
'observation[species_guess]' : 'Odocoileus virginianus',
'observation[taxon_id]' : 0,
'observation[id_please]' : '0',
'observation[observed_on_string]' : '2016-07-08',
'observation[time_zone]' : 'Mexico City ',
'observation[description]' : 'Prueba de EOMA 1',
'observation[tag_list]' : 'foo,bar',
'observation[place_guess]' : 'Tamaulipas',
'observation[latitude]' : '24.9318454',
'observation[longitude]' : '-100.8891331',
'observation[map_scale]' : '11',
'observation[location_is_exact]' : 'false',
'observation[positional_accuracy]' : '7798',
'observation[geoprivacy]' : 'obscured'
},
{
'observation[species_guess]' : 'Mimus gilvus',
'observation[taxon_id]' : 0,
'observation[id_please]' : '0',
'observation[observed_on_string]' : '2016-07-08',
'observation[time_zone]' : 'Mexico City ',
'observation[description]' : 'Prueba de EOMA 2',
'observation[tag_list]' : 'SAC-MOD',
'observation[place_guess]' : 'Tamaulipas',
'observation[latitude]' : '24.9318454',
'observation[longitude]' : '-100.8891331',
'observation[map_scale]' : '11',
'observation[location_is_exact]' : 'false',
'observation[positional_accuracy]' : '7798',
'observation[geoprivacy]' : 'obscured'
}
]
# TESTING
#response = requests.post(("%s/observations.json" % site), payload[1], headers=headers)
#print response.content

for item in snmb_data["data"]:
    print item
    #response = requests.post(("%s/observations.json" % site), item, headers=headers)
    #print response.content
    #print
