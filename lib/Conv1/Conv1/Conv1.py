import re
from random import randint
import time

class Character:

    def __init__(self):
        self.first_name=""
        self.last_name=""
        self.personality="1000"


class Conversation:

    def __init__(self):
        self.char_list=[]    #List of involved characters
        words=open('Words.txt','r')
        senten=open('Sentences1.txt','r')
        self.sentences=[]
        for line in senten:
            self.sentences.append(line)

    def add_char(self, new_char):
        self.char_list.append(new_char) #Adds the new character to the list

    def rem_char(self,leave_char):
        self.char_list.remove(leave_char)

    def end_conv(self):
        self.char_list=[]

    def talk(self, char_num):
        talking=self.char_list[char_num]    #The character who is speaking
        talking_values=talking.personality  #Grab their personaility from their object
        possible_statements=[]
        for row in range(0,len(self.sentences)-1):         #A list of possible sentences
            line_info=self.sentences[row].split(" | ")
            if line_info[0]==talking_values:    #How well does the sentence match the personality
                possible_statements.append(line_info[1][:-1])
        if len(possible_statements)>0:      #If we have well-matched statements
            which_statement=randint(0,len(possible_statements)-1)   #Pick one at random
            statement=possible_statements[which_statement]
        else:   #Otherwise, leave the conversation
            statement="Goodbye"
            self.rem_char(self.char_list[char_num])
        print "\""+statement+"\" said "+talking.first_name+ "\n"    #Display the statements
        time.sleep(1)
        next_talking=randint(0,len(self.char_list)-1)
        if(len(self.char_list)>1):
            while (next_talking==char_num):  
                next_talking=randint(0,len(self.char_list)-1)
            self.talk(next_talking)
        else:
            print "End of Conversation"

Steve=Character()
Steve.first_name="Steve"

Carl=Character()
Carl.first_name="Carl"

Joe=Character();
Joe.first_name="Joe"

Conv1=Conversation();
Conv1.add_char(Steve)
Conv1.add_char(Carl)

Conv1.talk(0)



