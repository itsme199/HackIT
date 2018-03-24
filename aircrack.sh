!#/bin/bash
echo -n "Enter BSSID: "
read bssid
echo -n "Enter Handshake File: "
read handshake
echo -n "Enter Wordlist [Leave Blank for Default Crunch Wordlist]: "
read wordlist
case $wordlist in
	"")
		wordlist = "-"
		last_command="crunch 0 25 abcdefghijklmonpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 | aircrack-ng --bssid $bssid $handshake -w -"
		eval $last_command
		;;			
	*)
		last_command="aircrack-ng --bssid $bssid $handshake -w $wordlist"
		eval $last_command
		;;
		esac
