import sys
import os
from collections import deque
# import threading
# from concurrent.futures import ThreadPoolExecutor
# import concurrent.futures

def is_valid_ip(ip):
    parts = ip.split('.')

    return len(parts) == 4 and all(part.isdigit() for part in parts)

def order_container(ds):
    valid_ips = [ip for ip in ds if is_valid_ip(ip)]

    if ds:
        ds = sorted(ds,key=lambda x: tuple(map(int,x.split('.'))))
        return ds
    else:
        return None

def order_container_with_ip(ds):
    if ds:
        ds = sorted(ds,key=lambda x:tuple(map(int,x[1].split('.'))))
        return ds
    else:
        return None

def update_Hub(new_ip,email,dq,client_name):
    if new_ip:
        dq.append(new_ip)
        dq = order_container(dq)
        Registered_ips = deque([])
        org_path = f'/etc/openvpn/hub_clients/{email}'
        flag = False
        if os.path.exists(org_path):
            with open(org_path,mode='r+') as org_file:
                org_file.seek(0)
                org_file.truncate(0)
                string_conversion = ','.join(map(str,dq))
                org_file.write(f"{string_conversion}\n")
                flag = True
        if flag == True:
            ip_list = deque([])
            all_list = deque([])
            ipp_text_file_path = '/etc/openvpn/server/ipp.txt'
            if os.path.exists(ipp_text_file_path):
                with open(ipp_text_file_path,mode='r+') as ipp_file:
                    # file_read = ipp_file.readlines().strip()
                    for line in ipp_file:
                        parts = line.strip().split(',')
                        if(len(parts)) == 2:
                            CN,ip = parts
                            all_list.append([CN,ip])
                            ip_list.append(ip)
                    Registered_ips.extend(ip_list)
                    Registered_ips.append(new_ip)
            all_list.append([client_name,new_ip])
            all_list = order_container_with_ip(all_list)
            Registered_ips = order_container(Registered_ips)
            with open(ipp_text_file_path,mode='w') as ipp_file:
                ipp_file.seek(0)
                ipp_file.truncate(0)
                for file in all_list:
                    ipp_file.write(f"{file[0]},{file[1]}\n")
    else:
        pass
    
def update_ccd(CN,ip):
    if ip:
        ccd_path = f'/etc/openvpn/ccd/{CN}'
        with open(ccd_path,'w') as ccd_file:
            ccd_file.write(f"{ip}")

def assign_ip_to_client(dq,client_name,email):
    dq = order_container(dq)
    server_conf_path =f"/etc/openvpn/server/server.conf"
    with open(server_conf_path,"r") as server_file:
        for line in server_file:
            if "server"  in line and line.startswith("server"):
                server,ip,netmask = line.split(' ')
                pool=ip
                net_mask = netmask
    ip_assignments = deque([])
    if dq[-2] == dq[-1]:
        print("1")
        exit(-1)
    elif (len(dq)==2):
        print(f"ifconfig-push {dq[0]} {netmask}")
        update_ccd(client_name,f"ifconfig-push {dq[0]} {netmask}")
        update_Hub(dq[0],email,dq,client_name)
    else:
        ip_assignments.append(dq[-2])
        if ip_assignments:
            ip_assignments = order_container(ip_assignments)
            ip = ip_assignments[0]
            one, two, three, four = ip.split('.')
            n1,n2,n3,n4=netmask.split('.')
            ip = f'{one}.{two}.{three}.{int(four)+1}'
            ip_assignments.append(ip)
            print(f"ifconfig-push {ip} {netmask}")
            update_ccd(client_name,f"ifconfig-push {ip} {netmask}")
            update_Hub(ip,email,dq,client_name)
        else:
            n1,n2,n3,n4=netmask.split('.')
            ip = str(pool).strip()
            ip=ip[:7]+'1'
            ip_assignments.append(ip)
            print(f"ifconfig-push {ip} {netmask}")
            update_ccd(client_name,f"ifconfig-push {ip} {netmask}")
            update_Hub(ip,email,dq,client_name)
    return ip_assignments




def main(email,client_name):
    pool_path=f'/etc/openvpn/hub_clients/{email}'
    dq = deque([])
    if os.path.exists(pool_path):
        with open(pool_path,mode='r') as file_path:
            file_read = file_path.readline().strip()
            dq.extend(file_read.split(','))
    # lock.acquire()
    assign_ip_to_client(dq,client_name,email)
    # lock.release()




if __name__ == "__main__":
    if(len(sys.argv[1])>1):
        # lock = threading.Lock()
        email = sys.argv[1]
        client_name = sys.argv[2]
        # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        main(email,client_name)
