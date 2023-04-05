import warnings
import datetime


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


if __name__ == '__main__':

    install_and_import('oracledb')
    install_and_import('requests')
    install_and_import('json')
    # Settings to ignore verification warnings
    warnings.filterwarnings('ignore')

    # Global variables for connection settings
    url = 'Insert your Octane URL'
    shared_space = 'Insert your space ID here'
    workspace = 'Insert your workspace ID here'
    client_id = "Insert your client ID here"
    client_secret = "Insert your client secret here"
    HeaderInfo = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}
    authentication = 'authentication/sign_in'
    payload = {"client_id": client_id, "client_secret": client_secret}
    db_address = "Insert your database address"

    # Authenticate
    resp = requests.post(url + '/' + authentication,
                         data=json.dumps(payload),
                         headers=HeaderInfo, verify=False)
    # Store cookies
    cookie = resp.cookies
    print('Login was successful with the status code: ' + str(resp.status_code))

    # Read all features
    resource = 'Insert your query parameters here'
    features = requests.get(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                            headers=HeaderInfo, cookies=cookie, verify=False)

    print('Getting features Status: ' + str(features.status_code))
    features_data = features.json()
    total_count = features_data['total_count']
    features_list = features_data['data']

    print('Total rows: ' + str(total_count))

    # Iterate through all features
    f_data = []
    for features in features_list:
        prio = 'None'
        regi = []
        try:
            for i in features['']['']:
                regi.append(str(i['']))
            regi = ', '.join(regi)
        except:
            regi = features['']['']

        if features[''] is not None:
            prio = str(features[''][''])

        # Store data in list
        f_data.append([features[''], features[''], features[''], features[''][''], regi, prio])

    # Insert data into database
    with oracledb.connect(db_address) as connection:
        with connection.cursor() as cursor:
            for i in f_data:
                crt_time = datetime.datetime.strptime(i[2], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y %H:%M:%S")
                cursor.execute("INSERT INTO <Insert Table Name> VALUES(:1, :2, :3, :4, :5, :6)",
                               [i[0], i[1], crt_time, i[3], i[4], i[5]])
            cursor.execute('commit')
    print("Data has been inserted into database!")
