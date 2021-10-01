class Conversation:
	def __init__(self, id = None, recipes = None):
		# self.ingredient = None
		# self.cuisine_preference = None
		# self.dietary_preference = None
		self.ID = id
		self.recipes = recipes
		self.pick = None

	# def def_ingredient(self, ingredient_list):
	# 	self.ingredient = ingredient_list

	# def def_cuisine_preference(self, cuisine_preference):
	# 	self.cuisine_preference = cuisine_preference

	# def def_dietary_preference(self, dietary_preference):
	# 	self.dietary_preference = dietary_preference

	def set_recipes(self, recipes):
		self.recipes = recipes
	
	def set_pick(self, p):
		self.pick = int(p)
	
	def get_pick(self):
		return self.pick
