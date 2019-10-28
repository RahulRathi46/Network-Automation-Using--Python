import Func_Def, os, getpass, sys, time


f=Func_Def


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
    
    

Descriptor()
while(1):
    print "\n"
    print "################################# < OPTIONS > #########################################"
    print "0.Exit "+"1.Interface Config " + "2.Line Config " + "3.Get_State "+"4.Save State "
    print "#######################################################################################"
    print "\n"
    x=raw_input("Enter the choice : ")
    if x=="0":
        os.system("clear")
        exit_fun()
        break 
    else:
        os.system("clear")
	#Static Router Address & credentials For Testing Purpose .
        f.connect_ssh("1.1.1.2", "Router1", "amount",x)
    
        

    





    


