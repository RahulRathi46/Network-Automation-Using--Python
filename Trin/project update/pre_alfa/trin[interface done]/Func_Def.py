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


def connect_ssh(ip,u,p):
  

    # Create instance of SSHClient object
    ssh = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    ssh.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())

    # initiate SSH connection
    ssh.connect(ip, username=u, password=p)
    print "SSH connection established to %s \n" % ip

    # establish an 'interactive session'
    remote_ssh = ssh.invoke_shell()
    print "Interactive SSH session established \n"

    # Turn off paging
    disable_paging(remote_ssh)
    to_do(remote_ssh)
    
    
    
def to_do(w):
    w.send("en\n")
    time.sleep(1)
    w.send("amount\n")
    time.sleep(1)
    w.send("config t\n")
    time.sleep(2)
    line(w)
    interface(w)
   
    
    
    print w.recv(100000)
    




def line(w):
    for l in range(int(config("c").get("line_config", "no of task"))) :
        w.send("line "+ config("c").get("line_config", "line%d"%l) +"\n")
        time.sleep(1)
        w.send("logging "+ config("c").get("line_config", "login%d"%l) +"\n")
        w.send("exit\n")
        time.sleep(2)

def interface(w):
    for l in range(int(config("c").get("Interface_config", "no of task"))) :
        w.send("interface "+ config("c").get("Interface_config", "interface%d"%l) +"\n")
        time.sleep(1)
        w.send("ip address "+ config("c").get("Interface_config", "ip_subnet%d"%l) +"\n")
        time.sleep(1)
        if config("c").get("Interface_config", "state%d"%l) =="up":
            w.send("no sh"+"\n")
        else :
            w.send("sh\n")
            time.sleep(1)
            w.send("exit\n")
            w.send("\n")
            time.sleep(1)
    w.send("exit\n")
    w.send("exit\n")
    time.sleep(1)
    get_state(w)
    
    

    
def get_state(w):
    w.send(config("d").get("get_state", "ip_interface")+"\n")
    time.sleep(2)
    
    

    
    
    
    

    
