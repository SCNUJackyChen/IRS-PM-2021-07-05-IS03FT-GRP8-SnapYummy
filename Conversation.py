class Conversation:
	def __init__(self):
		self.ingredient = None
		self.cuisine_preference = None
		self.dietary_preference = None

	def def_ingredient(self, ingredient_list):
		self.ingredient = ingredient_list

	def def_cuisine_preference(self, cuisine_preference):
		self.cuisine_preference = cuisine_preference

	def def_dietary_preference(self, dietary_preference):
		self.dietary_preference = dietary_preference
