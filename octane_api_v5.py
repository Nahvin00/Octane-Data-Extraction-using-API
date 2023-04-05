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


if __name__ == '__main__':

    install_and_import('oracledb')
    install_and_import('requests')
    install_and_import('json')
    install_and_import('pandas')
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
    resource = 'features?fields=biz_benefit_eur_udf,ccb_approved_rejected_udf,ccb_comment_udf,cr_classification_udf,' \
               'cr_type_udf,deliverables_timeliness_udf,effort_in_hours_udf,go_live_date_udf,id,incident_no_udf,' \
               'it_owner_feature_udf,name,owner,phase,planned_for_ccb_udf,priority,application_modules,' \
               'project_operation_udf,quality_of_deliverables_udf,regions_sites_udf,release,release_remark_udf,' \
               'teamwork_evaluation_udf,uat_first_time_right_udf,update_document_udf'
    features = requests.get(url + '/api/shared_spaces/' + shared_id + '/workspaces/' + workspace_id + '/' + resource,
                            headers=HeaderInfo, cookies=cookie, verify=False)

    serv_prod = 'application_modules?fields=name,parent&order_by=id'
    serv_prod_res = requests.get(
        url + '/api/shared_spaces/' + shared_id + '/workspaces/' + workspace_id + '/' + serv_prod,
        headers=HeaderInfo, cookies=cookie, verify=False)

    print('Getting features Status: ' + str(features.status_code))
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
        id_ = features['id']
        phase = features['phase']['name']
        owner = features['owner']['full_name']
        it_owner_feature_udf = None
        if features['it_owner_feature_udf'] is not None:
            it_owner_feature_udf = features['it_owner_feature_udf']['full_name']
        regions_sites_udf = []
        try:
            for i in features['regions_sites_udf']['data']:
                regions_sites_udf.append(str(i['name']))
            regions_sites_udf = ', '.join(regions_sites_udf)
        except:
            regions_sites_udf = features['regions_sites_udf']['name']
        project_operation_udf = features['project_operation_udf']['name']
        project = features['name']
        cr_type_udf = features['cr_type_udf']['name']
        service_product = get_app_mod(proc_app_mod, features['product_areas']['data'][0]['name'])
        module = []
        for i in features['product_areas']['data']:
            module.append(str(i['name']))
        module = ', '.join(module)
        if module == service_product:
            module = None
        priority = None
        if features['priority'] is not None:
            priority = str(features['priority']['name'])
        incident_no_udf = features['incident_no_udf']
        cr_classification_udf = features['cr_classification_udf']['name']
        biz_benefit_eur_udf = features['biz_benefit_eur_udf']
        update_document_udf = []
        try:
            for i in features['update_document_udf']['data']:
                update_document_udf.append(str(i['name']))
            update_document_udf = ', '.join(update_document_udf)
        except:
            update_document_udf = None
        planned_for_ccb_udf = features['planned_for_ccb_udf']
        effort_in_hours_udf = features['effort_in_hours_udf']
        ccb_approved_rejected_udf = features['ccb_approved_rejected_udf']
        ccb_comment_udf = features['ccb_comment_udf']
        release = None
        if features['release'] is not None:
            release = str(features['release']['name'])
        # release = features['release']
        go_live_date_udf = features['go_live_date_udf']
        release_remark_udf = features['release_remark_udf']
        uat_first_time_right_udf = None
        if features['uat_first_time_right_udf'] is not None:
            uat_first_time_right_udf = features['uat_first_time_right_udf']['name']
        deliverables_timeliness_udf = None
        if features['uat_first_time_right_udf'] is not None:
            deliverables_timeliness_udf = features['deliverables_timeliness_udf']['name']
        quality_of_deliverables_udf = None
        if features['quality_of_deliverables_udf'] is not None:
            quality_of_deliverables_udf = features['quality_of_deliverables_udf']['name']
        teamwork_evaluation_udf = None
        if features['teamwork_evaluation_udf'] is not None:
            teamwork_evaluation_udf = features['teamwork_evaluation_udf']['name']

        # Store data in list
        f_data.append(
            [id_, shared_id, workspace_id, phase, owner, it_owner_feature_udf, regions_sites_udf, project_operation_udf,
             project, cr_type_udf, service_product, module, priority, incident_no_udf, cr_classification_udf,
             biz_benefit_eur_udf, update_document_udf, planned_for_ccb_udf, effort_in_hours_udf,
             ccb_approved_rejected_udf, ccb_comment_udf, release, go_live_date_udf, release_remark_udf,
             uat_first_time_right_udf, deliverables_timeliness_udf, quality_of_deliverables_udf,
             teamwork_evaluation_udf])

    df = pandas.DataFrame(f_data)
    df.columns = ['id_', 'shared_id', 'workspace_id', 'phase', 'owner', 'it_owner_feature_udf', 'regions_sites_udf',
                  'project_operation_udf', 'project', 'cr_type_udf', 'service_product', 'module', 'priority',
                  'incident_no_udf', 'cr_classification_udf', 'biz_benefit_eur_udf', 'update_document_udf',
                  'planned_for_ccb_udf', 'effort_in_hours_udf', 'ccb_approved_rejected_udf', 'ccb_comment_udf',
                  'release', 'go_live_date_udf', 'release_remark_udf', 'uat_first_time_right_udf',
                  'deliverables_timeliness_udf', 'quality_of_deliverables_udf', 'teamwork_evaluation_udf']
    pandas.set_option('display.max_rows', 500)
    pandas.set_option('display.max_columns', 500)
    pandas.set_option('display.width', 1000)
    print(df)

    # Insert data into database

    with oracledb.connect(db_address) as connection:
        with connection.cursor() as cursor:
            for i in f_data:
                time_0 = datetime.datetime.strptime(i[17], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y %H:%M:%S") if i[17] is not None else None
                time_1 = datetime.datetime.strptime(i[19], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y %H:%M:%S") if i[19] is not None else None
                time_2 = datetime.datetime.strptime(i[22], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y %H:%M:%S") if i[22] is not None else None
                cursor.execute("INSERT INTO AA_OCTANE_HIST VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27, :28)",
                               [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16], time_0, i[18], time_1, i[20], i[21], time_2, i[23], i[24], i[25], i[26], i[27]])
            cursor.execute('commit')
    print("Data has been inserted into database!")
