from collections import deque
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import sys
import os
import threading

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
def update_files(ips):
    ips=list(ips)
    if len(ips) <= 1:
        return update_last_ip_file(''.join(ips[1]))
    else:
        return update_last_ip_file(''.join(ips[1]))

def update_pool_org(org_name,from_ip,to_ip):
    pool_ip_list = f'/etc/openvpn/hub_clients/{org_name}'
    with open(pool_ip_list,mode='w') as pool_file:
        pool_file.write(f'{from_ip},{to_ip}\n')

def assign_pool_ip(last_ip,no_of_ips_assign_in_pool,org_name):
    one,two,three,four = last_ip.split('.')
    remaining = 254-int(four)
    res = deque([])
    latest_ip=''
    starting_ip = ''
    if int(four) < 254:
        starting_ip = f"{one}.{two}.{three}.{int(four)+1}"
        res.append(starting_ip)
    else:
        if int(three) <= 254:
            three = int(three)+1
            four = '1'
            starting_ip = f"{one}.{two}.{three}.{four}"
            res.append(starting_ip)
        else:
            if int(two) != 9:
                two = int(two)+1
                three = '0'
                four = '1'
                starting_ip = f"{one}.{two}.{three}.{four}"
                res.append(starting_ip)
    no_of_ips_assign_in_pool = int(no_of_ips_assign_in_pool)
    if no_of_ips_assign_in_pool > remaining:
        number = no_of_ips_assign_in_pool
        quotient = 1 if (number < 254 and int(four)+number > 254) else number // 254 
        remainder = number % 254
        if int(three)+quotient <= 255:
            three = int(three)+quotient
            four = (no_of_ips_assign_in_pool-remaining) if ((no_of_ips_assign_in_pool+remaining) >= 254) else (no_of_ips_assign_in_pool-remaining)
            lastest_ip = f"{one}.{two}.{three}.{four}"
            res.append(lastest_ip)
            update_files(res)
        else:
            if int(two) != 9:
                two = int(two)+1
                last_ip=f"{one}.{two}.0.0"
                value = (remainder-(quotient*254)-remaining) if (remainder-(quotient*254)-remaining) >= 0 else (no_of_ips_assign_in_pool-remaining)
                assign_pool_ip(last_ip,value,org_name)
            else:
                print("1")
                exit(-1)
    else:
        quotient = no_of_ips_assign_in_pool // 254
        remainder = no_of_ips_assign_in_pool % 254
        four = int(four)+no_of_ips_assign_in_pool
        lastest_ip = f"{one}.{two}.{quotient+int(three)}.{four}"
        res.append(lastest_ip)
        update_files(res)

    update_pool_org(org_name,res[0],res[-1])
    print(f"{res[0]},{res[-1]}")


def main(org_name,pool_range,lock):
    last_ip = ''
    last_ip_file_path = '/etc/openvpn/server/last_ip'
    if os.path.exists(last_ip_file_path):
        with open(last_ip_file_path,mode='r') as last_file:
            first_line = last_file.readline().strip()
            if first_line == '':
                last_ip = '10.8.0.0'
            else:
                last_ip = first_line
    lock.acquire()
    assign_pool_ip(last_ip,pool_range,org_name)
    lock.release()

if __name__ == "__main__":
    if(len(sys.argv)>1):
        lock = threading.Lock()
        org_name = sys.argv[1]
        pool_range = sys.argv[2]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            main(org_name,pool_range,lock)














