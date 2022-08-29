from quicksnmp import *

import time
def get_full_info(ip: str):
    oids = ['.1.3.6.1.2.1.25.3.2.1.3.1','.1.3.6.1.2.1.1.3.0','.1.3.6.1.2.1.43.10.2.1.4.1.1','.1.3.6.1.2.1.43.11.1.1.9.1.1','.1.3.6.1.2.1.43.11.1.1.6.1.1',
           '.1.3.6.1.2.1.1.5.0']
    keys = ['model', 'uptime', 'pages', 'black_toner_left', 'black_toner_model', 'Device name']
    new_dict = {}
    try:
        raw_data = get(ip, oids, hlapi.CommunityData('public',mpModel=0))
        old_keys = list(raw_data.keys())
        for i in range(len(keys)):
            new_dict[keys[i]] = str(raw_data[old_keys[i]]).encode('iso-8859-1','ignore').decode('utf-8','ignore')
        return new_dict
    except:
        for key in keys:
            new_dict[key] = None

        return new_dict




if __name__ == "__main__":
    # -*- coding: utf-8 -*-
    import os
    import sys
    import codecs
    df = get_full_info('10.7.10.205')
    print(df['Device name'])