# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

#from interview_error import CredentialsException

def terminate_session():
    print('Terminating connection to server')
    for i in range(0,10):
        print('.', end = '')
        sys.stdout.flush()
    ssl_socket.close()
    print('Server socket closed')
    return

def adminMenu(ssl_socket):
    print("What would you like to do?")
    print("(1) create interview")
    print("(2) review interview")
    print("(3) assign interview")
    print("(4) List users")
    print("(q) Log out and exit")

    response = str(input(" > "))

    ssl_socket.send((response).encode())

    confirmation = ssl_socket.recv(1024).decode()
    print(confirmation)
    while True:
        if response == '1':
            createInterview()
            break
        elif response == '2':
            reviewInterview()
            break
        elif response == '3':
            assignInterview()
            break
        elif response == '4':
            listUsers()
            break
        else:
            #print()
            #terminate_session()
            #if (len(response) != 0): print(response)
            sys.stdout.flush()
            return
            #answer_string = str(input(" > "))
            #answer_string = enc.encrypt(answer_string)
            #ssl_socket.send(answer_string)
            #response = ssl_socket.recv(1024)
            #response = enc.decrypt(response)



# =========================================================================
#             LAWYER: INTERVIEW CREATION   
# Status: Incomplete (skeleton finished)
# 
# Precondition: 
# - Lawyer/Staff access
# - create interview option selected
#
# Postcondition:
# - interview recorded in database
#
# TO DO
# - PROTOCOL: add database interactions
# - ENCRYPTION: add redirect to main menu
# - SYNC: test/refine loop control
# =========================================================================

def create_interview():
    
    # incoming intro message
    intro_msg = client_socket.recv(1024)
    if(len(intro_msg) != 0):
        print(intro_msg)
    
    # incoming name entry request
    name_msg = client_socket.recv(1024)
    if(len(name_msg) != 0):
        print(name_msg)
    
    # outgoing name submission
    name_entry = str(input(' > '))
    client_socket.send(name_entry)
    
    ## INTERVIEW CREATION LOOP ##
    while(True):
        
        ## question verification loop ##
        while(True):
            
            # incoming question entry request
            question_msg = client_socket.recv(1024)
            if(len(question_msg) != 0):
                print(question_msg)
            
            # outgoing question submission (String)
            question_entry = str(input(' > '))
            client_socket.send(question_entry)
            
            # incoming question echo
            echo = client_socket.recv(1024)
            if(len(echo) != 0):
                print(echo)
            
            # incoming verify request
            verify_msg = client_socket.recv(1024)
            if(len(verify_msg) != 0):
                print(verify_msg)
            
            # outgoing verification (String) Y/N
            verify_entry = str(input(' > ')) 
            client_socket.send(verify_entry)
            
            ## INNER LOOP CONTROL ##
            # Y: save question (terminate loop)
            if verify_entry == 'Y':
                
                # incoming confirmation message
                confirm_msg = client_socket.recv(1024)
                if(len(confirm_msg) != 0):
                    print(confirm_msg)
                break
            
            # N: redo question (loop again)
            elif verify_entry == 'N':
                continue
            
            # invalid response
            else:
                invalid_resp = client_socket.recv(1024)
                if(len(invalid_resp) != 0):
                    print(invalid_resp)    
        
        ## OUTER LOOP CONTROL ##
        
        # incoming request for more questions
        add_msg = client_socket.recv(1024)
        if(len(add_msg) != 0):
            print(add_msg)
        
        # outgoing response (String) Y/N
        add_resp = input(str(' > '))
        client_socket.send(add_resp)
        
        # N: add new interview to database (terminate loop)
        if add_resp == 'N':
            
            # incoming confirmation message
            db_msg = client_socket.recv(1024)
            if(len(db_msg) != 0):
                print(db_msg)
            break
        
        # Y: add more questions (loop again)
        elif add_resp == 'Y':
            continue
        
        # invalid response
        else:
            invalid_resp = client_socket.recv(1024)
            if(len(invalid_resp) != 0):
                print(invalid_resp)    
        
        ## post-interview display ##
        
        # <PROTOCOL: retrieve interview from database and display full details?>
        
        # END create_interview: back to Lawyer Options
    
    # remove pass when code is complete
    pass
       
# ===========================================================================
#             LAWYER: INTERVIEW ASSIGNMENT   
# Status: Incomplete
# 
# Precondition(s): 
# - interview exists
# - interviewee exists
#
# Postcondition:
# - interviewee can access interview
#
# TO DO
# - encrypt/decrypt messages
# - finalize interview assignment design (e.g. single or multiple assignment?)
# =============================================================================

def assignInterview():

	# Get name of Interviewee
	print("Enter the username of the interviewee:")
	user = str(input(" > "))

	#Confirms that the interviewee exists

	ssl_socket.send(( user ).encode()) 									#User_Search
	user_conf = ssl_socket.recv(1024).decode()

	#if no existing user
	while user_conf != "User exists":
		print(user_conf)
		user = str(input(" > "))
		ssl_socket.send(( user ).encode())								#User_Search
		if user == 'quit':
			return
		user_conf = ssl_socket.recv(1024).decode()
		
	print(user_conf)

	# Get name of Interview
	print("Enter the name of the interviewe you wish to assign:")
	interview = str(input(" > "))

	#Confirms that the interview exists

	ssl_socket.send(( interview ).encode())								#Interview_Search
	interview_conf = ssl_socket.recv(1024).decode()			
	#if no existing user
	while interview_conf == "Interview does not exist, try again.":
		print(interview_conf)
		interview = str(input(" > "))
		ssl_socket.send(( interview ).encode())							#Interview_Search
		if interview == 'quit':
			return
		interview_conf = ssl_socket.recv(1024).decode()

	print(interview_conf)	# Assigning Interview
	interview_conf = ssl_socket.recv(1024).decode() #
	print(interview_conf)	# INTERVIEW has been assigned to USER


	pass
    
def review_submissions():
    pass

# ===========================================================================
#             LAWYER: MANAGE INTERVIEWS
# Status: Incomplete (skeleton finished)
# 
# Precondition(s):
# - Lawyer/Staff account session
#
# Postcondition: 
# - interview edited in database, interview deleted from database, or
#   return to main menu
#
# TO DO
# - PROTOCOL: add database interactions
# - ENCRYPTION: add redirect to main menu
# - test/refine loop control
# =============================================================================
def manage_interviews():
    
    ## MANAGE_INTERVIEWS LOOP ##
    while(True):
        
        ## options display ##
    
        # incoming option messages
        option_msg = client_socket.recv(1024)
        option_e = client_socket.recv(1024)
        option_d = client_socket.recv(1024)
        option_q = client_socket.recv(1024)
        
        if(option_msg != 0 and
           option_e   != 0 and
           option_d   != 0 and 
           option_q   != 0    ):
            print(option_msg)
            print(option_e)
            print(option_d)
            print(option_q)
         
        ## LOOP CONTROL ##
            
        # outgoing option response
        option_resp = str(input(' > '))
        client_socket.send(option_resp)
        
        # E: edit/view created interviews
        if option_resp == 'E':
            
            # incoming edit/view intro message
            edit_msg = client_socket.recv(1024)
            if(len(edit_msg) != 0):
                print(edit_msg)
                
            # <PROTOCOL: generate interview list from database >
            # display <none> if none exist
            
            # incoming interview selection message
            select_msg = client_socket.recv(1024)
            if(len(select_msg) != 0):
                print(select_msg)
                
            # outgoing interview selection entry
            select_entry = str(input(' > '))
            client_socket.send(select_entry)
            
            # <PROTOCOL: 
            #    - retrieve interview based on criteria
            #    - ask for name change; if yes, make database changes
            #    - generate loop for each question
            #    - ask for question edit; if yes, make database changes>
            
            # incoming confirmation message
            confirm_msg = client_socket.recv(1024)
            if(len(confirm_msg) != 0):
                print(confirm_msg)
        
        # D: remove created interview
        elif option_resp == 'D':
            
            ## verification loop ##
            while(True):
                
                # incoming delete intro message
                delete_msg = client_socket.recv(1024)
                if(len(delete_msg) != 0):
                    print(delete_msg)
                    
                # <PROTOCOL: generate interview list from database >
                # display <none> if none exist
                
                # incoming interview selection message
                select_msg = client_socket.recv(1024)
                if(len(select_msg) != 0):
                    print(select_msg)
                
                # outgoing interview selection entry
                select_entry = str(input(' > '))
                client_socket.send(select_entry)
                
                ## LOOP CONTROL ##
                
                # incoming verify request
                verify_msg = client_socket.recv(1024)
                if(len(verify_msg) != 0):
                    print(verify_msg)
            
                # outgoing verification (String) Y/N
                verify_entry = str(input(' > ')) 
                client_socket.send(verify_entry)
                
                # Y: confirm selection
                if verify_entry == 'Y':
                    
                    # incoming confirmation message
                    confirm_msg = client_socket.recv(1024)
                    if(len(confirm_msg) != 0):
                        print(confirm_msg)
                    break
                
                # N: redo selection
                elif verify_entry == 'N':
                    continue
                
                # invalid response
                else:
                    
                    invalid_resp = client_socket.recv(1024)
                    if(len(invalid_resp) != 0):
                        print(invalid_resp)    
                
        
        # Q: return to Lawyer Options
        elif option_resp == 'Q':
            break
        
        # invalid response
        else:
            
            invalid_resp = client_socket.recv(1024)
            if(len(invalid_resp) != 0):
                print(invalid_resp)    
        
    # remove pass when code is complete    
    pass

# ===========================================================================
#             INTERVIEWEE: TAKE INTERVIEW   
# Status: Incomplete (skeleton finished)
# 
# Precondition(s):
# - interviewee account session
# - interview linked to interviewee
#
# Postcondition: 
# - answers linked to questions of interview in database
#
# TO DO
# - PROTOCOL: add database interactions
# - SYNC: test/refine loop control
# =============================================================================
def take_interview():
    
    # incoming intro message
    intro_msg = client_socket.recv(1024)
    if(len(intro_msg) != 0):
        print(intro_msg)
        
    # assigned interview list
    # <PROTOCOL: generate interviewee's interview list from database?>
    # display <none> if none exist
    
    # incoming interview selection request
    select_msg = client_socket.recv(1024)
    if(len(select_msg) != 0):
        print(select_msg)
    
    # outgoing interview selection entry
    select_entry = input(str(' > '))
    client_socket.send(select_entry)
    
    # <PROTOCOL: 
    #    - retrieve interview based on criteria
    #    - generate loop for each question
    #    - for each question, ask for answer, link it to question
    #    - add interview to review list>
    
    # incoming confirmation message
    confirm_msg = client_socket.recv(1024)
    if(len(confirm_msg) != 0):
        print(confirm_msg)
        
    # END take_interview: return to Interviewee Options
    
    # remove pass when code is complete
    pass



def validate(loggedInAs):
    # KH -- EXCISED PER LICENSING RESTRICTION
    pass
    
# CURRENT CERTIFICATE'S HOSTNAME IS 'localhost'
# won't work if not using 'localhost' unless you create a new certificate with new host address as the certificate's commonName
def ssl_connection(client_socket):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_verify_locations("cert.pem")
    # wrap client_socket, uses RSA encryption, certificate required
    ssl_socket = ssl.wrap_socket(client_socket, ciphers="RSA:!COMPLEMENTOFALL", ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
    # make connection
    ssl_socket.connect((_HOST, _PORT))
    # verify certificate and do handshake
    cert = ssl_socket.getpeercert()
    ssl.match_hostname(cert, _HOST)
    ssl_socket.do_handshake()
    return ssl_socket
    
# use:
# openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
# on the cmd line to generate new certificate (update ssl.match_hostname() parameter)
if __name__ == "__main__":
    import sys
    import socket
    import ssl

    argc = len(sys.argv)

    if (argc != 3):
        _HOST = str(input("Enter HOST name: "))
        _PORT = int(input("Enter PORT number: "))
    else:
        _HOST = str(sys.argv[1])
        _PORT = int(sys.argv[2])

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = ssl_connection(client_socket)

    #Server greets client
    greeting_msg = ssl_socket.recv(1024)
    greeting_msg = (greeting_msg).decode()
    print(greeting_msg)

    #Ask user to login or create new account
    print("(1) Login.")
    print("(2) Create New User.")
    response = str(input("> "))
    ssl_socket.send((response).encode())

    if (response == '2'):
    	new_USER_NAME = str(input("Enter Username: "))
    	ssl_socket.send((new_USER_NAME).encode())
    	USER_AUTH     = str(input("Enter Authorization: "))
    	ssl_socket.send((USER_AUTH).encode())

    #Prompt For Password and Username
    USER_NAME = str(input("Username: "))
    ssl_socket.send((USER_NAME).encode())
    USER_PW   = str(input("Password: "))
    ssl_socket.send((USER_PW).encode())

    confirmation= str(ssl_socket.recv(1024).decode()) # confirms credentials
    print(confirmation)                             #print credentials
    try:
        cred = int(confirmation)
        
    except ValueError:
        terminate_session()
        sys.exit()
        
    if cred == 1:
        print("interviewee")
        #take interview
    elif cred == 2:
        print("lawyer")
        adminMenu(ssl_socket)
        #admin_interface
    elif cred == 3:
        print("other?")
        #review_answers

    terminate_session()
    print("Logging Out...")