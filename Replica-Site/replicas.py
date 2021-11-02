#!/usr/bin/env python3

"""
This script CLONES an existing SITE from current ORG to the NEW ORG
- All the config details are read from 'replicas.json' file.

"""

import time
import json
import requests

def read_current_site_info(configs):
    api_url = '{0}/sites/{1}'.format(configs['mist_url'], configs['current_org_site']['site_id'])
    print (api_url)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['current_org_site']['token'])}

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        assert False, 'Fetching Site info failed ---> Error Code = {}, Error Text = {}'.format(response.status_code, response.text)

    site_info = json.loads(response.content.decode('utf-8'))
    # print(json.dumps(site_settings, indent=4, sort_keys=True))
    with open('replicas_current_site_info.json', 'w') as fp:
        json.dump(site_info, fp, indent=4)
    return site_info


def create_new_site(configs):
    """
    This function creates a new Site based on the information located in configs
    API Call Used: POST https://api.mist.com/api/v1/orgs/:org_id/sites
    Parameters:
        - configs: Dictionary containing all configurations information
    Returns:
        - The ID of the newly created site
    """

    current_site_info = read_current_site_info(configs)
    mist_site = {}
    mist_site['name'] = current_site_info['name']
    mist_site['timezone'] = current_site_info['timezone']
    mist_site['country_code'] = current_site_info['country_code']
    mist_site['address'] = current_site_info['address']
    mist_site['latlng'] = {'lat': current_site_info['lat'], 'lng': current_site_info['lng']}
    
    data_post = json.dumps(mist_site)
    # print (data_post)

    api_url = '{0}/orgs/{1}/sites'.format(configs['mist_url'], configs['new_org_site']['org_id'])
    # print (api_url)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['new_org_site']['token'])}

    response = requests.post(api_url, data=data_post, headers=headers)

    if response.status_code != 200:
        assert False, "Creating Site '{}' failed ---> Error Code = {}, Error Text = {}".format(mist_site['name'],
                                                                                       response.status_code,
                                                                                       response.text)
    new_site = json.loads(response.content.decode('utf-8'))
    print (json.dumps(new_site, indent=4, sort_keys=True))
    print('\n\n{0} site was created.\t\t\t\tSITE ID={1}'.format(new_site['name'], new_site['id']))
    return new_site['id']


def read_current_site_settings(configs):
    api_url = '{0}/sites/{1}/setting'.format(configs['mist_url'], configs['current_org_site']['site_id'])
    print (api_url)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['current_org_site']['token'])}

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        assert False, 'Fetching Site settings failed ---> Error Code = {}, Error Text = {}'.format(response.status_code, response.text)

    site_settings = json.loads(response.content.decode('utf-8'))
    # print(json.dumps(site_settings, indent=4, sort_keys=True))
    with open('replicas_current_site_settings.json', 'w') as fp:
        json.dump(site_settings, fp, indent=4)
    return site_settings


def update_settings_for_new_site(configs, current_site_settings, new_site_id):
    api_url = '{0}/sites/{1}/setting'.format(configs['mist_url'], new_site_id)
    print (api_url)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['new_org_site']['token'])}

    response = requests.put(api_url, data=json.dumps(current_site_settings), headers=headers)
    if response.status_code != 200:
        assert False, 'Updating Site settings failed ---> Error Code = {}, Error Text = {}'.format(response.status_code, response.text)

    site_settings = json.loads(response.content.decode('utf-8'))
    # print(json.dumps(site_settings, indent=4, sort_keys=True))
    with open('replicas_new_site_settings.json', 'w') as fp:
        json.dump(site_settings, fp, indent=4)
    return site_settings



def main():
    """
    This function parses the config-file passed and creates a Mist Site within your organization
    """
    print ("\n\nReading config file ===> ")
    with open('replicas.json') as jf:
        configs = json.load(jf)
    # print (configs)

    # read the site settings for your current org
    print("\n\nReading Current Site settings ===> ")
    current_site_settings = read_current_site_settings(configs)

    # create a site in the New org
    print("\n\nCreate New Site ===> ")
    new_site_id = create_new_site(configs)

    # update your current site (new-site-id) w/ settings
    print("\n\nUpdate New Site settings ===> ")
    new_site_settings = update_settings_for_new_site(configs, current_site_settings, new_site_id)
    return


if __name__ == '__main__':
    start_time = time.time()
    print('** Creating a Replica Site')
    print('--------------\n')
    main()
    run_time = time.time() - start_time
    print("")
    print('--------------\n')
    print("** Time to run: %s sec" % round(run_time, 2))
