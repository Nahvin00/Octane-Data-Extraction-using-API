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
    install_and_import('warnings')
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
    db_address = ""

    # Authenticate
    resp = requests.post(url + '/' + authentication,
                         data=json.dumps(payload),
                         headers=HeaderInfo, verify=False)
    # Store cookies
    cookie = resp.cookies
    print('Login was successful with the status code: ' + str(resp.status_code))

    # Read all features
    resource = 'features?fields=creation_time,id,name,owner,priority,regions_sites_udf'
    features = requests.get(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                            headers=HeaderInfo, cookies=cookie, verify=False)

    print('Getting features Status: ' + str(features.status_code))
    features_data = features.json()
    total_count = features_data['total_count']
    features_list = features_data['data']

    print('Total features: ' + str(total_count))

    # Iterate through all features
    f_data = []
    for features in features_list:
        prio = 'None'
        regi = []
        for i in features['regions_sites_udf']['data']:
            regi.append(str(i['name']))
        regi = ', '.join(regi)
        if features['priority'] is not None:
            prio = str(features['priority']['name'])

        # Store data in list
        f_data.append([features['id'], features['name'], features['creation_time'], features['owner']['full_name'], regi, prio])

    # Insert data into database
    with oracledb.connect(db_address) as connection:
        with connection.cursor() as cursor:
            for i in f_data:
                cursor.execute("INSERT INTO AA_OCTANE_HIST VALUES(:1, :2, :3, :4, :5, :6)", [i[0], i[1], i[2], i[3], i[4], i[5]])
            cursor.execute('commit')
    print("Data has been inserted into database!")