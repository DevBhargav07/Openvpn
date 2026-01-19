
import asyncio, time, os
from collections import deque
from asgiref.sync import sync_to_async
import sys
# from aiofile import async_open


async def order_list(ds):
    if ds:
        ds=sorted(ds,key=lambda x: tuple(map(int,x.split('.'))))
        return ds 
    else:
        return None

async def process_ip_list(pool,netmask):
    ipp_txt_file="/home/bhargav/Documents/openvpn/server/ipp.txt"    #we have to change for our need.
    ip_assignments=deque([])
    try:
        with open(ipp_txt_file,mode='r') as file:
            for line in file:
                parts=line.strip().split(',')
                if(len(parts)) == 2:
                    CN,ip=parts
                    ip_assignments.append(ip)
            file.close()
    except FileNotFoundError:
        print(f"file {ipp_txt_file} didn't found in the specified path")

    if ip_assignments:
        ip_assignments = await order_list(ip_assignments)
        ip = ip_assignments[-1]
        one, two, three, four = ip.split('.')
        if int(four) < 254:
            four = int(four) + 1
            ip = f"{one}.{two}.{three}.{four}"
            ip_assignments.append(ip)  # Append to the main list
        else:
            n1,n2,n3,n4=netmask.split('.')
            if int(n3) == 0 and int(n4) == 0:
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
                print("Please change the netmask only these are allowed")
                exit(-1)
    else:
        ip = str(pool)
        ip=ip[:7]+'1'
        ip_assignments.append(ip)
    return ip_assignments
    # print(offline_list)

async def emulate_user(CN):
    # print(f"User {id} requesting for the ip....")
    ccd_file_path = f"/home/bhargav/Documents/openvpn/ccd/{CN}.ovpn"
    pool=0
    net_mask = 0
    server_conf_path =f"/home/bhargav/Documents/openvpn/server/server.conf"
    with open(server_conf_path,"r") as server_file:
        for line in server_file:
            if "server"  in line and line.startswith("server"):
                server,ip,netmask = line.split(' ')
                pool=ip
                net_mask = netmask
    if os.path.exists(ccd_file_path):
        print(f"Client with the {CN} name already existed")
        pass
    else:
        val = await process_ip_list(pool,net_mask)
        with open(ccd_file_path,mode="w") as file:
            file.write(f"ifconfig-push {val[-1]} {net_mask}")
            file.close()
        ipp_text_file_path="/home/bhargav/Documents/openvpn/server/ipp.txt"
        if not os.path.exists(ipp_text_file_path):
            try:
                with open(ipp_text_file_path,mode='x') as txt_file:
                    txt_file.close()
            except FileNotFoundError:
                print("File is not found in that directory")
        if os.path.exists(ipp_text_file_path):
            with open(ipp_text_file_path,mode="a") as text_file:
                text_file.write(f"{CN},{val[-1]}\n")
                text_file.close()
        # print(f"ifconfig-push {val[-1]} {net_mask}")
        return f"ifconfig-push {val[-1]} {net_mask}"

    # await asyncio.sleep(1)
    

# Main_container = deque([])
async def main(common_name):
    # data=await fetch_data()
    # tasks = []
    # if ips_count:
    #     if ips_count == 1:
    #             tasks.append(emulate_user(Main_container,1))
    #     elif ips_count > 1 and ips_count: 
    #         for i in range(1,ips_count+1):
    #             tasks.append(emulate_user(Main_container,i))

    # vals = await asyncio.gather(*tasks)
    vals = await emulate_user(common_name)
    print(vals)

if __name__ == "__main__":
    if(len(sys.argv)>1):
        common_name=sys.argv[1]
        asyncio.run(main(common_name))
    else:
        pass
    
    


# asyncio.run(main())

# @sync_to_async
# def fetch_data():
#     offlines_devs=[]
#     data = Master.objects.all().values() #at this we have to provide the new db.
#     if data:
#         for info in data:
#             # print(info["device_status"])
#             tempo={}
#             if info["device_status"]=="Offline":
#                 tempo["id"]=info["id"]
#                 tempo["device_id"]=info["device_id"]
#                 tempo["device_status"]=info["device_status"]
#             if tempo:
#                 offlines_devs.append(tempo)
#     return offlines_devs