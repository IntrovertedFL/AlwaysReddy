### COMPLETIONS API SETTINGS ###
COMPLETIONS_API = "together" # 'openai' or 'together' 
OPENAI_MODEL = "gpt-3.5-turbo"
TOGETHER_MODEL = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT"

### HOTKEYS ###
CANCEL_HOTKEY = 'ctrl + alt + x'
CLEAR_HISTORY_HOTKEY = 'ctrl + alt + f12'
RECORD_HOTKEY = 'ctrl + shift + space'

### VOICE SETTINGS ###
PIPER_VOICE_JSON="en_en_US_amy_medium_en_US-amy-medium.onnx.json" #These are located in the piper_voices folder
PIPER_VOICE_ONNX="en_US-amy-medium.onnx"
TTS_ENGINE="piper" # 'piper' or 'openai' piper is local and fast but openai is better sounding
OPENAI_VOICE = "nova"


### MISC ###
HOTKEY_DELAY = 0.5
AUDIO_FILE_DIR = "audio_files"
MAX_TOKENS = 6000 #Max tokens allowed in memory at once
START_SEQ = "-CLIPSTART-" #the model is instructed to place any text for the clipboard between the start and end seq
END_SEQ = "-CLIPEND-" #the model is instructed to place any text for the clipboard between the start and end seq


### AUDIO SETTINGS ###
BASE_VOLUME = 1 
FS = 11025   
START_SOUND_VOLUME = 0.000003
END_SOUND_VOLUME = 0.000003
CANCEL_SOUND_VOLUME = 0.000009
MIN_RECORDING_DURATION = 0.3
MAX_RECORDING_DURATION= 300 #in seconds 5 min by default

