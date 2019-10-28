import Func_Def, os, getpass, sys, time


f=Func_Def
x1 = "0" 


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
    print "#--------------------------------------------------------------------------#"
    print "Author : Er.Rahul Rathi".ljust(43)+"DEVLOPMENT Platform : GNU/LINUX".ljust(10)
    print "COMMUNICATE ME ON : VANGIEX.RR@GMAIL.COM ".ljust(43)+"COMPATABLE WITH : GNU/LINUX".ljust(10)
    print "FOLLOW ME ON FB".ljust(43) + "Written in : 2015".ljust(10) 
    print"#--------------------------------------------------------------------------#" +"\n"
    
    
def exit_fun():
    print "\n"*2
    print ("SSH connection "  +"&"+" Interactive SSH session Closed \n").rjust(60)
    print "\n"*3
    Descriptor()
    print "\n"*2
    print "##############################".rjust(47)
    print " GOOD BYE ".rjust(32) +  getpass.getuser() + "@" + sys.platform
    print "##############################".rjust(47)
    print "\n"*3
      


def menu():
    print "-------------------------> MENU <---------------------------\n\n".ljust(31)
    print "1.Interface Config ".ljust(21)+"4.Get_State".rjust(10)+"7.Exit ".rjust(15)
    print "2.Line Config ".ljust(21)+"5.Save State".rjust(10)
    print "3.Routing config ".ljust(21)+"6.Host_config".rjust(10)
    print "\n\n----------------------------> <-----------------------------".ljust(31)
    
    
    
def core() :
    while(1):
        print "\n"
        menu()
        print "\n"
        x=raw_input("Enter the choice : ")
        if x=="7":
            os.system("clear")
            exit_fun()
            break 
        elif x=="6":
            os.system("clear")
            x1=f.init_host()
            os.system("clear")
        else :
            os.system("clear")
            f.connect_ssh(x,(int(x1)+1))
            
#main()            
wall()
Descriptor()
print"\n"
print"INSTALLING CORE FUNCTIONS".rjust(51)
time.sleep(05)
os.system("clear")
core()
        
            

    





    


