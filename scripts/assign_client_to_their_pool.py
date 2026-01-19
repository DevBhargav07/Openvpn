import sys
import os
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading

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

def update_org_file(new_ip,org_name,dq,client_name):
    if new_ip:
        dq.append(new_ip)
        dq = order_container(dq)
        Registered_ips = deque([])
        org_path = f'/etc/openvpn/hub_clients/{org_name}'
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
def assign_ip_to_client(dq,client_name,org_name):
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
        ip = dq[-2] if len(dq) == 2 else dq[-1]
        length = len(dq)
        if length == 3:
            # print("All fields for your hub are filled!!")
            print("1")
            exit(-1)
        elif length == 2:
            ip_assignments.append(ip)
            print(f"ifconfig-push {ip} {netmask}")
            update_org_file(ip,org_name,dq,client_name)
        # ip_assignments.append(ip)

        # print(f"ifconfig-push {ip} {netmask}")
        # update_org_file(ip,org_name,dq,client_name)
    elif (len(dq)==2):
        print(f"ifconfig-push {dq[0]} {netmask}")
        update_org_file(dq[0],org_name,dq,client_name)
    else:
        ip_assignments.append(dq[-2])
        if ip_assignments:
            ip_assignments = order_container(ip_assignments)
            ip = ip_assignments[0]
            one, two, three, four = ip.split('.')
            n1,n2,n3,n4=netmask.split('.')
            if int(four) < 254:
                four = int(four) + 1
                ip = f"{one}.{two}.{three}.{four}"
                ip_assignments.append(ip)
                print(f"ifconfig-push {ip} {netmask}")
                update_org_file(ip,org_name,dq,client_name)
            else:
                if int(n3) != 255 and int(n4) == 0:
                    if int(three) <= 254:
                        three = str(int(three)+1)
                        four = "1"
                        ip = f"{one}.{two}.{three}.{four}"
                        ip_assignments.append(ip)
                        print(f"ifconfig-push {ip} {netmask}")
                        update_org_file(ip,org_name,dq,client_name)
                    else:
                        if int(four) == 254 and int(three) == 255:
                            if int(two) == 9:
                                # print("All are filled")
                                exit(-1)
                            else:
                                two = "9"
                                ip = f"{one}.{two}.0.1"
                                ip_assignments.append(ip)
                                print(f"ifconfig-push {ip} {netmask}")
                                update_org_file(ip,org_name,dq,client_name)
                else:
                    print("2")
                    exit(-1)
        else:
            n1,n2,n3,n4=netmask.split('.')
            ip = str(pool).strip()
            ip=ip[:7]+'1'
            ip_assignments.append(ip)
            print(f"ifconfig-push {ip} {netmask}")
            update_org_file(ip,org_name,dq,client_name)
    return ip_assignments
    # print(ip_assignments)




def main(org_name,client_name,lock):
    pool_path=f'/etc/openvpn/hub_clients/{org_name}'
    dq = deque([])
    if os.path.exists(pool_path):
        with open(pool_path,mode='r') as file_path:
            file_read = file_path.readline().strip()
            # from_ip,to_ip = file_read.split(',')
            dq.extend(file_read.split(','))
    lock.acquire()
    assign_ip_to_client(dq,client_name,org_name)
    lock.release()


if __name__ == "__main__":
    if(len(sys.argv)>1):
        lock = threading.Lock()
        org_name = sys.argv[1]
        client_name = sys.argv[2]
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            main(org_name,client_name,lock)
