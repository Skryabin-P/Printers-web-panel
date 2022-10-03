from quicksnmp import *
import time
def get_full_info(ip: str):

    oids = ['.1.3.6.1.2.1.25.3.2.1.3.1','.1.3.6.1.2.1.1.3.0','.1.3.6.1.2.1.43.10.2.1.4.1.1','.1.3.6.1.2.1.43.11.1.1.9.1.1','.1.3.6.1.2.1.43.11.1.1.6.1.1',
               '.1.3.6.1.2.1.1.5.0']
    keys = ['model', 'uptime', 'pages', 'black_toner_left', 'black_toner_model', 'Device name']
    new_dict = {}
    # if printer doesn't response set all fields as None
    try:
        raw_data = get(ip, oids, hlapi.CommunityData('public',mpModel=0))
        old_keys = list(raw_data.keys())
        for i in range(len(keys)):
            # because it works on windows server i had to change encoding
            new_dict[keys[i]] = str(raw_data[old_keys[i]]).encode('iso-8859-1','ignore').decode('utf-8','ignore')

        return new_dict
    except:
        for key in keys:
            new_dict[key] = None

        return new_dict




if __name__ == "__main__":
    # commented code. I just looked for printers in our network subnets and save it to excel
    # so I  can easy add them in admin dashboard

    import xlwt
    ip_list = ['10.13.10.22']
    for ip in ip_list:
        print(ip)
        print(get_full_info(ip))
        print('-------------------')
    # networks = ['192.168.61','10.12.2','10.13.10','10.14.10','10.15.2','10.16.2',
    #             '10.17.10','192.168.144','10.7.10','192.168.20',
    #             '10.169.2','192.168.160','10.171.0','192.168.50','10.10.0']
    # printers = []
    # keys = list(get_full_info('192.168.128.19').keys())
    # keys.append('IP')
    # start = time.time()
    # print(start)
    #
    # for net in networks:
    #     printers = []
    #     wb = xlwt.Workbook(encoding='utf-8')
    #     ws = wb.add_sheet('Report')
    #     print(f'Network is {net}')
    #     start1 = time.time()
    #     for i in range(1, 256):
    #         ip = f"{net}.{i}"
    #         print(ip)
    #         data = get_full_info(ip)
    #         print(data['model'])
    #         if data['model'] != None:
    #             data['IP'] = ip
    #             printers.append(data)
    #     row_num = 0
    #     for col in range(len(keys)):
    #         ws.write(row_num, col, keys[col])
    #         ws.col(col).width = 256 * 32
    #     for row in printers:
    #         row_num += 1
    #         for col in range(len(keys)):
    #             ws.write(row_num, col, row[keys[col]])
    #     wb.save(f'printers_{net}.xls')
    #     print(f'Затрачено на подсеть : {time.time()-start1} секунд')

    import csv


    # keys = list(printers[0].keys())
    # print(keys)
    # row_num = 0
    # for col in range(len(keys)):
    #     ws.write(row_num, col, keys[col])
    #     ws.col(col).width = 256 * 32
    # for row in printers:
    #     row_num += 1
    #     for col in range(len(keys)):
    #         ws.write(row_num, col, row[keys[col]])
    # wb.save('printers.xls')
    # print(f'Время исполнения: {time.time() - start} секунды')




