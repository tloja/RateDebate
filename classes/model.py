import tiktoken
class Model:
	"""
	Class to represent various GPT models in order to calculate their token limits, and 
	potential completion cost
	"""
	def __init__(self, name, tokens, cost_input, cost_output):
		self.name = name
		self.tokens = tokens
		self.cost_input = cost_input
		self.cost_output = cost_output

	def get_name(self):
		return self.name

	def get_tokens(self):
		return self.tokens

	def get_token_limit(self):
	## Initial token limit safeguard
		return int(self.tokens * .5)

	def get_cost_input(self):
	## Per 1K tokens
		return self.cost_input

	def get_cost_output(self):
	## Per 1k tokens
		return self.cost_output

	def get_encoding(self):
		return tiktoken.encoding_for_model(self.name)


gpt_4 = Model("gpt-4", 8192, 0.03, 0.06)
gpt_4_0613 = Model("gpt-4-0613", 8192, 0.03, 0.06)
gpt_35_turbo_16k = Model("gpt-3.5-turbo-16k", 16385, 0.003, 0.004)
gpt_4_1106_preview = Model("gpt-4-1106-preview", 128000, 0.01, 0.03)
gpt_35_turbo_0125 = Model("gpt-3.5-turbo-0125", 16385, 0.0005, 0.0015)