import threading
from collections import deque
import sys, os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

def order_container(ds):
    if ds:
        ds = sorted(ds,key=lambda x: tuple(map(int,x.split('.'))))
        return ds
    else:
        return None



def process_ip_list(pool,netmask):
    ipp_txt_file="/etc/openvpn/server/ipp.txt"
    ip_assignments=deque([])
    if os.path.exists(ipp_txt_file):
        with open(ipp_txt_file,mode='r') as file:
            for line in file:
                parts = line.strip().split(',')
                if(len(parts)) == 2:
                    CN,ip = parts
                    ip_assignments.append(ip)
    
    last_one = "/etc/openvpn/server/last_ip"
    file_read = ''
    
    if os.path.exists(last_one):
        with open(last_one,mode='r') as last_one_ip_file:
	        file_read = last_one_ip_file.readline().strip()
    

    # temp = deque([])
    # temp.append(ip_assignments[-1] if ip_assignments else pool)
    # temp.append(file_read if file_read else pool)
    ip = file_read if file_read else pool
    if ip_assignments:
        ip_assignments = order_container(ip_assignments)
        ip = ip
        one, two, three, four = ip.split('.')
        n1,n2,n3,n4=netmask.split('.')
        if int(four) < 254:
            four = int(four) + 1
            ip = f"{one}.{two}.{three}.{four}"
            ip_assignments.append(ip)
        else:
            if int(n3) != 255 and int(n4) == 0:
                if int(three) <= 254:
                    three = str(int(three)+1)
                    four = "1"
                    ip = f"{one}.{two}.{three}.{four}"
                    ip_assignments.append(ip)
                else:
                    if int(four) == 254 and int(three) == 255:
                        if int(two) == 9:
                            print("All are filled")
                            exit(-1)
                        else:
                            two = "9"
                            ip = f"{one}.{two}.0.1"
                            ip_assignments.append(ip)
            else:
                print("1")
                exit(-1)
    else:
        n1,n2,n3,n4=netmask.split('.')
        ip = str(pool).strip()
        ip=ip[:7]+'1'
        ip_assignments.append(ip)
    return ip_assignments


def Generate_User_ip(lock,CN):
    pool=0
    net_mask = 0
    server_conf_path =f"/etc/openvpn/server/server.conf"
    with open(server_conf_path,"r") as server_file:
        for line in server_file:
            if "server"  in line and line.startswith("server"):
                server,ip,netmask = line.split(' ')
                pool=ip
                net_mask = netmask
    lock.acquire()
    try:
        val = process_ip_list(pool, net_mask)
    finally:
        lock.release()
    if val:
        ipp_text_file_path="/etc/openvpn/server/ipp.txt"
        last_ip_path = "/etc/openvpn/server/last_ip"
        if os.path.exists(ipp_text_file_path):
            with open(ipp_text_file_path,mode="a") as text_file:
                text_file.write(f"{CN},{val[-1]}\n")
        if os.path.exists(last_ip_path):
            with open(last_ip_path,mode='w') as last_one_file:
                last_one_file.write(f'{val[-1]}\n')
        print(f"ifconfig-push {val[-1]} {net_mask}")
        return f"ifconfig-push {val[-1]} {net_mask}"
    else:
        print(f"Nothing Here {val}")

def main(common_name):
    lock = threading.Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(Generate_User_ip,lock,common_name)
        future.result()
        # if future.result() is not None:
        #     print(future.result())
       


if __name__ == "__main__":
    if(len(sys.argv)>1):
        common_name = sys.argv[1]
        main(common_name)
    else:
        pass
