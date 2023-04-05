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


def app_mod_path(temp):
    new = []
    for i in temp:
        if i[1] == 'Application Modules':
            cc = [i[0]]
            new.append(cc)
    for i in temp:
        for c, j in enumerate(new):
            for x in j:
                if x == i[1]:
                    cc = new[c]
                    cc.append(i[0])
                    new[c] = cc
    return new


def get_app_mod(new, x):
    for i in new:
        for j in i:
            if j == x:
                return i[0]


def main_proc(shared_id, workspace_id, client_id, client_secret, db_last_modified, oracle_connection):
    url = ''
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
    resource = 'features?fields=biz_benefit_eur_udf,ccb_approved_rejected_udf,ccb_comment_udf,cr_classification_udf,' \
               'cr_type_udf,deliverables_timeliness_udf,effort_in_hours_udf,go_live_date_udf,id,incident_no_udf,' \
               'it_owner_feature_udf,name,owner,phase,planned_for_ccb_udf,priority,application_modules,' \
               'project_operation_udf,quality_of_deliverables_udf,regions_sites_udf,release,release_remark_udf,' \
               'teamwork_evaluation_udf,uat_first_time_right_udf,update_document_udf,last_modified'
    query = '&query="last_modified%20GT%20^' + db_last_modified + '^"'
    features = requests.get(url + '/api/shared_spaces/' + shared_id + '/workspaces/' + workspace_id + '/' + resource +
                            query, headers=HeaderInfo, cookies=cookie, verify=False)
    print('Getting features Status: ' + str(features.status_code))
    api_attempts = 2
    upd_resource = resource
    while api_attempts > 0 and features.status_code == 400:
        err_field = features.json()['properties']['field_name'].split(',')
        print("Error: ", err_field)
        for i in err_field:
            if i == 'effort_in_hours_udf' and api_attempts == 2:
                upd_resource = upd_resource.replace('effort_in_hours_udf', 'effort_estimation_udf')
            else:
                upd_resource = upd_resource.replace(i + ',', '')
        features = requests.get(
            url + '/api/shared_spaces/' + shared_id + '/workspaces/' + workspace_id + '/' + upd_resource + query,
            headers=HeaderInfo, cookies=cookie, verify=False)
        print('Getting features Status: ' + str(features.status_code))
        api_attempts = api_attempts - 1
    if features.status_code == 200 and features.json()['total_count'] == 0:
        print("No new features!\n")
        return
    serv_prod = 'application_modules?fields=name,parent&order_by=id'
    serv_prod_res = requests.get(
        url + '/api/shared_spaces/' + shared_id + '/workspaces/' + workspace_id + '/' + serv_prod,
        headers=HeaderInfo, cookies=cookie, verify=False)

    print('Getting service product Status: ' + str(serv_prod_res.status_code))
    features_data = features.json()
    total_count = features_data['total_count']
    features_list = features_data['data']

    serv_prod_data = serv_prod_res.json()['data']
    app_mod = []
    for i in serv_prod_data:
        try:
            app_mod.append([i['name'], i['parent']['name']])
        except:
            app_mod.append([i['name'], i['parent']])
    proc_app_mod = app_mod_path(app_mod)

    print('Total features: ' + str(total_count))

    # Iterate through all features
    f_data = []
    for features in features_list:
        error_comment = ""
        id_ = features['id']
        phase = features['phase']['name']
        owner = features['owner']['full_name']
        try:
            if features['it_owner_feature_udf'] is not None:
                it_owner_feature_udf = features['it_owner_feature_udf']['full_name']
        except:
            it_owner_feature_udf = None
        try:
            regions_sites_udf = []
            for i in features['regions_sites_udf']['data']:
                regions_sites_udf.append(str(i['name']))
            regions_sites_udf = ', '.join(regions_sites_udf)
        except:
            try:
                regions_sites_udf = features['regions_sites_udf']['name']
            except:
                regions_sites_udf = None
        try:
            project_operation_udf = features['project_operation_udf']['name']
        except:
            project_operation_udf = None
        project = features['name']
        cr_type_udf = features['cr_type_udf']['name']
        try:
            service_product = get_app_mod(proc_app_mod, features['product_areas']['data'][0]['name'])
            serv_prod_count = features['product_areas']['total_count']
            serv_prod_lst = []
            if serv_prod_count > 1:
                for elem in range(serv_prod_count):
                    serv_prod_par = get_app_mod(proc_app_mod, features['product_areas']['data'][elem]['name'])
                    if len(serv_prod_lst) == 0:
                        serv_prod_lst.append(serv_prod_par)
                    elif serv_prod_par != serv_prod_lst[-1]:
                        serv_prod_lst.append(serv_prod_par)
                if len(serv_prod_lst) > 1:
                    error_comment = error_comment + "Modules from different service products have been selected."
        except:
            try:
                service_product = get_app_mod(proc_app_mod, features['product_areas']['data']['name'])
            except:
                service_product = None
        module = []
        for i in features['product_areas']['data']:
            module.append(str(i['name']))
        module = ', '.join(module)
        if module == service_product or service_product is None:
            module = None
        priority = None
        if features['priority'] is not None:
            priority = str(features['priority']['name'])
        incident_no_udf = features['incident_no_udf']
        try:
            cr_classification_udf = features['cr_classification_udf']['name']
        except:
            cr_classification_udf = None
        try:
            biz_benefit_eur_udf = features['biz_benefit_eur_udf']
        except:
            biz_benefit_eur_udf = None
        try:
            update_document_udf = []
            for i in features['update_document_udf']['data']:
                update_document_udf.append(str(i['name']))
            update_document_udf = ', '.join(update_document_udf)
        except:
            update_document_udf = None
        try:
            planned_for_ccb_udf = features['planned_for_ccb_udf']
        except:
            planned_for_ccb_udf = None
        try:
            effort_in_hours_udf = features['effort_in_hours_udf']
        except:
            try:
                effort_in_hours_udf = features['effort_estimation_udf']
                if effort_in_hours_udf is not None:
                    effort_in_days = effort_in_hours_udf.split()
                    if effort_in_days[1] == 'day' or effort_in_days[1] == 'days':
                        effort_in_hours_udf = str(int(effort_in_days[0]) * 24)
                    elif effort_in_days[1] == 'hour' or effort_in_days[1] == 'hours':
                        effort_in_hours_udf = effort_in_days[0]
            except:
                effort_in_hours_udf = None
        try:
            ccb_approved_rejected_udf = features['ccb_approved_rejected_udf']
        except:
            ccb_approved_rejected_udf = None
        try:
            ccb_comment_udf = features['ccb_comment_udf']
        except:
            ccb_comment_udf = None
        release = None
        if features['release'] is not None:
            release = str(features['release']['name'])
        go_live_date_udf = features['go_live_date_udf']
        try:
            release_remark_udf = features['release_remark_udf']
        except:
            release_remark_udf = None
        try:
            uat_first_time_right_udf = features['uat_first_time_right_udf']['name']
        except:
            uat_first_time_right_udf = None
        try:
            deliverables_timeliness_udf = features['deliverables_timeliness_udf']['name']
        except:
            deliverables_timeliness_udf = None
        try:
            quality_of_deliverables_udf = features['quality_of_deliverables_udf']['name']
        except:
            quality_of_deliverables_udf = None
        try:
            teamwork_evaluation_udf = features['teamwork_evaluation_udf']['name']
        except:
            teamwork_evaluation_udf = None
        last_modified = features['last_modified']
        if error_comment == "":
            error_comment = None
        # Store data in list
        f_data.append(
            [id_, shared_id, workspace_id, phase, owner, it_owner_feature_udf, regions_sites_udf, project_operation_udf,
             project, cr_type_udf, service_product, module, priority, incident_no_udf, cr_classification_udf,
             biz_benefit_eur_udf, update_document_udf, planned_for_ccb_udf, effort_in_hours_udf,
             ccb_approved_rejected_udf, ccb_comment_udf, release, go_live_date_udf, release_remark_udf,
             uat_first_time_right_udf, deliverables_timeliness_udf, quality_of_deliverables_udf,
             teamwork_evaluation_udf, last_modified, error_comment])

    df = pandas.DataFrame(f_data)
    df.columns = ['id_', 'shared_id', 'workspace_id', 'phase', 'owner', 'it_owner_feature_udf', 'regions_sites_udf',
                  'project_operation_udf', 'project', 'cr_type_udf', 'service_product', 'module', 'priority',
                  'incident_no_udf', 'cr_classification_udf', 'biz_benefit_eur_udf', 'update_document_udf',
                  'planned_for_ccb_udf', 'effort_in_hours_udf', 'ccb_approved_rejected_udf', 'ccb_comment_udf',
                  'release', 'go_live_date_udf', 'release_remark_udf', 'uat_first_time_right_udf',
                  'deliverables_timeliness_udf', 'quality_of_deliverables_udf', 'teamwork_evaluation_udf',
                  'last_modified', 'error_comment']
    pandas.set_option('display.max_rows', 500)
    pandas.set_option('display.max_columns', 500)
    pandas.set_option('display.width', 1000)
    print(df)

    # Insert data into database

    with oracledb.connect(oracle_connection) as connection:
        with connection.cursor() as cursor:
            for i in f_data:
                time_0 = datetime.datetime.strptime(i[17], "%Y-%m-%dT%H:%M:%SZ") \
                    .strftime("%d/%m/%Y %H:%M:%S") if i[17] is not None else None
                time_1 = datetime.datetime.strptime(i[19], "%Y-%m-%dT%H:%M:%SZ") \
                    .strftime("%d/%m/%Y %H:%M:%S") if i[19] is not None else None
                time_2 = datetime.datetime.strptime(i[22], "%Y-%m-%dT%H:%M:%SZ") \
                    .strftime("%d/%m/%Y %H:%M:%S") if i[22] is not None else None
                time_3 = datetime.datetime.strptime(i[28], "%Y-%m-%dT%H:%M:%SZ") \
                    .strftime("%d/%m/%Y %H:%M:%S") if i[28] is not None else None
                try:
                    cursor.execute("INSERT INTO AA_OCTANE_HIST VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12,"
                               ":13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, "
                               ":30)",
                               [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13],
                                i[14], i[15], i[16], time_0, i[18], time_1, i[20], i[21], time_2, i[23], i[24], i[25],
                                i[26], i[27], time_3, i[29]])
                    cursor.execute('commit')
                except:
                    cursor.execute("DELETE FROM AA_OCTANE_HIST WHERE FEATURE_ID :1", [i[0]])
                    cursor.execute(
                        "INSERT INTO AA_OCTANE_HIST VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12,"
                        ":13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28, :29, "
                        ":30)",
                        [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13],
                         i[14], i[15], i[16], time_0, i[18], time_1, i[20], i[21], time_2, i[23], i[24], i[25],
                         i[26], i[27], time_3, i[29]])
                    cursor.execute('commit')
    print("Data has been inserted into database!\n")


if __name__ == '__main__':

    install_and_import('cryptography')
    from cryptography.fernet import Fernet
    install_and_import('oracledb')
    install_and_import('requests')
    install_and_import('json')
    install_and_import('pandas')
    # Settings to ignore verification warnings
    warnings.filterwarnings('ignore')

    # Global variables for connection settings
    encrypted_oracle_connection = "gAAAAABj029aKs1wjsHluT7hktSraW3J0XJq6HamM8YzhJXA51Va11g4Ipq_aMgcQ1gFVV80FZU02ljG" \
                                  "4yGG8strSJnM8jqoWI7WeNF4VG8s0OV_iNUy3CdXHmysBaic4sh0KSH7vGu7aMz8JeTOyIYncIFGbU6tbw=="
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    # using the generated key
    fernet = Fernet(key)
    oracle_connection = fernet.decrypt(encrypted_oracle_connection).decode()

    db_ = []
    with oracledb.connect(oracle_connection) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM AA_OCTANE_DB")
            for i in cursor:
                with connection.cursor() as cursor_2:
                    try:
                        cursor_2.execute("SELECT MAX(LAST_MODIFIED) FROM AA_OCTANE_HIST WHERE SPACE_ID = :1", [i[0]])
                        for j in cursor_2:
                            db_last_modified = str(j[0].strftime("%Y-%m-%dT%H:%M:%SZ"))
                    except:
                        db_last_modified = "2000-01-01T00:00:00Z"
                db_.append(i + (db_last_modified,))
    x = 0
    for i in db_:
        if x < 5:
            print('Currently processing workspace', i[4])
            main_proc(str(i[0]), i[1], i[2], i[3], i[5], oracle_connection)
        x += 1