#!/usr/bin/env python3

"""
This batch script creates New Site within your Mist Organization.
- Each Site information is read from 'create_site.csv' file
- Org/Token/API config internals is read from 'create_site.json' file.

Original python script written by Francois Verges @ SemFio
GitRepo : https://github.com/francoisverges/semfio-mist
"""

import argparse
import time
import json
import requests
import csv

def create_new_site(configs, mist_site):
    '''
    This function creates a Site within your Mist org
    API Call Used: POST https://api.mist.com/api/v1/orgs/:org_id/sites
    Parameters:
        - configs: Dictionary containing all configurations information
    Returns:
        - The ID of the newly created site
    '''
    print('\n\nCreating a Mist Site : {}'.format(mist_site['name']))
    print('=======================================================\n')

    data_post = json.dumps(mist_site)

    api_url = '{0}/orgs/{1}/sites'.format(configs['api']['mist_url'], configs['api']['org_id'])
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Token {}'.format(configs['api']['token'])}

    response = requests.post(api_url, data=data_post, headers=headers)

    if response.status_code == 200:
        new_site = json.loads(response.content.decode('utf-8'))
        print (json.dumps(new_site, indent=4, sort_keys=True))
        print('\n\n======> {0} site was created.\t\tSITE ID={1}\n\n'.format(new_site['name'], new_site['id']))
        # return (new_site['id'])
    else:
        print('======> Something went wrong ---> Error Code = {}, Error Text = {}\n\n'.format(response.status_code, response.text))
    return


def main():
    # read Org/Token/API config internals from JSON file : 'create_site.json'
    parser = argparse.ArgumentParser(description='Creates a Mist site within your organization')
    parser.add_argument('config', metavar='config_file', type=argparse.FileType('r'),
                        help='file containing all the configuration information')
    args = parser.parse_args()

    configs = json.load(args.config)

    # Read every Site & its parameters from CSV file 'create_site.csv'
    # and call function create_new_site() to Create the site.
    with open('create_site.csv', 'r') as file:
        flag_skip_header = True
        for site in csv.reader(file, quotechar='"', delimiter=',',
                            quoting=csv.QUOTE_ALL, skipinitialspace=True):
            if flag_skip_header:
                flag_skip_header = False
                continue
            print("\n*** Read from CSV ==> {} ***".format(site))
            mist_site = {}
            mist_site['name'] = site[0]
            mist_site['timezone'] = site[1]
            mist_site['country_code'] = site[2]
            mist_site['address'] = site[3]
            mist_site['latlng'] = {'lat': site[4], 'lng': site[5]}
            # print (mist_site)

            create_new_site(configs, mist_site)

    return


if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print("\n** Time to run: %s sec\n" % round(run_time, 2))
