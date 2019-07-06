import socket
import select
import string
import sys
import time
import getpass
import MySQLdb

def main():

    host = 'localhost'
    port = 12345
    conn = MySQLdb.connect(host = 'localhost' , database = 'mydb' , user ='root' , password = 'bhavesh27')
    cursor = conn.cursor()
    print("YOU ARE GOING TO CONNECT WITH YOUR PARTNERS IN A FEW MOMENTS")
    time.sleep(2)
    #asks for user name
    name=raw_input("Enter username:")
    password= getpass.getpass()
    cursor.execute("select * from userdb")
    row = cursor.fetchall()
    if name == row[0] && password == row[1]:
	continue
    else
	sys.exit()
    s = socket.socket()
    s.settimeout(2)
    
    # connecting host
    try :
        s.connect((host, port))
	f = open('your_messages.txt' , 'a+')
    except :
        print " Can't connect to the server"
        sys.exit()

    #if connected
    s.send(name)
  
    while 1:
        socket_list = [sys.stdin, s]
        
        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list , [], [])
        
        for sock in rList:
            #incoming message from server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print 'BYE HAVE A GOOD DAY!!\n'
                    sys.exit()
                else :
                    sys.stdout.write(data)
		    f.write(data)
                  
        
            #user entered a message
            else :
                msg=sys.stdin.readline()
		f.write(msg)
                s.send(msg)
		
    f.close()
if __name__ == "__main__":
    main()
