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

**About openvpn-install.sh**
  This file is used to Install Openvpn
  At the time of installing it is going to ask some pre-requirements to run for the project
  After Installing the openvpn, it's going to create an .ovpn certificate to the usage private network
  In this script we did some modifications to take the requirements like username for the certificate through command line only
  Upon Taking it is going to call one function which handles the creation of ovpn certificate
  If we want to create HUB or add client in a HUB we are going to the requirements (inputs) as mentioned above
  
**About Scripts(python):-**

  Here, we used some python scripts to generate a static ip for a user
  In here we are using ThreadPoolExecutor for multi-using process and This is written for creating HUB first
  Inside any one of the HUB (name specifically), we can create an User with the username
  So, as this is file system i am using Os module to work with the files in this project
  There will be ccd directory which will be helpful to the server to hold or take the static ip mentioned in that directory with  
   the  username  ( if user1 is username then file name is also user1 [withoutextensions] and ifconfig-push ip netmask)
  And these certificates will be created in a specific path mentioned in the openvpn-install.sh file.


Above Whole process of installing, creating and revoking OpenVPN and .ovpn certificates are done in Ubuntu(Linux) installed system.
While taking the script only take if the script supports for Windows os.
And the Paths also will be different for Windows system.

A Linux system path will be located at
/etc/openvpn/..
Here you can find the folders and files which are related to the openvpn