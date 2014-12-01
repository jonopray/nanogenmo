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
	trait_categories = ["intelligence", "strength", "charisma", "kindness", "competence", "resolve", "honesty", "age", "outgoingness", "status", "mood", "attractiveness"]
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

    def create_relationship(self, other):
    	possible_relationships = []
    	
    	family_difference = 0
    	for ['status', 'intelligence', 'charisma', 'strength'] as trait:
    		family_difference += abs(self.traits[trait] - other.traits[trait])
    	values_difference = 0
    	for ['intelligence', 'kindness', 'honesty', 'status', 'attractiveness'] as trait:
    		values_difference += abs(self.traits[trait] - other.traits[trait])

    	if (self.allegiance == other.allegiance and self.traits['status'] >= 4 and \
    		other.traits['status'] >= 4) or family_difference <= 3:
    		possible_relationships.append('familial')
    	
    	if (self.allegiance == other.allegiance and self.traits['status'] >= 2 and \
    		other.traits['status'] >= 2):
    		possible_relationships.append('political')

    	if (self.gender != other.gender and self.mood > 2 and other.mood > 2 and \
    		values_difference <= 4):
    		possible_relationships.append('romantic')

    	if ()

    		"""
    		if self.traits['age'] == other.traits['age']:
    			self.relationships[other.id] = "sibling"
    			other.relationships[self.id] = "sibling"
    		else if self.traits['age'] < other.traits['age']:
    			self.relationships[other.id] = "parent";
    			other.relationships[self.id] = "child";
    		else:
    			self.relationships[other.id] = "child";
    			other.relationships[self.id] = "parent";
    		self.relationships[other.id] = "";
    			other.relationships[self.id] = "";
    		"""

    	# if same allegiance and both high status, familial
    	# if similar strength and intelligence, familial
    	# if familial and differing ages, parent or uncle if parent exists
    	# if conflicting values of kindness, enemies
    	# if not family, and not enemies

	def print2(self):
		print(self.first_name + " " + self.last_name + " - " + self.gender + " " + self.allegiance)
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
	characters[i].print2()

# Create relationships
num_relationships = 0
while num_relationships < 4 * num_characters: # roughly 4 relationships per person
	# Pick two characters at random and create a relationship, if they don't have one
	(char_a, char_b2) = sample(characters, 2)
	char_a.create_relationship(char_b)
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