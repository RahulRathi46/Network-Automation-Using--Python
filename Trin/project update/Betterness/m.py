import Func_Def, os, getpass, sys, time


f=Func_Def
x1="0" 


def wall():
    os.system('clear')
    print "\n"
    print ("                                    Welcome   ") + getpass.getuser() + "@" + sys.platform + "\n"
    print " ..._...|..____________________, ,"
    print "....../ `---___________----_____|]"
    print "...../_==o;;;;;;;;_______.:/"
    print ".....), ---.(_(__) /"                      
    print "....// (..) ), ----"
    print "...//___//"                      
    print "..//___//"
    print ".//___// "
    print        "                            %s \n" %time.asctime(time.localtime())
    print "               This a Prototype for Automation Router Configuration     "
    print "                               lets test it out !!    " + "\n"*2
    print "                PreRequest for the script is PYTHON and Router with "
    print "                   SSH enabled and as well as configured"+"\n"


def Descriptor():
    print "#--------------------------------------------------------------------------------------------#"
    print "Author : " + "Er. Rahul Rathi"  +    "COMPATABLE WITH : GNU/LINUX".rjust(46) 
    print "DEVLOPMENT Platform : " +"GNU/LINUX(UBUNTU)" + "COMMUNICATE ME ON : VANGIEX.RR@GMAIL.COM ".rjust(45)
    print "Written in : " + "2015" + "FOLLOW ME ON FB".rjust(41)
    print"#--------------------------------------------------------------------------------------------#" +"\n"
    
    
def exit_fun():
    print "\n"*2
    print ("SSH connection "  +"&"+" Interactive SSH session Closed \n").rjust(70)
    print "\n"*3
    Descriptor()
    print "\n"*2
    print "##############################".rjust(50)
    print " GOOD BYE ".rjust(35) +  getpass.getuser() + "@" + sys.platform
    print "##############################".rjust(50)
    print "\n"*3
      
def init_host():
    print"\n"
    x1=raw_input("1.Host1\t2.Host2\t3.Host3 [And So On ! ] : ")
    print"\n"
    return x1

       

wall()

Descriptor()

print"\n"

while(1):
    print "\n"
    
    print "0.Exit "+"1.Interface Config " + "2.Line Config " + "3.Get_State "+"4.Save State "+"5.Host_config"
   
    print "\n"
    x=raw_input("Enter the choice : ")
    if x=="0":
        os.system("clear")
        exit_fun()
        break 
    elif x=="5":
        x1=init_host()
        os.system("clear")
    else :
        os.system("clear")
        f.connect_ssh(x,int(x1)+1)
    
        

    





    


