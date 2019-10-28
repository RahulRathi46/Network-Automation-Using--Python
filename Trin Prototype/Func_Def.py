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


def connect_ssh(ip,u,p,o):
  

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
    to_do(remote_ssh,o,ssh)
    

    
    
    
def signal(x,w):
    if x=="g":
        w.send("config t\n")
        time.sleep(2)
    else :
        w.send("en\n")
        time.sleep(1)
        w.send("amount\n")
        time.sleep(1)
   





def to_do(w,o,ssh):
    if o=="1":
        signal("u", w)
        signal("g", w)
        
        
    elif o=="2":
        signal("u", w)
        signal("g", w)
        
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
    #session terminiting aftwer every task { applied for security } { you can inscres speed of excution of script by removing this }
    ssh.close()
    
    
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
        
      

    
    

    
