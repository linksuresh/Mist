#!/usr/bin/env python3

"""
This script creates a single New Site within your Mist Organization.
- All the config details are read from 'create_site.json' file.

Original python script written by Francois Verges @ SemFio
GitRepo : https://github.com/francoisverges/semfio-mist
"""

import argparse
import time
import json
import requests


def create_new_site(configs):
    """
    This function creates a new Site based on the information located in configs
    API Call Used: POST https://api.mist.com/api/v1/orgs/:org_id/sites
    Parameters:
        - configs: Dictionary containing all configurations information
    Returns:
        - The ID of the newly created site
    """
    mist_site = {}
    mist_site['name'] = configs['site']['name']
    mist_site['timezone'] = configs['site']['timezone']
    mist_site['country_code'] = configs['site']['country_code']
    mist_site['address'] = configs['site']['address']
    mist_site['latlng'] = {'lat': configs['site']['lat'], 'lng': configs['site']['lng']}

    data_post = json.dumps(mist_site)

    api_url = '{0}/orgs/{1}/sites'.format(configs['api']['mist_url'], configs['api']['org_id'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['api']['token'])}

    response = requests.post(api_url, data=data_post, headers=headers)

    if response.status_code == 200:
        new_site = json.loads(response.content.decode('utf-8'))
        print (json.dumps(new_site, indent=4, sort_keys=True))
        print('\n\n{0} site was created.\t\t\t\tSITE ID={1}'.format(new_site['name'], new_site['id']))
    else:
        print("Creating Site '{}' failed ---> Error Code = {}, Error Text = {}".format(mist_site['name'], response.status_code, response.text))
    return


def main():
    """
    This function parses the config-file passed and creates a Mist Site within your organization
    """
    parser = argparse.ArgumentParser(description='Creates a Mist site within your organization')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType('r'),
                        help='file containing all the configuration information')
    args = parser.parse_args()

    configs = json.load(args.config)

    create_new_site(configs)
    return


if __name__ == '__main__':
    start_time = time.time()
    print('** Creating a Mist Site')
    print('--------------\n')
    main()
    run_time = time.time() - start_time
    print("")
    print('--------------\n')
    print("** Time to run: %s sec" % round(run_time, 2))
