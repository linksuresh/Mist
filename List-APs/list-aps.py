#!/usr/bin/env python3

"""
This script lists all the Mist AP devices associated to the specified Mist Org & Site.

Original python script written by Francois Verges @ SemFio
GitRepo : https://github.com/francoisverges/semfio-mist
"""

import time
import json
import requests


def main():
    # Org_id comes from : Mist UI > Organization > Settings > Org-id
    # site_id comes from : Mist UI > Organization > Select Site > Site-id
    # Token can be created by doing a Post at : https://api.mist.com/api/v1/self/apitokens
    org_id = 'Your-Org-ID'
    site_id = 'Your-Site-ID'
    token = 'Your-token'

    mist_url = 'https://api.mist.com/api/v1'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(token)}
    api_url = '{0}/sites/{1}/devices'.format(mist_url, site_id)

    # fetch the AP devices in the Site specified
    print ("\nFetching Devices from URL : {}\n".format(api_url))
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))
        # print (devices)

        print('--------------')
        for device in devices:
            print('AP Name        : {}'.format(device['name']))
            print('AP Model       : {}'.format(device['model']))
            print('AP MAC Address : {}'.format(device['mac']))
            print('--------------')
    else:
        print('--------------')
        print('Fetching APs failed ---> Error Code = {}, Error Text = {}'.format(response.status_code, response.text))
        print('--------------')


if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print("** Time to run: %s sec\n" % round(run_time, 2))
