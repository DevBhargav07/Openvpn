#!/bin/bash

CLIENT_CN="$common_name"    #$1-common_name $4-ip

if [ "$script_type" == "$client-connect" ];then

	#we have to give the path for python file
	PYTHON_SCRIPT_PATH="/etc/openvpn/scripts/assign_ip.py"


	#process of ip
	ASSIGNED_IP=$(python3 $PYTHON_SCRIPT_PATH $CLIENT_CN)

	#log file time
	LOG_TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

	#log file path
	#LOG_PATH=?

	#TARGET_FILE="/etc/openvpn/ccd/$CLIENT_CN"

	#client
	#CLIENT_FILE=$(cat $TARGET_FILE)

	#echo "assigning the same ip for $CLIENT_CN"

	#echo "ifconfig-push $ASSIGNED_IP 255.255.255.0" > "/home/bhargav/Documents/openvpn/ccd/$CLIENT_CN"

	#if updated log files also needs to updated

	#echo "$CLIENT_CN is already exists"

	#ASSIGNED_IP=$(python3 $PYTHON_SCRIPT_PATH $CLIENT_CN)

	#have to create log for:- timestamp common_name ip assigned to it 
	#touch "/etc/openvpn/ccd/$CLIENT_CN"

	#echo "ifconfig-push $ASSIGNED_IP 255.255.255.0" >> "/etc/openvpn/ccd/$CLIENT_CN"

	#echo "$LOG_TIMESTAMP  -- $CLIENT_CN IS CREATED" >> "$LOG_PATH" ----CHANGE HERE LOG FILE PATH

	#echo "$CLIENT_CN,$ASSIGNED_IP" >> "/etc/openvpn/server/ipp.txt"

elif [ "$script_type" == "$client-disconnect" ];then 

	echo "$CLIENT_CN is disconnected"

	#echo "$LOG_TIMESTAMP   -- $CLIENT_CN IS DISCONNECTED"  >> "LOG_PATH"   --- HAVE TO SAVE THESE CHANGES.

fi
