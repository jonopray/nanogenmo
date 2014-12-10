import re
from random import randint
import time
import math

class Character:

    def __init__(self):
        self.first_name=""
        self.last_name=""
        self.personality="1000"
        self.extroversion=0


class Conversation:

    def __init__(self):
        self.char_list=[]    #List of involved characters
        wor=open('Words.txt','r')
        senten=open('Sentences1.txt','r')
        self.sentences=[]
        for line in senten:
            self.sentences.append(line)
        self.words=[]
        for line in wor:
            self.words.append(line)

    def addChar(self, new_char):
        self.char_list.append(new_char) #Adds the new character to the list

    def remChar(self, leave_char):
        self.char_list.remove(leave_char)

    def startConv(self):
        next_talking=randint(0,len(self.char_list)-1)
        while(len(self.char_list)>1):
            spoke=self.talk(next_talking)
            while (next_talking==spoke):  
                next_talking=randint(0,len(self.char_list)-1)

    def endConv(self):
        self.char_list=[]

    def talk(self, char_num):
        talking=self.char_list[char_num]    #The character who is speaking
        talking_values=talking.personality  #Grab their personaility from their object
        possible_statements=[]
        for row in range(0,len(self.sentences)-1):         #A list of possible sentences
            line_info=self.sentences[row].split(" | ")
            if self.personalityFit(line_info[0],char_num):    #How well does the sentence match the personality
                possible_statements.append(line_info[1][:-1])
        if (len(possible_statements)>0 and talking.extroversion>0):      #If we have well-matched statements
            which_statement=randint(0,len(possible_statements)-1)   #Pick one at random
            statement=possible_statements[which_statement]
            if statement.count("_")>0:
                statement=self.fillML(line_info[0],statement, char_num)   #If the statement is a madlib, fill it.
        else:   #Otherwise, leave the conversation
            statement="Goodbye"
            self.remChar(self.char_list[char_num])
        print "\""+statement+"\" said "+talking.first_name+ "\n"    #Display the statements
        talking.extroversion-=1
        time.sleep(1)
        next_talking=randint(0,len(self.char_list)-1)
        if(len(self.char_list)<2):
            print "End of Conversation"
        return char_num

    def fillML(self, line_info, madlib, char_num):
        talking=self.char_list[char_num]    #The character who is speaking
        talking_values=talking.personality  #Grab their personaility from their object
        number_blanks=madlib.count("_")/2   #Determine the number of blanks: _A_, _V_, etc.
        r_blanks=re.compile("_[A-Z]+_")
        blanks=r_blanks.findall(madlib)     #Uses RE to locate the blanks
        possible_blanks=[]
        for i in range(0,int(float(number_blanks))):
            possible_blanks.append([])
            curr_blank=blanks[i][1:-1]
            for row in range(0,len(self.words)):    #Searches words for valid insertions
                word_info=self.words[row].split(" | ")
                if self.personalityFitML(line_info, word_info, char_num):
                    possible_blanks[i].append(line_info[1][:-1])
            which_choice=randint(0,len(possible_blanks[i])-1)       #Selects insertions at random
            madlib=madlib.replace(blanks[i],possible_blanks[i][which_choice],1)
        return madlib

    def personalityFit(self, statement_info, char_num, *obj_num):    #Evaluates the statement information (.txt info) against the character personality
        personality_values=self.char_list[char_num].personality     #*obj_num are who/what they are talking to/about
        for i in obj_num:
            print i
        match=0
        for i in range(0, min(len(statement_info),personality_values)-1):
            match+=abs(float(statement_info[i])**2-float(personality_values[i])**2)
        if match<1:
            return 1
        else:
            return 0

    def personalityFitML(self, statement_info, word_info, char_num, *obj_num):
        personality_values=self.char_list[char_num].personality
        object_perspective=[]
        #for i in obj_num:
            #object_perspective.append(self.char_list[char_num].perspective[i]);
        match=0
        for i in range(0, min(len(statement_info),personality_values)-1):
            match+=abs(float(statement_info[i])**2-float(personality_values[i])**2)
        for i in range(0, min(len(word_info),personality_values)-1):
            match+=abs(float(word_info[i])**2-float(personality_values[i])**2)
        if match<1:
            return 1
        else:
            return 0




Steve=Character()
Steve.first_name="Steve"
Steve.extroversion=2

Carl=Character()
Carl.first_name="Carl"
Carl.extroversion=3

Joe=Character();
Joe.first_name="Joe"
Joe.extroversion=2

Conv1=Conversation();
Conv1.addChar(Steve)
Conv1.addChar(Carl)
Conv1.addChar(Joe)

Conv1.startConv()
print "Done"



