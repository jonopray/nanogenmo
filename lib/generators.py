# Written by Jonathan Opray
# Credit to treyhunner for the name generation https://github.com/treyhunner

from random import choice
from random import randint
from random import sample
from name import get_first_name
from name import get_last_name

class Character:
	genders = ["male", "female"]
	trait_categories = ["intelligence", "strength", "charisma", "kindness", "competence", "resolve", "honesty", "age", "extraversion", "status", "mood", "attractiveness", "pride", "curiosity"]
	dist = [1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5];
	#trait_category_scales = {"intelligence" : ["moron", "foolish"]}

	#traits_1 = ["loyal", "opportunist", "selfish", "deceiptful", "stubborn", "pragmatic", "resolute"] # loyalties
	#traits_2 = ["weak", "thin", "flabby", "fat", "strong"] # physical
	#traits_3 = ["silent", "mean", "kind", "boring", "charismatic", "talkative"] # persona
	# appearance (hair, eyes, nose)

	@staticmethod
	def generate(character_id, allegiances):
		character = Character()
		character.id = character_id
		character.gender = choice(Character.genders)
		character.first_name = get_first_name(character.gender)
		character.last_name = get_last_name()
		character.allegiance = choice(allegiances)
		character.generate_traits()

		character.knowledge = {} # a dictionary of plot_id : [location bool, subject bool, verb bool, object bool]
		# character.job/position? has a location
		character.relationships = {} # a dictionary of character name : 1-5 describing how close, 3 neutral
		character.goals = []

		# TODO: process traits into archetype for character
		return character

	def generate_traits(self):
		# TODO: Bias traits on a per trait level when generating. Most traits should bias in the middle
		# TODO: Correlate traits (status and pride, age and strength/intelligence)
		self.traits = {category : choice(self.dist) for category in Character.trait_categories}

	@staticmethod
	def generate_npc():
		character = Character.generate()
		character.traits['strength'] = randint(1,3)
		character.traits['intelligence'] = randint(1,3)
		character.traits['status'] = randint(1,3)
		character.traits['resolve'] = randint(1,3)
		return character

	def act(self, world):
		pass
		# Look at current goal and figure out what to do next.
		# Do we want to do something with a person?

	# if same allegiance and both high status, familial
	# if similar strength and intelligence, familial
	# if familial and differing ages, parent or uncle if parent exists
	# if conflicting values of kindness, enemies
	# if not family, and not enemies
	def create_relationship(self, other):
		#TODO: exception for age = 1. Should either be familial or maybe friends if same age
		possible_relationships = []
		
		family_difference = 0
		for trait in ['status', 'intelligence', 'charisma', 'strength']:
			family_difference += abs(self.traits[trait] - other.traits[trait])
		if self.allegiance != other.allegiance:
			family_difference += 5
		values_difference = 0
		for trait in ['intelligence', 'kindness', 'honesty', 'status', 'attractiveness']:
			values_difference += abs(self.traits[trait] - other.traits[trait])

		if (self.allegiance == other.allegiance and self.traits['status'] >= 4 and \
			other.traits['status'] >= 4) or family_difference <= 3:
			possible_relationships.append('familial')
		
		if self.allegiance == other.allegiance and self.traits['status'] >= 2 and \
			other.traits['status'] >= 2 and self.traits['status'] != other.traits['status']:
			possible_relationships.append('political')

		if self.gender != other.gender and self.traits['mood'] > 2 and \
			other.traits['mood'] > 2 and values_difference <= 4:
			possible_relationships.append('romantic interest')

		# TODO: each character should have a different view of the other.
		# proud, mean, moody people of different allegiances should be enemies
		malice = 21
		malice = malice + self.traits['pride'] + other.traits['pride']
		malice = malice - self.traits['kindness'] - other.traits['kindness']
		malice = malice - self.traits['mood'] / 2 - other.traits['mood'] / 2
		malice = malice - 2 * abs(self.traits['age'] - other.traits['age'])
		if self.allegiance != other.allegiance:
			malice += 3
		if malice >= 23:
			possible_relationships.append('enemy')

		if malice <= 15 and values_difference <= 9:
			possible_relationships.append('friend')

		# If two randos are forced to have a relationship, sometimes they shouldn't
		if len(possible_relationships) == 0:
			if randint(1,3) == 1:
				possible_relationships.append('acquaintance')
			else:
				return 0

		# Pick the possible relationship to be the relationship
		relationship = choice(possible_relationships)

		# Categorize by age
		# enemies, friends, and acquaintances can just be that
		if relationship == "enemy" or relationship == "friend" or \
			relationship == "acquaintance" or relationship == "romantic interest":
			self.relationships[other.id] = relationship;
			other.relationships[self.id] = relationship;
		elif relationship == "familial":
			if self.traits['age'] == other.traits['age']:
				self.relationships[other.id] = "sibling"
				other.relationships[self.id] = "sibling"
			elif self.traits['age'] < other.traits['age']:
				self.relationships[other.id] = "parent";
				other.relationships[self.id] = "child";
			else:
				self.relationships[other.id] = "child";
				other.relationships[self.id] = "parent";
		elif relationship == "political":
			if self.traits['status'] > other.traits['status']:
				# TODO: Can't have two masters?
				self.relationships[other.id] = "subordinate";
				other.relationships[self.id] = "master";
			else:
				self.relationships[other.id] = "master";
				other.relationships[self.id] = "subordinate";
		"""
		# Print out the relationship
		print(other.full_name() + " is " + self.full_name() + "'s " + self.relationships[other.id])
		print(self.full_name() + " is " + other.full_name() + "'s " + other.relationships[self.id])
		self.print2()
		other.print2()
		"""
		return 1

	def generate_goals(self):
		self.goals = ["protect self"]
		self.generate_goal()

	goals = ["entertain self", "protect PERSON", ""]
	# NEED TO GENERATE CHARACTERS AND FORM RELATIONSHIPS FIRST, BEFORE DECIDING GOALS
	def generate_goal(self):
		# Motivations: is there a person we care about? Are we high status?
		#["intelligence", "strength", "charisma", "kindness", "competence", "resolve", "honesty", "age", "extraversion", "status", "mood", "attractiveness", "pride"]
		# High status, pride, and lots of subordinates: want to conquer/do something for self
		# Strength, resolve, kindness, and a close bond: protect that person
		# Age = 1: no goals. Age = 2: "follow X (caretaker?)" or "see world"/"find home" if no caretaker
		# Age = 3-4: do anything, Age = 5: "find home", "do job"
		# Any master: "obey X" should be present
		# High extraversion, charisma, and intelligence: "entertain self"
		# Kindness of 1: abuse others?
		# High strength and pride: confront enemy
		# Character with a job: do job
		age = self.traits['age']
		if age == 1:
			return
		elif age == 2:
			parent = -1
			master = -1
			friend = -1
			for char_id, relationship in self.relationships.items():
				if relationship == "parent":
					parent = char_id
				elif relationship == "master":
					master = char_id
				#elif relationship == "friend": # TODO: if friend is older, then add them here
				#	friend = char_id
			if parent != -1:
				self.goals.append("follow " + str(parent))
			elif master != -1:
				self.goals.append("follow " + str(master))
			return
		
		num_subordinates = 0
		child = -1
		sibling = -1
		interest = -1
		friend = -1
		enemy = -1
		for char_id, relationship in self.relationships.items():
			if relationship == "subordinate":
				num_subordinates += 1
			elif relationship == "master":
				num_subordinates = -1
			elif relationship == "child":
				child = char_id
			elif relationship == "sibling":
				sibling = char_id
			elif relationship == "romantic interest":
				interest = char_id
			elif relationship == "friend":
				friend = char_id
			elif relationship == "enemy":
				enemy = char_id
					
		leadership_score = self.traits['status'] + self.traits['pride'] + num_subordinates #4, 4, 1
		if self.traits['status'] >= 4 and leadership_score >= 9:
			self.goals.append("conquer " + "X") # TODO: Replace "X" with some sort of real target

		guardian_score = self.traits['strength'] + self.traits['resolve'] + self.traits['kindness'] #4, 3, 3
		if child != -1 and guardian_score >= 8:
			self.goals.append("protect " + str(child))
		elif interest != -1 and guardian_score >= 10:
			self.goals.append("protect " + str(interest))
		elif sibling != -1 and guardian_score >= 10:
			self.goals.append("protect " + str(sibling))
		elif friend != -1 and guardian_score >= 12:
			self.goals.append("protect " + str(friend))

		print("leadership: " + str(leadership_score) + " -> 9, guardian: " + str(guardian_score) + " -> 8,10,12")
		# most people don't want to protect anyone or conquer anything... curiosity + resolve -> explore
		if self.traits['curiosity'] + self.traits['resolve'] >= 8:
			self.goals.append("explore world")

		# a lot of people will want to entertain themselves
		if self.traits['extraversion'] >= 3 and randint(1,3) == 1:
			self.goals.append("entertain self")

		if self.traits['attractiveness'] >= 3 and self.traits['mood'] >= 3 and \
			self.traits['extraversion'] >= 3 and interest == -1 and randint(1,2) == 1:
			self.goals.append("find love")
		
		if enemy != -1 and self.traits['pride'] + randint(0,2) >= 5:
			self.goals.append("defeat " + str(enemy))


		# I want to avenge my brother by finding the person who knows who killed him and getting that information, then
		# by killing that person. Top level goals would include "avenge X", "conquer X", "protect X", "escape X", "obey X",
		# "protect self", "entertain self"
		#
		# Plot event is any action that a character takes.
		#
		# If a character is in a place where an action happens, that action is added to their knowledge.
		# If two characters are in the same location, random chance to share knowledge. If a character asks about something,
		# better chance of getting shared knowledge.
		#
		# Base actions include 'go', 'find' (at location), 'work', 'sleep', ('ask', 'talk', 'recruit', 'confront') -> dialogue with intent, 'fight', 'kill'
		# what does a base level action look like?
		action = {'verb' : "go", 'object' : "Port Monsmouth"}

	# TODO: job generator

	# TODO: evaluating fear of a situation

	def full_name(self):
		return self.first_name + " " + self.last_name

	def print2(self):
		print(self.full_name() + " - " + self.gender + " " + self.allegiance)
		print(self.traits)
		print(self.goals)
		print(self.relationships)

# Generate some allegiances
allegiances = ["none", "Harteria", "Mystacasm", "Poynter"]

# Generate a bunch of characters
num_characters = 20
characters = []
for i in range(num_characters):
	characters.append(
		Character.generate(i, allegiances)
	)
	#characters[i].print2()

# Create relationships
num_relationships = 0
while num_relationships < 4 * num_characters: # roughly 4 relationships per person
	# Pick two characters at random and create a relationship, if they don't have one
	(char_a, char_b) = sample(characters, 2)
	if char_a.create_relationship(char_b) == 1: 
		num_relationships += 2

# Create goals
characters[0].generate_goals()
characters[0].print2()
#for i in range(num_characters):
#	characters[i].gererate_goals()


def generate_environment():
	pass

def generate_goals():
	pass

def generate_plot():
	pass