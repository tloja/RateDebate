# RateDebate: GPT-Powered Debate Analyzer
RateDebate uses GPT API to analyze audio conversations between speakers through logical fallacy and factual inaccuracy detection. Speakers are assigned a grade for their performance, depending on how many of these offenses they make. RateDebate can take a youtube video, or a .wav file as input. Weights for logical fallacies can be found in `classes/Fallacy.py` for customization in grading. If you have a GPU available then `device='cpu'` in `diarize.py` can be changed to your GPU for a more optimized transcription.

## Getting Set Up
- Install SoX and FFmpeg:
```
  sudo apt-get install sox ffmpeg
```
- Install python packages:
```
  pip3 install -r requirements.txt
```
- put your GPT API key in `GPT.py`

## Running
To run a youtube video, also supply the number of speakers: 
```
python3 RateDebate.py --yt_link=https://youtu.be/tYrdMjVXyNg --num_speakers=3
```
> Note: If a moderator is present, include them in the `num_speakers`

The script will proceed converting the video into .wav, and producing a `transcript.txt`, which will take around the same time as the video length. Before making the API call, a rough estimate of the API cost will be displayed, with the option of proceeding or exiting.

