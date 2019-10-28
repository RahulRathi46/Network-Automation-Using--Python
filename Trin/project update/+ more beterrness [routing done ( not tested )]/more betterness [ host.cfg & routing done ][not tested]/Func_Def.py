import ConfigParser
import paramiko
import time


def config(i):
    if i=="h":
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'host.cfg'))
        return config
    
    elif i=="c":
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'trin.cfg'))
        return config
    
    else:
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'trin.ini'))
        return config
    
    
    
def init_host():
    print "##############-> HOST_CONFIG <-###############\n\n"
    for count in range(100):  
        if config("h").has_option("Host_config", "host%d"%count) :
            print str(count) + " - "+config("h").get("Host_config", "host%d"%count)+"\n"   
        else :
            break
    print "###########################################\n\n"    
    print"\n"
    return raw_input("Enter Host No. : ")
        
        
        
    



def connect_ssh(Select,r):
   
    host_no=0
    for l in range(r):
        if l==0:
                
            # Create instance of SSHClient object
            ssh = paramiko.SSHClient()
        
            # Automatically add untrusted hosts (make sure okay for security policy in your environment)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
            # initiate SSH connection
            ssh.connect(config("h").get("Host_config", "host%d"%l) , username=config("h").get("Host_config", "username%d"%l), password=config("h").get("Host_config", "password%d"%l))
            
            # establish an 'interactive session'
            remote_ssh = ssh.invoke_shell()
            
            # Turn off paging
            remote_ssh.send("terminal length 0 \n")
            
            
            

        else :
            
            
            #Typing SSH CMD
            remote_ssh.send("ssh "+"-l "+ config("h").get("Host_config", "username%d"%l)+" " +config("h").get("Host_config", "host%d"%l)+"\n")
            time.sleep(2)
            
            #Entering password
            remote_ssh.send(config("h").get("Host_config", "password%d"%l)+"\n")
            time.sleep(1)
            
            # Turn off paging
            remote_ssh.send("terminal length 0 \n")
            
            #assigning host no to determne config
            host_no=host_no+1
            
            
     
    buffer_clear=remote_ssh.recv(1000)
    
    print " Interactive SSH session established \n"
    
    #action list
    to_do(remote_ssh,Select,ssh,host_no,r)
    

    
    
    
def signal(x,remote_ssh,r):
    if x=="g":
        remote_ssh.send("config t\n")
        time.sleep(2)
    else :
        remote_ssh.send("en\n")
        time.sleep(1)
# used to send enable password
        remote_ssh.send(config("c").get("Host_config", "user_pass%d"%(r-1))+"\n")
        time.sleep(1)
        
    buffer_clear=remote_ssh.recv(1000)
   





def to_do(remote_ssh,Select,ssh,host_no,r):
    
    if Select=="1":
        signal("u", remote_ssh,r)
        signal("g", remote_ssh,r)
        interface(remote_ssh,host_no)
        
    elif Select=="2":
        signal("u", remote_ssh,r)
        signal("g", remote_ssh,r)
        line(remote_ssh,host_no)
        get_state(remote_ssh,"2")
        
    elif Select=="3":
        Route(remote_ssh,host_no)
        
    elif Select=="4":
        print("\n#########################################################")
        print ("1.Interface "+"2.running-config "+"3. startup-config"+" 4. route")
        print ("#########################################################\n")
        x=raw_input("Enter the choice : ")
        print "\n"
        signal("u", remote_ssh,r)
        get_state(remote_ssh,x)
        
    elif Select=="5":
        print("\n###############################################################################")
        print ("1.Save to startup-Config "+"  "+"2. Get back Running-Config from Startup-Config")
        print ("###############################################################################\n")
        x=raw_input("Enter the choice : ")
        print "\n"
        signal("u", remote_ssh,r)
        save(remote_ssh,x)
        
    else:
        return 0
        
    #session terminiting aftwer every task { applied for security } { you can inscres speed of excution of script by removing this }
    ssh.close()
    
def line(remote_ssh,host_no):
    #intiallizing of task 
    for l in range(int(config("c").get("Host%d_Line_config"%host_no, "no_of_task"))) :
        
        #sending frist line cmd
        remote_ssh.send("line "+ config("c").get("Host%d_Line_config"%host_no, "line%d"%l) +"\n")
        time.sleep(1)
        
        #sending login cmd 
        if "login" in config("c").get("Host%d_Line_config"%host_no, "login%d"%l) :
            remote_ssh.send(config("c").get("Host%d_Line_config"%host_no, "login%d"%l) +"\n")
        else :
            remote_ssh.send( config("c").get("Host%d_Line_config"%host_no, "login%d"%l) +"\n")
        
        #sending password cmd
        if config("c").get("Host%d_Line_config"%host_no, "password%d"%l)=="-1" :
            remote_ssh.send("exit\n")
        else :
            remote_ssh.send("password "+ config("c").get("Host%d_Line_config"%host_no, "password%d"%l) +"\n")
        
        #sending  exit
        remote_ssh.send("exit\n")
        time.sleep(2)
        
        print remote_ssh.recv(1000)
    #sending back to user-mode signal
    remote_ssh.send("exit\n")


def interface(remote_ssh,host_no):
    
    #intiallizing of task 
    for l in range(int(config("c").get("Host%d_Interface_config"%host_no, "no_of_task"))) :
        
        
        # sending interface cmd
        remote_ssh.send("interface "+ config("c").get("Host%d_Interface_config"%host_no, "interface%d"%l) +"\n")
        time.sleep(1)
        
        #configuring ip & subnet
        remote_ssh.send("ip address "+ config("c").get("Host%d_Interface_config"%host_no, "ip_subnet%d"%l) +"\n")
        time.sleep(1)
        
        #sending state config
        if config("c").get("Host%d_Interface_config"%host_no, "state%d"%l) =="up":
            remote_ssh.send("no sh"+"\n")
            time.sleep(1)
            
        else :
            remote_ssh.send("sh\n")
            time.sleep(1)
    
    
    remote_ssh.send("exit\n")
    remote_ssh.send("\n")
    time.sleep(1)
    remote_ssh.send("exit\n")
    time.sleep(1)
    
     
   
    
    #sending get_state
    get_state(remote_ssh,"1")
    
    
    
    
    
    
def get_state(remote_ssh,x):
    
    #get_state of interface 
    if x=="1":
        remote_ssh.send(config("d").get("Get_state", "ip_interface")+"\n")
        time.sleep(2)
    #get state of running state
    elif x=="2":
        remote_ssh.send(config("d").get("Get_state", "running-config")+"\n")
        time.sleep(5)
    #get state of startup
    elif x=="3":
        remote_ssh.send(config("d").get("Get_state", "startup-config")+"\n")
        time.sleep(5)
        
    elif x=="4":
        remote_ssh.send(config("d").get("Get_state", "route")+"\n")
        remote_ssh.send("\n")
        time.sleep(5)
        
    print remote_ssh.recv(900)





def save(remote_ssh,x):
    
    #get state save to Startup-config
    if x=="1":
        remote_ssh.send(config("d").get("Save_change", "to_startup-config")+"\n")
        remote_ssh.send("\n")
        
    #get state save to running-config
    elif x=="2":
        remote_ssh.send(config("d").get("Save_change", "to_running-config")+"\n")
        remote_ssh.send("\n")
        
    
    time.sleep(5)
    print remote_ssh.recv(100)
    
    
    
    
    

 
def Route(remote_ssh,host_no):
    #intiallizing of task 
    for l in range(int(config("c").get("Host%d_Route_config"%host_no, "no_of_task"))) :
        #cheacking for protocal
        if "static" in config("c").get("Host%d_Line_config"%host_no, "protocol%d"%l) :
            st_route(remote_ssh,host_no,l)
        else :
            dy_route(remote_ssh,host_no,l)
           
        #sending  exit
        remote_ssh.send("exit\n")
        time.sleep(2)
        
        print remote_ssh.recv(1000)
        
        
        
def st_route(remote_ssh,host_no,l): #Driving routies for Static_routing 
    #counter & network index 
    no=0
    for n in range (10) :
        if config("c").has_option("Host%d_Line_config"%host_no, "route%d"%no) == True :
            remote_ssh.send("ip route " + config("c").get("Host%d_Line_config"%host_no, "route%d"%no) +"\n")
            #counting for max limit
            no=no+.10    
        else :
            break   
        
    templete(remote_ssh,host_no,l) 
                
                   
    
  
    
def dy_route(remote_ssh,host_no,l) : #Driving routies for dynamic routing 
    #counter & network index 
    no=0
    remote_ssh.send(config("c").get("Host%d_Line_config"%host_no, "protocol%d"%l) +"\n")
    for n in range (10) :
        if config("c").has_option("Host%d_Line_config"%host_no, "network%d"%no) == True :
            remote_ssh.send("network " + config("c").get("Host%d_Line_config"%host_no, "network%d"%l) +"\n")
            #counting for max limit
            no=no+.10  
        else :
            break
        
    templete(remote_ssh,host_no,l)
        
        
        
def templete(remote_ssh,host_no,l) :
    #counter & network index 
    no=0
    for n in range (10) :
        if config("c").has_option("Host%d_Line_config"%host_no, "template%d"%no) == True :
            remote_ssh.send(config("c").get("Host%d_Line_config"%host_no, "template%d"%l) +"\n")
            #counting for max limit
            no=no+.10  
        else :
            break
        
    # sending exit
    remote_ssh.send("exit\n")