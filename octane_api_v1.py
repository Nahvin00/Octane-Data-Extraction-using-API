import requests
import json
import warnings

# Settings to ignore verification warnings
warnings.filterwarnings('ignore')

# Global variables for connection settings
url = ''
shared_space = ''
workspace = ''
client_id = ""
client_secret = ""
HeaderInfo = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}
authentication = 'authentication/sign_in'
payload = {"client_id": client_id, "client_secret": client_secret}

# Authenticate
resp = requests.post(url + '/' + authentication,
                     data=json.dumps(payload),
                     headers=HeaderInfo, verify=False)
# Store cookies
cookie = resp.cookies
print('Login was successful with the status code: ' + str(resp.status_code))

# Read all features
resource = 'features'
features = requests.get(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                        headers=HeaderInfo, cookies=cookie, verify=False)

print('Getting features Status: ' + str(features.status_code))
features_data = features.json()
total_count = features_data['total_count']
features_list = features_data['data']

print('Total features: ' + str(total_count))

# Iterate through all features
print('Features Summary:')
for features in features_list:
    print('ID: ' + features['id'])
