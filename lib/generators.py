from random import choice
from random import randint
from random import sample

class Character:
	# TODO: abstract away these choices. In generate(), pass in a config file,
	# which we can open and read from.
	male_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard"]
	female_names = ["Mary", "Jennifer", "Jessica", "Sarah", "Karen", "Lisa", "Sandra", "Ashley", "Michelle", "Emily"]
	last_names = ["Johnson", "Davis", "Miller", "Jackson", "Robinson", "Clark", "Allen", "Carter"]
	genders = ["male", "female"]
	trait_categories = ["intelligence", "strength", "charisma", "kindness", "competence", "resolve", "honesty", "age", "outgoingness", "status", "mood", "attractiveness", "pride"]
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
		if character.gender == "male" :
			character.first_name = choice(Character.male_names)
		else:
			character.first_name = choice(Character.female_names)
		character.last_name = choice(Character.last_names)
		character.generate_traits()
		character.knowledge = {} # a dictionary of plot_id : [location bool, subject bool, verb bool, object bool]
		# character.job/position? has a location
		character.relationships = {} # a dictionary of character name : 1-5 describing how close, 3 neutral
		character.goals = []
		character.allegiance = choice(allegiances)

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

	def generate_goals(self):
		self.goals = ["protect self"]
		self.generate_goal()

	goals = ["entertain self", "protect PERSON", ""]
	# NEED TO GENERATE CHARACTERS AND FORM RELATIONSHIPS FIRST, BEFORE DECIDING GOALS
	def generate_goal(self):
		# Motivations: is there a person we care about? Are we high status?
		# for now, let's do random



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
		print(other.full_name() + " is " + self.full_name() + "'s " + self.relationships[other.id])
		print(self.full_name() + " is " + other.full_name() + "'s " + other.relationships[self.id])
		#print(other.full_name() + " is a " + other.relationships[self.id] + " of " + self.full_name())
		self.print2()
		other.print2()
		return 1

	def full_name(self):
		return self.first_name + " " + self.last_name

	def print2(self):
		print(self.full_name() + " - " + self.gender + " " + self.allegiance)
		print(self.traits)

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
while num_relationships < 10: #4 * num_characters: # roughly 4 relationships per person
	# Pick two characters at random and create a relationship, if they don't have one
	(char_a, char_b) = sample(characters, 2)
	if char_a.create_relationship(char_b) == 1: 
		num_relationships += 2

"""
# test Character creation
c = Character.generate()
c.print2()
"""

def generate_environment():
	pass

def generate_goals():
	pass

def generate_plot():
	pass