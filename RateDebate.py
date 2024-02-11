from GPT import *
from grading import grading
from classes.model import *
from tqdm import tqdm
import argparse
import os.path
from yt2wav import *
import re

def num_speakers(text):
	"""
	Returns an array of the speaker strings
	"""
	speaker_list = []
	speakers = re.findall('SPEAKER [0-9]', text)
	return sorted(list(set(speakers)), key=lambda x: int(x.split()[1]))

def filter_speakers(speakers_list):
	"""
	Creates a dictionary where each speaker key has an array of dictionaries as its value
	"""
	filtered_dict = {}
	for dictionary in speakers_list:
		speaker = dictionary["speaker"]
		if speaker not in filtered_dict:
			filtered_dict[speaker] = []
		filtered_dict[speaker].append(dictionary)
	return filtered_dict

def validate_dict(data, arg_list):
	"""
	ensure the dictionary returned from the GPT API is correct
	"""
	if not isinstance(data, dict):
		return False
	for argument in arg_list:
		if not (argument in data and isinstance(data[argument], str)):
			return False

	return True

def validate_response(final_list, model_max_tokens, gpt_list, arg_list):
	"""
	validate GPT response; if not valid, lower max_tokens and restart calls
	"""
	try:
		if isinstance(eval(gpt_list), list):
			if(eval(gpt_list) == [{}]):
				return final_list, model_max_tokens
			for dictionary in eval(gpt_list):
				valid_flag = validate_dict(dictionary, arg_list)
				if not valid_flag:
					model_max_tokens -= 1000
					break
				final_list.append(dictionary)
				# if not valid_flag:
				# 	continue
	except SyntaxError:
		pass
	except NameError:
		pass
	return final_list, model_max_tokens


def file_to_GPT(text, model):
	"""
	Process the transcript with GPT responses and collect the fallacies and inaccuracies. Save each speaker 
	error to the specific speaker and report a final grade.
	"""
	speakers = num_speakers(text)
	if speakers == []:
		print(f"\nNo speakers detected. Please check the filepath or re-attempt the transcription.")
		exit()

	model_max_tokens = model.get_token_limit()
	tokens = len(model.get_encoding().encode(text))  
	text_length = len(text)
	quotient = text_length / model.get_tokens()	
	fallacies = []
	factual_inaccuracies = []

	## send the transcript in segments to get the GPT response
	if(tokens > model_max_tokens):
		file_cursor = 0

		pbar = tqdm(total=text_length, desc="Processing GPT response", position = 0, leave=True)
		while(file_cursor < text_length):
			calculation = int(model_max_tokens * quotient + file_cursor)

			if (calculation < text_length):
				loop_cursor = text[0:calculation].rfind('\n')
			else:
				loop_cursor = text_length
			if "SPEAKER" in text[loop_cursor-18:loop_cursor]:
				loop_cursor = text[0:loop_cursor].rfind('\n')

			truncated_text = text[file_cursor:loop_cursor]
			gpt_fallacy_list = get_logical_fallacies(truncated_text, model.get_name())
			gpt_fact_list = get_factual_inaccuracies(truncated_text, model.get_name())

			fallacies, model_max_tokens = validate_response(fallacies, model_max_tokens, \
				gpt_fallacy_list, ["speaker", "text", "timestamp", "explanation"])
			factual_inaccuracies, model_max_tokens = validate_response(factual_inaccuracies, model_max_tokens, \
				gpt_fact_list, ["speaker", "text", "timestamp", "factual correction"])


			file_cursor = loop_cursor
			pbar.update(loop_cursor)
		pbar.close()

	# the transcript is small enough to process in one response
	else:
		gpt_fallacy_list = get_logical_fallacies(text, model.get_name())
		gpt_fact_list = get_factual_inaccuracies(text, model.get_name())
		try:
			if isinstance(eval(gpt_list), list):
				for dictionary in eval(gpt_list):
					fallacies.append(dictionary)
		except SyntaxError:
			print("Nothing added to list.")

	filtered_result = filter_speakers(fallacies + factual_inaccuracies)

	grade_list = {speaker: 100 for speaker in speakers}
	error_list = {speaker: [] for speaker in speakers}

	for speaker, dict_list in filtered_result.items():
		speaker_grade = 100
		speaker_errors = []
		for dictionary in dict_list:
			speaker_grade, speaker_error = grading(dictionary, speaker_grade)
			speaker_errors.append(speaker_error) if speaker_error else None
		grade_list[speaker] = speaker_grade
		error_list[speaker] = speaker_errors

	return grade_list, error_list

def wav_file(file):
	ext = os.path.splitext(file)[1][1:]
	if ext != "wav":
		raise argparse.ArgumentTypeError(f"File is not in correct format (.wav).")
	return file

def main():
	parser = argparse.ArgumentParser(description='Can accept a youtube link, .wav file, or a proprietary transcript.')
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("--text_file", help="Path to the already processed text file", type=str)
	group.add_argument("--yt_link", help="Youtube link to convert [NEEDS --num_speakers DEFINED]", type=str)
	group.add_argument("--audio_file", help="Path to the .wav input file [NEEDS --num_speakers DEFINED]", type=wav_file)
	parser.add_argument("--num_speakers", help="Number of speakers in file", type=int)
	args = parser.parse_args()

	## Current Model (see available models in classes/model.py)
	model = gpt_35_turbo_0125

	if args.text_file:
		file = args.text_file

	if args.yt_link:
		print(f"Processing Video Conversion...\n")
		args.audio_file = convert_video(args.yt_link)

	if args.audio_file and not args.num_speakers:
		print(f"--num_speakers is required for audio file transcription.")
		return

	if args.audio_file and args.num_speakers:
		from diarize import diarize_file, model_size, language
		diarize_file(args.audio_file, args.num_speakers)
		file = "transcript.txt"

	print(f"\nProcessing text file: {file}")
	with open(file) as f:
		text = f.read()
	
	tokens = len(model.get_encoding().encode(text))
	price = (tokens / 1000) * model.get_cost_input()
	price += (tokens / 2000) * model.get_cost_output()
	price *= 2
	decision = input(f"GPT API call will cost ~${round(price, 3)}. Do you wish to continue? (Y/N): ")
	if decision == "Y" or decision == "y":
		grades, errors = file_to_GPT(text, model)
	else:
		return

	print(f"\n\n\nSPEAKER GRADING: \n")
	for key in grades.keys():
		if key in errors:
			for error in errors[key]:
				for k, v in error.items():
					print(f"{k}: {v}")
				print('=' * 100)
			print('*' * 41)
			print(f"*\t{key} Final Grade:\t{grades[key]}\t*")
			print('*' * 41)
			print()

if __name__ == "__main__":
    main()