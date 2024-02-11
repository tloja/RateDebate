class Fallacy:
	"""
	Class to represent various logical fallacies to validate a GPT fallacy response. Weights are a
	arbitrarily initialized based on preliminary testing.
	"""
	def __init__(self, name, weight):
		self.name = name
		self.weight = weight 
		self.counter = 0 

	def apply_deduction(self, grade):
		""" Deduct the weight from the grade and increment the counter. """
		self.counter += 1
		return grade - self.weight

	def total_deduction(self):
		""" Return total deduction for this fallacy. """
		return self.counter * self.weight

	def get_name(self):
		""" Return the name of the fallacy. """
		return self.name

""" Fallacy Initializations """
fallacy_list = []
###
fallacy_list.append(Fallacy("Begging the Question", 0.9))
fallacy_list.append(Fallacy("Circular Reasoning", 0.9))
###
fallacy_list.append(Fallacy("Ad Hominem", 1.1))
fallacy_list.append(Fallacy("Name Calling", 1.1))
###
fallacy_list.append(Fallacy("Anecdotal", 1.0))
fallacy_list.append(Fallacy("Appeal to Personal Experience", 1.0))
###
fallacy_list.append(Fallacy("Appeal to Tradition", 0.6))
fallacy_list.append(Fallacy("Appeal to Common Practice", 0.6))
###
fallacy_list.append(Fallacy("False Cause", 1.0))
fallacy_list.append(Fallacy("Questionable Cause", 0.5))
###
fallacy_list.append(Fallacy("Appeal to Ignorance", 0.9))
fallacy_list.append(Fallacy("Appeal from Ignorance", 0.9))
###
fallacy_list.append(Fallacy("Fallacy of Black and White", 1.0))
fallacy_list.append(Fallacy("False Dilemma", 1.0))
###
fallacy_list.append(Fallacy("Hasty Generalization", 0.9))
fallacy_list.append(Fallacy("Overgeneralization", 1.0))
###
fallacy_list.append(Fallacy("Bandwagon Fallacy", 1.0))
fallacy_list.append(Fallacy("Loaded Language", 1.0))
fallacy_list.append(Fallacy("Tu Quoque", 0.9))
fallacy_list.append(Fallacy("Red Herring", 0.7))
fallacy_list.append(Fallacy("Cherry Picking", 1.0))
fallacy_list.append(Fallacy("Slippery Slope", 0.9))
fallacy_list.append(Fallacy("False Dichotomy", 0.9))
fallacy_list.append(Fallacy("Appeal to Emotion", 1.0))
fallacy_list.append(Fallacy("Strawman", 0.3))
fallacy_list.append(Fallacy("Fatalistic", 2.2))
fallacy_list.append(Fallacy("False Equivalence", 0.9))
fallacy_list.append(Fallacy("Appeal to Authority", 0.8))
fallacy_list.append(Fallacy("Appeal to Popularity", 1.0))
fallacy_list.append(Fallacy("Exaggeration", 1.0))
fallacy_list.append(Fallacy("Appeal to Consequences", 0.9))
fallacy_list.append(Fallacy("False Analogy", 1.0))
fallacy_list.append(Fallacy("Conspiracy Theory", 1.0))
fallacy_list.append(Fallacy("Appeal to Personal Belief", 0.9))
fallacy_list.append(Fallacy("Loaded Question", 1.0))
fallacy_list.append(Fallacy("Repetition", 1.0))
fallacy_list.append(Fallacy("Appeal to Probability", 1.0))
fallacy_list.append(Fallacy("Appeal to Hypocrisy", 1.0))
fallacy_list.append(Fallacy("Subjective Comparison", 1.0))
fallacy_list.append(Fallacy("Non Sequitur", 1.0))
fallacy_list.append(Fallacy("Contradiction", 1.0))
fallacy_list.append(Fallacy("Appeal to Ridicule", 1.0))
fallacy_list.append(Fallacy("Ad Ignorantiam", 1.0))
fallacy_list.append(Fallacy("Argument from Incredulity", 1.0))
fallacy_list.append(Fallacy("Ambiguity", 1.0))
fallacy_list.append(Fallacy("Jumping to Conclusions", 1.0))
fallacy_list.append(Fallacy("Ad Hoc", 1.0))
fallacy_list.append(Fallacy("Appeal to Extremes", 1.0))
fallacy_list.append(Fallacy("Appeal to Complexity", 0.4))
fallacy_list.append(Fallacy("Appeal to Simplicity", 0.7))
fallacy_list.append(Fallacy("Hypothesis Contrary to Fact", 0.5))
fallacy_list.append(Fallacy("Unfalsfiability", 1.0))
fallacy_list.append(Fallacy("Post hoc ergo propter hoc", 1.0))