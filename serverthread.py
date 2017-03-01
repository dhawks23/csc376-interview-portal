# Copyright 2016. DePaul University. All rights reserved. 
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

import sys
import threading
import socket
import sqlite3

class ServerThread(threading.Thread):    
    def __init__(self, client_socket, connection_id):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self._USER_NAME = ''
        self._USER_PW = ''
        self.connection_id = connection_id

    def terminate_session(self):
        print('Terminating connection', self.connection_id)
        sys.stdout.flush()
        self.client_socket.close()
        print('Socket closed')
        sys.stdout.flush()
     
      
    # =========================================================================
    #             INTERVIEW CREATION   
    # Status: Incomplete
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
    # - test/refine loop control
    # =========================================================================
    def create_interview(self):
        
        # interview creation intro
        self.client_socket.send( ('Interview Creation').encode() )
        
        # interview name entry
        self.client_socket.send( ('Enter a name for the interview').encode() )
        name = self.client_socket.recv(1024)
        
        # < name recorded here >
        
        # INTERVIEW CREATION LOOP
        while(True):
            
            # verification loop
            while(True):            
                
                # question entry
                self.client_socket.send( ('Enter a question').encode() )
                print('You entered:')
                print(self.client_socket.recv(1024))
                
                # question verification (verification loop control)
                self.client_socket.send( ('Add this question to the interview? Y/N').encode() )
                verify = self.client_socket.recv(1024)
                
                # Y: link question to interview (terminate loop)
                if verify == 'Y':
                    # <PROTOCOL: record question to database >
                    self.client_socket.send( ('Question added to interview.').encode() )
                    break
                # N: re-enter question (repeat loop)
                elif verify == 'N':
                    continue
                # invalid (error msg)
                else:
                    self.client_socket.send( ('Invalid Input!  Please answer with Y or N').encode() )
                    
            # interview progression (interview creation loop control)
            self.client_socket.send( ('Would you like to add another question? Y/N').encode() )
            response = self.client_socket.recv(1024)
            
            # N: submit interview to database (terminate loop)
            if response == 'N':
                # <PROTOCOL: interview added to database >
                self.client_socket.send( ('Interview added to database.').encode() )
                break
            # Y: continue adding questions (repeat loop)
            elif response == 'Y':
                continue
            # invalid response (error msg)
            else:
                self.client_socket.send( ('Invalid Response!').encode() )
        
        # post-interview completion options
        self.client_socket.send( (')What would you like to do now? (choose one)').encode() )
        self.client_socket.send( ('A: Assign recently completed interview to interviewee(s)').encode() )
        self.client_socket.send( ('I: Create another interview').encode() )        
        self.client_socket.send( ('Q: Log out and return to main menu').encode() )
        option = self.client_socket.recv(1024)
        
        # A: assign interview (terminate loop)
        if option == 'A':
            # <PROTOCOL: assignment function/process here >
            pass
        # I: create another interview (repeat loop)
        elif option == 'I':
            pass
        # Q: return to main menu (terminate loop)
        elif option == 'Q':
            # <ENCRYPTION: redirect to main menu >
            pass
        # invalid response (error msg)
        else:
            self.client_socket.send( ('Invalid Response!').encode() )   
        
        # remove pass when code is complete
        pass
    
        # ===========================================================================
    #             INTERVIEW ASSIGNMENT   
    # Status: Incomplete
    # 
    # Precondition(s): 
    # - completed interview
    # - interviewee exists
    #
    # Postcondition:
    # - interviewee can access interview
    #
    # TO DO
    # - encrypt/decrypt messages
    # - add database interactions:
    #   - assign interview to interviewee Inbox 
    # - finalize interview assignment design (e.g. single or multiple assignment?)
    # =============================================================================
    def assign_interview(self):
        
        # < followup on interview creation or unique menu? >
        self.client_socket.send( ('Interview Assignment').encode( ))

        #Recieves a username from client
        User_Search = self.client_socket.recv(1024).decode()

        ###CHECK DATABASE FOR###
        # import sqlite3 first
        conn= sqlite3.connect( 'interview.db' )
        conn.row_factory = sqlite3.Row
        User_Row = conn.execute("SELECT user_name FROM Users WHERE user_name = ?", User_Search).fetchone() 

        #if no existing user
        while User_Row == None: #invalid user
            self.client_socket.send( ('User does not exist, try again.').encode() )
            if User_Search == 'quit':
                return
            User_Search = self.client_socket.recv(1024).decode()
            conn.row_factory = sqlite3.Row
            User_Row = conn.execute("SELECT user_name FROM Users WHERE user_name = ?", User_Search).fetchone() 
        
        self.client_socket.send( ('User exists').encode() )#user_conf
        User_Found = User_Row['user_name']
        
        #else
        #Recieves a interview from client


        Interview_Search = self.client_socket.recv(1024).decode()

        ###CHECK DATABASE FOR INTERVIEW###
        conn.row_factory = sqlite3.Row
        Interview_Row = conn.execute("SELECT interview_name FROM Interviews WHERE interview_name = ?", Interview_Search).fetchone()


        #if no existing user
        while Interview_Row == None:
            self.client_socket.send( ('Interview does not exist, try again.').encode() )
            if Interview_Search == 'quit':
                return
            Interview_Search = self.client_socket.recv(1024).decode()
            conn.row_factory = sqlite3.Row
            Interview_Row = conn.execute("SELECT interview_name FROM Interviews WHERE interview_name = ?", Interview_Search).fetchone() 
        Interview_Found = Interview_Row['interview_name']

        self.client_socket.send( ('Assigning Interview').encode() ) #interview_conf

        ###ADD INTERVIEW TO USER'S INBOX###

        self.client_socket.send( (Interview_Search + " has been assigned to " + User_Search + ".").encode() ) #interview_conf

        conn.close()
        pass
    
    # ===========================================================================
    #             INTERVIEW REVIEW  
    # Status: Incomplete
    # 
    # Precondition(s):
    # - assigned interview completed by interviewee
    # - interview recorded in database
    #
    # Postcondition: 
    # - can be viewed by Lawyer/Staff
    #
    # TO DO
    # - encrypt/decrypt messages
    # - add database interactions
    # - finalize interview review design 
    # =============================================================================
    def review_interview(self):

        # interview review intro
        self.client_socket.send( ('Interview Inbox').encode() )
        
        # interview retrieval
        # < search criteria? name, id? >
        self.client_socket.send( ('').encode() )
        self.client_socket.recv(1024)
        
        # < retrieve interview from database >
        # < send ID details >
        self.client_socket.send( ().encode() )
        
        # < INTERVIEW QUESTIONS LOOP >
        
        pass
        
    # ===========================================================================
    #             TAKE INTERVIEW   
    # Status: Incomplete
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
    # - ENCRYPTION: add redirect to main menu
    # - test/refine loop control
    # =============================================================================
    def take_interview(self):
        
        # INTERVIEW LOOP
        while(True):
            
            # interview review intro
            self.client_socket.send( ('Your available interviews:').encode() )
            # <PROTOCOL: generate interviewee's interview list from database >
            # display <none> if none exist
            
            # interview selection <PROTOCOL: search criteria?>
            self.client_socket.send( ('Select an interview to take').encode() )
            self.client_socket.recv(1024)
        
            # <PROTOCOL: 
            #    - retrieve interview based on criteria
            #    - generate loop for each question
            #    - for each question, ask for answer, link it to question
            #    - add interview to review list>
        
            self.client_socket.send( ('Interview complete').encode() )
            
            # post-interview options (interview loop control)
            self.client_socket.send( ('What would you like to do now? (choose one)').encode() )
            self.client_socket.send( ('I: Take another interview').encode() )
            self.client_socket.send( ('Q: Log out and return to main menu').encode() )
            option = self.client_socket.recv(1024)
            
            # I: take another interview (repeat loop)
            if option == 'I':
                continue
            # Q: return to main menu (terminate loop)
            elif option == 'Q':
                # <ENCRYPTION: redirect to main menu>
                break
            # invalid response
            else:
                self.client_socket.send( ('Invalid Input!').encode() )
        
        # remove pass when code is done
        pass
    
    # ===========================================================================
    #             MANAGE INTERVIEW   (extra feature)
    # Status: Incomplete
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
    def manage_interview(self):
        
        # EDIT INTERVIEW LOOP
        while(True):

            # edit options (edit interview loop control)
            self.client_socket.send( ('What would you like to do? (choose one)').encode() )
            self.client_socket.send( ('E: Edit/View an interview').encode() )
            self.client_socket.send( ('D: Delete an interview').encode() )
            self.client_socket.send( ('Q: Log out and return to main menu').encode() )
            option = self.client_socket.recv(1024)
            
            # E: edit interview (go through edit process then repeat loop)
            if option == 'E':
                # interview summary
                self.client_socket.send( ('Created Interviews:').encode() )
                # <PROTOCOL: generate interview list from database >
                # display <none> if none exist
                
                # interview selection <PROTOCOL: search criteria?>
                self.client_socket.send( ('Select an interview to edit').encode() )
                self.client_socket.recv(1024)
        
                # <PROTOCOL: 
                #    - retrieve interview based on criteria
                #    - ask for name change; if yes, make database changes
                #    - generate loop for each question
                #    - ask for question edit; if yes, make database changes>
        
                self.client_socket.send( ('All changes saved.').encode() )
            # D: delete interview (go through delete process then repeat loop)
            elif option == 'D':
                # interview summary
                self.client_socket.send( ('Created Interviews:').encode() )
                # <PROTOCOL: generate interview list from database >
                # display <none> if none exist
                
                # interview selection <PROTOCOL: search criteria?>
                self.client_socket.send( ('Select an interview to delete').encode() )
                self.client_socket.recv(1024)
        
                # <PROTOCOL: delete interview from database>
                self.client_socket.send( ('Interview removed.').encode() )
            # Q: return to main menu (terminate loop)
            elif option == 'Q':
                # <ENCRYPTION: redirect to main menu>
                break
            # invalid response
            else:
                self.client_socket.send( ('Invalid Input!').encode() )
                        
        # remove pass when code is done
        pass


    def run(self):
    #greet and request username and password
        self.client_socket.send( ('Greetings to the Interview Portal').encode() )

        self._USER_NAME = str(self.client_socket.recv(1024).decode())
        self._USER_PW  = str(self.client_socket.recv(1024).decode())

        ##Authentication stuff
        ##
        ##
        _LOGIN_STATUS = (self._USER_NAME == self._USER_PW)

        #_LOGIN_STATUS = self.validate()
       
        if _LOGIN_STATUS == True:
            self.client_socket.send( ('2').encode() )
            response = str(self.client_socket.recv(1024).decode())
            print(response)
            if response == '1':
                self.create_interview()
                return
            elif response == '2':
                self.review_interview()
                
            elif response == '3':
                self.assign_interview()
                return
            elif response == '4':
                self.manage_interview()
                return
            elif response == '4':
                self.take_interview()
                return
        else:
            self.client_socket.send( ("Invalid Username").encode() )

            self.terminate_session()
            return


        self.terminate_session()
         
