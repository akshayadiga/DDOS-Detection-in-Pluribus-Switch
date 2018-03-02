Hardware Requirements:

1. Pluribus Switch
2. A host machine to access the Switch remotely
3. An ethernet lan connection to connect host to the switch

Software Requirements:

1. Ubuntu
2. Python3
3. sshpass (sudo apt-get install sshpass)
4. CLI of Pluribus Switch installed in the Switch

How to Execute:

1. Run the ddos_check_each_ip_gui.py
2. Give the Admin e-mail address for notification purpose
3. The program keeps checking after every 5 seconds for ddos attack
4. When a ddos attack is detected
	a. The client IP address is blocked
	b. The admin is sent a mail and notified
5. It runs forever checkiing for ddos attack
