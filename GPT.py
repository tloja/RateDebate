import openai
openai.api_key = "YOUR_KEY_HERE"

def get_logical_fallacies(text, model):
	"""
	Find all logical fallacies and return them in a dictionary,
	with the type of logical fallacy, the culpable text, and the timestamps
	"""
	query = f"""
	You are a logical fallacy detector.
	Read the entire text to understand the full context, and whether or not a fallacy is being committed.
	The number and speaker that begin each line indicate the time stamps of the text spoken by X speaker.
	The speaker tag comes BEFORE the text, so when you choose text, go back and select the previous closest speaker tag.
	You will return each fallacy you detect, as well as an explanation of how the speaker engaged in a fallacy.
	This is how you will format it:
	''[{{"speaker": "SPEAKER X", "text": "text", "fallacy type": "Strawman", "timestamp": "0:00:00 - 0:00:59" "explanation": "This is your explanation"}},{{dictionary B}},{{dictionary C}}]''
	If there are no fallacies detected, return the empty array [{{}}].
	Remember to enclose the dictionaries into an array [].
	This is the text: 

	"""

	gpt_response = get_completion(query+text, model, 1.0).replace("'",r"\'")
	return gpt_response

def get_factual_inaccuracies(text, model):
	"""
	Find any factual inaccuracies in the text and return them in a dictionary,
	with the culpable text, the correction, and the timestmaps
	"""
	query = f"""
	You are a factual inaccuracy detector. 
	Read the entire text to understand the full context, and return any text that is not factually accurate.
	The number and speaker that begin each line indicate the time stamps of the text spoken by X speaker.
	You will return each factual inaccuracy you detect, speaker, timestamp, as well as the factual correction,.
	Do not detect statements from speakers if they are represented as opinions and not facts/truths.
	The speaker tag comes BEFORE the text, so when you choose text, go back and select the previous closest speaker tag.
	Do not include statements that are factually accurate.
	If you change your mind about a detection, remove it from your response.
	This is how you will format it:
	''[{{"speaker": "SPEAKER X", "text": "text", "timestamp": "0:00:00 - 0:00:59", "factual correction": "Insert your factual correction"}},{{dictionary B}},{{dictionary C}}]''
	If there are no factual inaccuracies, return the empty array [{{}}].
	Remember to enclose the dictionaries into an array [].
	This is the text: 

	"""

	gpt_response = get_completion(query+text, model, 1.0).replace("'",r"\'")
	return gpt_response


def get_completion(prompt, model, temperature): 
	"""
	Send the prompt to the API and receive the completion
	"""
	messages = [{"role": "user", "content": prompt}]

	try:
		response = openai.ChatCompletion.create(
		model=model,
		messages=messages,
		temperature=temperature,
		)
	except openai.error.InvalidRequestError:
		response = "[{}]"
		return response

	return response.choices[0].message["content"]