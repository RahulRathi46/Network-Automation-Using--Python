import ConfigParser
import paramiko
import time


def config(i):
    if i=="c":
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'/home/vx/Desktop/trin.conf'))
        return config
    else:
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'/home/vx/Desktop/trin.confd'))
        return config


def disable_paging(remote_ssh):
    '''Disable paging on a Cisco router'''

    remote_ssh.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_ssh.recv(1000)

    return output


def connect_ssh(ip,u,p,o,M):
  

    # Create instance of SSHClient object
    ssh = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    ssh.connect(ip, username=u, password=p)
    # establish an 'interactive session'
    remote_ssh = ssh.invoke_shell()
    
    
    print "SSH connection established to %s " % ip +"&"+" Interactive SSH session established \n"

    # Turn off paging
    disable_paging(remote_ssh)
    
    #action list
    to_do(remote_ssh,o,ssh,M)
    

    
    
    
def signal(x,w):
    if x=="g":
        w.send("config t\n")
        time.sleep(2)
    else :
        w.send("en\n")
        time.sleep(1)
        w.send("amount\n")
        time.sleep(1)
   




def to_do(w,o,ssh,M):
    
    if M=="0":
        select(o,w)
        #session terminiting aftwer every task { applied for security } { you can inscres speed of excution of script by removing this }
        ssh.close()
       
    else :
        for l in range(int(config("c").get("Miscellaneous_config", "nodes of config"))) :
            w.send("ssh "+"-l "+ config("c").get("Miscellaneous_config", "username%d"%l)+" " +config("c").get("Miscellaneous_config", "host%d"%l)+"\n")
            time.sleep(2)
            w.send(config("c").get("Miscellaneous_config", "password%d"%l)+"\n")
            time.sleep(1)
            w.send("terminal length 0 \n")
        select(o,w)
        #session terminiting aftwer every task { applied for security } { you can inscres speed of excution of script by removing this }
        ssh.close()
                
                
        
    



def select(o,w):
    if o=="1":
        signal("u", w)
        signal("g", w)
        interface(w)
        
    elif o=="2":
        signal("u", w)
        signal("g", w)
        line(w)
        get_state(w,"2")
        
    elif o=="3":
        print("\n#########################################################")
        print ("1.Interface "+"2.running-config "+"3. startup-config")
        print ("#########################################################\n")
        x=raw_input("Enter the choice : ")
        print "\n"
        signal("u", w)
        get_state(w,x)
    elif o=="4":
        print("\n###############################################################################")
        print ("1.Save to startup-Config "+"  "+"2. Get back Running-Config from Startup-Config")
        print ("###############################################################################\n")
        x=raw_input("Enter the choice : ")
        print "\n"
        signal("u", w)
        save(w,x)
        
    else:
        return 0
        
    print w.recv(100000)
        


def line(w):
    #intiallizing of task 
    for l in range(int(config("c").get("Line_config", "no of task"))) :
        
        #sending frist line cmd
        w.send("line "+ config("c").get("Line_config", "line%d"%l) +"\n")
        time.sleep(1)
        
        #sending login cmd 
        if "login" in config("c").get("Line_config", "login%d"%l) :
            w.send(config("c").get("Line_config", "login%d"%l) +"\n")
        else :
            w.send( config("c").get("Line_config", "login%d"%l) +"\n")
        
        #sending password cmd
        if config("c").get("Line_config", "password%d"%l)=="-1" :
            w.send("exit\n")
        else :
            w.send("password "+ config("c").get("Line_config", "password%d"%l) +"\n")
        
        #sending  exit
        w.send("exit\n")
        time.sleep(2)
        
    #sending back to user-mode signal
    w.send("exit\n")

def interface(w):
    
    #intiallizing of task 
    for l in range(int(config("c").get("Interface_config", "no of task"))) :
        
        # sending interface cmd
        w.send("interface "+ config("c").get("Interface_config", "interface%d"%l) +"\n")
        time.sleep(1)
        
        #configuring ip & subnet
        w.send("ip address "+ config("c").get("Interface_config", "ip_subnet%d"%l) +"\n")
        time.sleep(1)
        
        #sending state config
        if config("c").get("Interface_config", "state%d"%l) =="up":
            w.send("no sh"+"\n")
            w.send("exit\n")
            w.send("\n")
            time.sleep(1)
            w.send("exit\n")
            time.sleep(1)
        else :
            w.send("sh\n")
            time.sleep(1)
            w.send("exit\n")
            w.send("\n")
            time.sleep(1)
            w.send("exit\n")
            time.sleep(1)
            
    #sending get_state
    get_state(w,"1")
    
    

    
def get_state(w,x):
    
    #get_state of interface 
    if x=="1":
        w.send(config("d").get("Get_state", "ip_interface")+"\n")
        time.sleep(2)
    #get state of running state
    elif x=="2":
        w.send(config("d").get("Get_state", "running-config")+"\n")
        time.sleep(5)
    #get state of startup
    elif x=="3":
        w.send(config("d").get("Get_state", "startup-config")+"\n")
        time.sleep(5)
        
      
def save(w,x):
    
    #get state save to Startup-config
    if x=="1":
        w.send(config("d").get("Save_change", "to_startup-config")+"\n")
        w.send("\n")
        
    #get state save to running-config
    elif x=="2":
        w.send(config("d").get("Save_change", "to_running-config")+"\n")
        w.send("\n")
   
    time.sleep(5)
    
    
    

    
