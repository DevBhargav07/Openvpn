from collections import deque
# from concurrent.futures import ThreadPoolExecutor
# import concurrent.futures
import sys
import os
# import threading


def order_container(ds):
    if len(ds) > 1:
        ds = sorted(ds,key=lambda x: tuple(map(int,x.split('.'))))
        return ds[1]
    else:
        return d[0]

def update_last_ip_file(ip):
    dq = deque([])
    last_ip_file_path = '/etc/openvpn/server/last_ip'
    with open(last_ip_file_path,mode='r+') as last_file:
        file_read = last_file.readline()
        if file_read:
            dq.append(file_read)
            dq.append(ip)
            res = order_container(dq)
            last_file.seek(0)
            last_file.truncate(0)
            last_file.write(f"{res}\n")
        else:
            last_file.seek(0)
            last_file.truncate(0)
            last_file.write(f"{ip}\n")


def update_pool_org(email,from_ip,to_ip):
    pool_ip_list = f'/etc/openvpn/hub_clients/{email}'
    with open(pool_ip_list,mode='w') as pool_file:
        pool_file.write(f'{from_ip},{to_ip}\n')

def create_a_pool(last_ip,email):
    one, two, three, four = last_ip.split('.')
    pool_ip = ''
    if int(three) < 255:
        if int(three) == 0 and int(four) == 0:
            starting_ip = f'{one}.{two}.{three}.{1}'
            ending_ip = f'{one}.{two}.{three}.{254}'
            update_last_ip_file(ending_ip)
            update_pool_org(email,starting_ip,ending_ip)
            pool_ip = f"{starting_ip},{ending_ip}"
        else:
            starting_ip = f'{one}.{two}.{int(three)+1}.{1}'
            ending_ip = f'{one}.{two}.{int(three)+1}.{254}'
            update_last_ip_file(ending_ip)
            update_pool_org(email,starting_ip,ending_ip)
            pool_ip = f"{starting_ip},{ending_ip}"
    else:
        if int(two) != 9:
            starting_ip = f'{one}.{int(two)+1}.{0}.{1}'
            ending_ip = f'{one}.{int(two)+1}.{0}.{254}'
            update_last_ip_file(ending_ip)
            update_pool_org(email,starting_ip,ending_ip)
            pool_ip = f"{starting_ip},{ending_ip}"
        else:
            print('1')
            #all fields are filled
    print(pool_ip)

def main(email):
    last_ip = ''
    last_ip_file_path = '/etc/openvpn/server/last_ip'
    if os.path.exists(last_ip_file_path):
        with open(last_ip_file_path,mode='r') as last_file:
            first_line = last_file.readline().strip()
            if first_line == '':
                last_ip = '10.8.0.0'
            else:
                last_ip = first_line
    # lock.acquire()
    create_a_pool(last_ip,email)
    # lock.release()


if __name__ == "__main__":
    if(len(sys.argv)>1):
        # lock = threading.Lock()
        email = sys.argv[1]
        # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        main(email)
