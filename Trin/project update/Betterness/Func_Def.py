import ConfigParser
import paramiko
import time


def config(i):
    if i=="c":
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'trin.cfg'))
        return config
    else:
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'trin.ini'))
        return config


def connect_ssh(x,r):
   
    L=0
    for l in range(r):
        if l==0:
                
            # Create instance of SSHClient object
            ssh = paramiko.SSHClient()
        
            # Automatically add untrusted hosts (make sure okay for security policy in your environment)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
            # initiate SSH connection
            ssh.connect(config("c").get("Host_config", "host%d"%l) , username=config("c").get("Host_config", "username%d"%l), password=config("c").get("Host_config", "password%d"%l))
            
            # establish an 'interactive session'
            remote_ssh = ssh.invoke_shell()
            
            # Turn off paging
            remote_ssh.send("terminal length 0 \n")
            
            
            

        else :
            
            
            #Typing SSH CMD
            remote_ssh.send("ssh "+"-l "+ config("c").get("Host_config", "username%d"%l)+" " +config("c").get("Host_config", "host%d"%l)+"\n")
            time.sleep(2)
            
            #Entering password
            remote_ssh.send(config("c").get("Host_config", "password%d"%l)+"\n")
            time.sleep(1)
            
            # Turn off paging
            remote_ssh.send("terminal length 0 \n")
            
            #assigning host no to determne config
            L=L+1
            
            
     
    buffer_clear=remote_ssh.recv(1000)
    
    print " Interactive SSH session established \n"
    
    #action list
    to_do(remote_ssh,x,ssh,L,r)
    

    
    
    
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
   





def to_do(remote_ssh,o,ssh,L,r):
    if o=="1":
        signal("u", remote_ssh,r)
        signal("g", remote_ssh,r)
        interface(remote_ssh,L)
        
    elif o=="2":
        signal("u", remote_ssh,r)
        signal("g", remote_ssh,r)
        line(remote_ssh,L)
        get_state(remote_ssh,"2")
        
    elif o=="3":
        print("\n#########################################################")
        print ("1.Interface "+"2.running-config "+"3. startup-config"+" 4. route")
        print ("#########################################################\n")
        x=raw_input("Enter the choice : ")
        print "\n"
        signal("u", remote_ssh,r)
        get_state(remote_ssh,x)
    elif o=="4":
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
    
def line(remote_ssh,L):
    #intiallizing of task 
    for l in range(int(config("c").get("Host%d_Line_config"%L, "no_of_task"))) :
        
        #sending frist line cmd
        remote_ssh.send("line "+ config("c").get("Host%d_Line_config"%L, "line%d"%l) +"\n")
        time.sleep(1)
        
        #sending login cmd 
        if "login" in config("c").get("Host%d_Line_config"%L, "login%d"%l) :
            remote_ssh.send(config("c").get("Host%d_Line_config"%L, "login%d"%l) +"\n")
        else :
            remote_ssh.send( config("c").get("Host%d_Line_config"%L, "login%d"%l) +"\n")
        
        #sending password cmd
        if config("c").get("Host%d_Line_config"%L, "password%d"%l)=="-1" :
            remote_ssh.send("exit\n")
        else :
            remote_ssh.send("password "+ config("c").get("Host%d_Line_config"%L, "password%d"%l) +"\n")
        
        #sending  exit
        remote_ssh.send("exit\n")
        time.sleep(2)
        
        print remote_ssh.recv(1000)
    #sending back to user-mode signal
    remote_ssh.send("exit\n")


def interface(remote_ssh,L):
    
    #intiallizing of task 
    for l in range(int(config("c").get("Host%d_Interface_config"%L, "no_of_task"))) :
        
        
        # sending interface cmd
        remote_ssh.send("interface "+ config("c").get("Host%d_Interface_config"%L, "interface%d"%l) +"\n")
        time.sleep(1)
        
        #configuring ip & subnet
        remote_ssh.send("ip address "+ config("c").get("Host%d_Interface_config"%L, "ip_subnet%d"%l) +"\n")
        time.sleep(1)
        
        #sending state config
        if config("c").get("Host%d_Interface_config"%L, "state%d"%l) =="up":
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
    
    
    
    