#!/usr/bin/env python3

"""
This script changes the AP name for the specified Mist AP (input AP's MAC & new name)

Original python script written by Francois Verges @ SemFio
GitRepo : https://github.com/francoisverges/semfio-mist
"""

from optparse import OptionParser
import time
import json
import requests

def main():
    '''
    This function changes the AP name for the selected AP (based on input MAC)
    '''
    usage = "Usage: %prog <AP_MAC_Address> <AP_New_Name>"
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()

    if len(args) == 2:
        ap_mac = args[0]
        ap_new_name = args[1]
    else:
        print('Wrong set of arguments! Please see usage below:\n\t{0}'.format(usage))
        return

    org_id = 'Your-Org-ID'
    site_id = 'Your-Site-ID'
    token = 'Your-token'
    mist_url = 'https://api.mist.com/api/v1'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token {}'.format(token)}

    # Retrieve the list of APs deployed at specified Site
    api_url = '{0}/sites/{1}/devices'.format(mist_url, site_id)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        devices = json.loads(response.content.decode('utf-8'))
        # print (devices)

        # Loop through the APs to until we find our AP's mac and update it's AP name
        for device in devices:
            if device['type'] == 'ap':
                if device['mac'] == ap_mac:
                    old_name = device['name']
                    device['name'] = ap_new_name
                    device_id = device['id']
                    data_put = json.dumps(device)

                    # Send POST request to update AP's name for selected AP
                    api_url = '{0}/sites/{1}/devices/{2}'.format(mist_url, site_id, device_id)
                    response = requests.put(api_url, data=data_put, headers=headers)

                    if response.status_code == 200:
                        print("\nAP named changed from '{1}' to '{2}' for MAC '{0}'".format(device['mac'],old_name,device['name']))
                    else:
                        print('\nAP name change failed ---> Error Code = {}, Error Text = {}'.format(response.status_code, response.text))
    else:
        print('Fetching list of APs failed ---> Error Code = {}, Error Text = {}'.format(response.status_code, response.text))


if __name__ == '__main__':
    start_time = time.time()
    main()
    run_time = time.time() - start_time
    print('--------------')
    print("** Time to run: %s sec\n" % round(run_time, 2))
