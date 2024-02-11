from classes.fallacy import *

def fallacy_grading(detected_fallacy, grade):
	"""
	Attempts to validate dictionary as a fallacy using fallacy class instances (see classes/fallacy.py)
	, returns the dictionary and updated grade
	"""
	try:
		for fallacy_instance in fallacy_list:
			if fallacy_instance.get_name().lower() in detected_fallacy["fallacy type"].lower():
				grade = fallacy_instance.apply_deduction(grade)
				detected_fallacy["Penalty"] = fallacy_instance.total_deduction()
				return grade, detected_fallacy

		print(f"This fallacy was not an instance: {detected_fallacy['fallacy type']}")
		print(f"{detected_fallacy}\n")			
	except KeyError:
		print(f"Problematic Dictionary: \n{detected_fallacy}")
	return grade, None

def inaccuracy_grading(detected_inaccuracy, grade):
	"""
	Attempts to validate dictionary as an inaccuracy, returns the dictionary and updated
	grade
	"""
	skip_list = ["not a factual inaccuracy", "no factual inaccuracy", \
	"cannot be fact-checked", "This statement is true and accurate"]
	try: 
		if not any(skip in detected_inaccuracy["factual correction"].lower() for skip in skip_list):
			#if detected_inaccuracy["factual correction"] != "":
				## Inaccuracy penalty
				grade -= 1
				return grade, detected_inaccuracy
	except KeyError:
		print(f"Problematic Dictionary: \n{detected_inaccuracy}")	
	return grade, None

def grading(detected_dict, grade):
	"""
	Calls the correct grading function, depending on the dictionary keys
	"""
	for key, value in detected_dict.items():
		if key == "fallacy type":
			return fallacy_grading(detected_dict, grade)
		elif key == "factual correction":
			return inaccuracy_grading(detected_dict, grade)
		
	print(f"This dictionary was not an instance: {detected_dict}\n")
	return grade, None



