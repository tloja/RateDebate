import whisper
import datetime
import subprocess
import torch
import pyannote.audio
from pyannote.audio import Audio
from pyannote.core import Segment
import wave
import contextlib
from sklearn.cluster import AgglomerativeClustering
import numpy as np
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from sox import file_info
from tqdm import tqdm

audio = Audio()
language = 'English'
model_size = 'small'

def time(secs):
	return datetime.timedelta(seconds=round(secs))

def segment_embedding(embedding_model, segment, duration, file):
	start = segment["start"]
	end = min(duration, segment["end"])
	clip = Segment(start, end)
	waveform, sample_rate = audio.crop(file, clip)
	return embedding_model(waveform[None])

def diarize_file(file, num_speakers):
	"""
	Converts a .wav file (in mono format) into a transcript, where each segment of a speech is denoted
	by the speaker tag (SPEAKER N), and the timestamp. Needs to be provided the number of speakers present
	in the audio file. 

	Youtube Video Citation: 
	Title: OpenAI Whisper Speaker Diarization - Transcription with Speaker Names
	Creator: 1littlecoder
	URL: https://youtu.be/MVW746z8y_I
	"""
	channels = file_info.channels(file)
	if channels != 1:
		print("File not in mono format, please convert the file to mono to proceed.")
		exit()

	embedding_model = PretrainedSpeakerEmbedding(
		"speechbrain/spkrec-ecapa-voxceleb",
		device='cpu')

	# language = 'English'
	# model_size = 'small'
	# model_name = model_size

	with contextlib.closing(wave.open(file,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		duration = frames / float(rate)
	print(f"\n\nProcessing audio file transcription (this will take around {round(duration / 60, 1)} minutes)")
	
	model = whisper.load_model(model_size)
	result = model.transcribe(file)
	segments = result["segments"]
	embeddings = np.zeros(shape=(len(segments), 192))
	for i, segment in tqdm(enumerate(segments), total=len(segments), desc='Processing segments'):
		embeddings[i] = segment_embedding(embedding_model, segment, duration, file)

	embeddings = np.nan_to_num(embeddings)
	clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
	labels = clustering.labels_
	for i in range(len(segments)):
		segments[i]["speaker"] = 'SPEAKER ' + str(labels[i]+1)

	f = open("transcript.txt", "w")

	for (i, segment) in enumerate(segments):
		if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
			f.write("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + '\n' )
		f.write(segment["text"][1:] + ' ')
	f.close()

	model_name = model_size
	if language == 'English' and model_size != 'large':
		model_name += '.en'

	print("\nFile transcripted into transcript.txt")
