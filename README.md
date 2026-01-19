# Openvpn
Working of Openvpn

This Explains or tells about the working of Openvpn 
But, if you want to understand what is the basic introduction please do visit.
https://openvpn.net/as-docs/v3/

Here, I will attach one script which will help to download the openvpn and when you run again the 
script will help to generate .ovpn certificates 
and revoke certificates
delete ovpn certificates

This script will only take command line arguments, please remember that
1) creating new client 
2) revoking a client
3) Removing Openvpn
4) exit (from program)
5) Creating a hub
6) adding/creating a new client in already existed hub

Example command is

**sh +x openvpn-install.sh 1 Username**
        (file_name)   (process number)  (name of the user)


**About Scripts(python):-**

Here, we used some python scripts to generate a static ip for a user
In here we are using ThreadPoolExecutor for multi-using process
And This is written for creating HUB first
Inside any one of the HUB (name specifically), we can create an User with the username
So, as this is file system i am using Os module to work with the files in this project
There will be ccd directory which will be helpful to the server to hold or take the static ip mentioned in that directory with  
      the  username  ( if user1 is username then file name is also user1 [withoutextensions] and ifconfig-push ip netmask)
And these certificates will be created in a specific path mentioned in the openvpn-install.sh file.
