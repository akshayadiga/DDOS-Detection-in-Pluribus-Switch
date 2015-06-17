import threading
import time
from Tkinter import *
import os
import sys
import smtplib

def addToConsole(str):
	console.insert(END,str+"\n")

'''
Runs client-server-stats-show command and retrives the output 
Returns a list of all ip address and its details whose syn is greater than 1000
'''
def get_ip_syn_g1000(ip_switch,user,pswd):
	f=open("output.txt","w+")
	f.close()
	
	try:
		#run the command with output.txt as stdout file
		if(os.system("echo \"client-server-stats-show interval 5s limit-output 0 \"|sshpass -p '"+pswd+"' ssh "+user+"@"+ip_switch+" > output.txt")!=0):
			exit(0)
	except:
		addToConsole("Connection to Switch Failed!")
		return 0
			
	f=open("output.txt","r")
	
	data=[]
	count=0;
	for line in f:
		try:
			if(count==0):
				count+=1
				continue
			elif(count==1):
				count+=1
				continue
			d={}	
		
			switch,vlan,vxlan,clientip,serverip,syn,est,fin,obytes,ibytes,totalbytes,avgdur,avglat,lastseen=line.rstrip().split()
			d["switch"]=switch
			d["vlan"]=vlan
			d["vxlan"]=vxlan
			d["clientip"]=latency
			d["serverip"]=serverip
			d["syn"]=int(syn)
			d["est"]=int(est)
			d["fin"]=int(fin)
			d["obytes"]=obytes
			d["ibytes"]=ibytes
			d["totalbytes"]=totalbytes
			d["avgdur"]=avgdur
			d["avglat"]=avglat
			d["lastseen"]=lastseen
			
			#print(d)
			data.append(d)
		except:
			continue	
		
	
	f.close()
	
	#create a dictionary tat hold cliend ip address as key and its value as the details about the ip in another dictionary
	state_count={}
	for item in data:
		state_count[item["clientip"]]={"dest":item["serverip"],"syn":item["syn"],"est":item["est"],"fin":item["fin"]}
	
	
	#keep only those entries which have syn greater than 1000
	state_count={i:j for i,j in state_count.items() if j["syn"]>1000}
	
	return state_count		

def main(email_admin,ip_switch,user,pswd):	
	#Run sync check and detecting DDOS forever
	while(True):
		#chec
		list_causing_ddos=get_ip_syn_g1000(ip_switch,user,pswd)
		#list_causing_ddos["10.5.5.5"]={"dest":"10.6.6.6","syn":1200,"est":500,"fin":500}
		
		
		if(list_causing_ddos==0):
			startThread.configure(state=NORMAL)
			exit(0)
		if(len(list_causing_ddos)!=0):
			all_ddos_ip=""
	
			for ip,details in list_causing_ddos.items():
				addToConsole("IP:"+ip+"is creating a DDOS Attack!")
			
				#block in using vflow!
				try:
					if(os.system("echo \"vflow-create block flow3 scope local vlan 99 dst-ip "+ip+" action drop stats enable\"|sshpass -p '"+pswd+"' ssh "+user+"@"+ip_switch+" > output.txt")!=0):
						exit(0)
				except:
					addToConsole("Connection to Switch Failed!")
					return 0
				#vflow-create block flow3 scope local vlan 99 dst-ip+ip+ action drop stats enable
				#######
			
				addToConsole("IP:"+ip+"is blocked")
			
				#add this ip to all_ddos_ip
			
				all_ddos_ip=all_ddos_ip+","+ip
			
			#send admin a mail
		
			fromaddr = 'pluribus.switch.notice@gmail.com' 
			toaddrs = email_admin 

			msg = 'Subject:DDOS ATTACK NOTICE \n\n There was a possible DDOS attack that occured from'+ip+'following ip adresses and I have taken action by BLOCKING them! I wanted you to know!' 
			# Credentials (if needed) 
			username = 'pluribus.switch.notice' 
			password = 'pesittest123' 
			# The actual mail send 
			server = smtplib.SMTP('smtp.gmail.com:587') 
			server.starttls() 
			server.login(username,password) 
			try:
				server.sendmail(fromaddr, toaddrs, msg) 
			except:	
				pass
			finally:
				server.quit()
		else:
			addToConsole("No Attack!!")		
		#Re-check after 5 seconds
		time.sleep(5)


def start():
    email_admin=in1.get()
    ip_switch=in2.get()
    user=in3.get()
    pswd=in4.get()
    
    ##input validation
    
    ##################
    
    #addToConsole(email_admin)
    #addToConsole(ip_switch)
    #addToConsole(user)
    #addToConsole(pswd)
    t=threading.Thread(target=main,args=(email_admin,ip_switch,user,pswd))
    t.daemon = True
    t.start()
    startThread.configure(state=DISABLED)



mainFrame=Tk()

heading=Label(mainFrame,text="DDOS Prevention (Pluribus Network Switch)",bg="black",fg="white",font="bold").grid(row=0,column=0,columnspan=2)

lab1=Label(mainFrame,text="Admin Email-ID").grid(row=1,column=0,columnspan=1)
lab2=Label(mainFrame,text="IP address").grid(row=2,column=0,columnspan=1)
lab3=Label(mainFrame,text="Username").grid(row=3,column=0,columnspan=1)
lab4=Label(mainFrame,text="Password").grid(row=4,column=0,columnspan=1)

startThread=Button(mainFrame,text="Secure Switch",command=start,width=34)
startThread.grid(row=5,column=0,columnspan=2)

in1=Entry(mainFrame)
in1.grid(row=1,column=1,columnspan=1)
in2=Entry(mainFrame)
in2.grid(row=2,column=1,columnspan=1)
in3=Entry(mainFrame)
in3.grid(row=3,column=1,columnspan=1)
in4=Entry(mainFrame,show="*")
in4.grid(row=4,column=1,columnspan=1)




scrollbar = Scrollbar(mainFrame,orient=VERTICAL)

console=Text(mainFrame,bg="white",height=10,width=30,yscrollcommand = scrollbar.set)
console.grid(row=7,column=0,columnspan=2)
#console.pack(side="left", fill="both", expand=True)
#scrollbar.grid(row=7,column=3,rowspan=4)
scrollbar.grid(row=7,padx=1, column=3,sticky=NS,)
scrollbar.configure(command = console.yview )

mainFrame.mainloop()

