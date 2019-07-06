import socket, select
from threading import *

#Function to send message to all connected clients
def send_to_all (sock, message):
	#Message not forwarded to server and sender itself because server is also a part of the connected list to socket
	for socket in connected_list:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :
				# if connection not available
				socket.close()
				connected_list.remove(socket)
				


if __name__ == "__main__":
	connected_list = []			#all the server and clients connected to the socket
	user_record = {}			#the dictionary containing address and usernames of each client connected 
	host = 'localhost'
	port = 12345
	buffer = 4096				#buffer value already defined
	server_socket = socket.socket()
	server_socket.bind((host , port))
	server_socket.listen(20)
	connected_list.append(server_socket)
	print ("THE SERVER IS WORKING WITH 0 CONNECTIONS RIGHT NOW ")        #because rit now no-one is connected with the server
	while 1:
		rList,wList,error_sockets = select.select(connected_list,[],[])		#readable connections from the connected list stored here
		for sock in rList:
			if sock == server_socket:
				connection, addr = server_socket.accept()
				#start_new_thread(threaded ,(connection, addr))
				username = connection.recv(buffer)
				connected_list.append(connection)
				user_record[addr]=""		#record's value initialised as null before confirmation
				

				if username in user_record.values():
					connection.send("Username already taken! BYE BYE \n")
					del user_record[addr]
					connected_list.remove(connection)
					connection.close()
					continue
				else:
					user_record[addr] = username
					length = len(connected_list) -1	
					print length
					connection.send("Welcome to chat room. Enter 'bye' or 'tata' or 'exit' anytime to exit\n")
					send_to_all(connection, username+" joined the conversation\n")		#sends message to all the clients
			else:
				try:
					data1 = sock.recv(buffer)
					data=data1[:data1.index("\n")] #reads till the end of the 1st line
                    
                    #get addr of client sending the message
					m, n =sock.getpeername() #because address is an array of 2 values so it should be stored in 2 variables
					if data == "tata" or data == "exit" or data == "bye" :
						msg= user_record[(m,n)]+" left the conversation\n"
						send_to_all(sock,msg)
						print "Client (%s, %s) is offline" % (m,n)," [",user_record[(m,n)],"]"
						del user_record[(m,n)]
						connected_list.remove(sock)
						sock.close()
						length = len(connected_list) -1	
						print length
						continue

					else:
						msg= user_record[(m,n)]+": " +data+"\n"
						send_to_all(sock,msg)
            
                #abrupt user exit
				except:
					(m,n)=sock.getpeername()
					send_to_all(sock, user_record[(m,n)]+" left the conversation unexpectedly\n")
					print "Client (%s, %s) is offline (error)" % (m,n)," [",user_record[(m,n)],"]\n"
					del user_record[(m,n)]
					connected_list.remove(sock)
					sock.close()
					length = len(connected_list) -1	
					print length
					continue

	server_socket.close()


