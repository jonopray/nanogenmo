from random import choice

class Character:
	# TODO: abstract away these choices. In generate(), pass in a config file,
	# which we can open and read from.
	first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard"]
	last_names = ["Johnson", "Davis", "Miller", "Jackson", "Robinson", "Clark", "Allen", "Carter"]
	ages = ["child", "young", "middle-aged", "old"]
	genders = ["male", "female"]
	traits_1 = ["loyal", "opportunist", "selfish", "deceiptful", "stubborn", "pragmatic", "resolute"] # loyalties
	traits_2 = ["weak", "thin", "flabby", "fat", "strong"] # physical
	traits_3 = ["silent", "mean", "kind", "boring", "charismatic", "talkative"] # persona
	# appearance (hair, eyes, nose)

	def generate():
		character = Character()
		character.name = choice(Character.first_names) + " " + choice(Character.last_names)
		character.gender = choice(Character.genders)
		character.attributes = []
		character.attributes.append(choice(Character.ages))
		character.attributes.append(choice(Character.traits_1))
		character.attributes.append(choice(Character.traits_2))
		character.attributes.append(choice(Character.traits_3))
		return character

	def print(self):
		print(self.name + " is a " + ", ".join(self.attributes) + " " + self.gender)

# test Character creation
c = Character.generate()
c.print()

def generate_environment():
	pass

def generate_goals():
	pass

def generate_plot():
	pass