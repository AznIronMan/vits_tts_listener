import os
import time
import torch

from flask import Flask, request

from utils.checks import api_check, batch_file_exists, cuda_check, env_check, get_os, get_wav_path, models_check, sub_check
from utils.configs import get_num_chars, get_outputs_dict_config, vits_config
from utils.gitclone import check_git
from utils.procs import get_audio_processor, get_model, get_timer
from utils.starter import batch_check, check_pip
from utils.voices import get_voice, meta_file_name, output_folder

env_check()

skips = [ os.getenv('SKIP_PIP'), os.getenv('SKIP_BATCH') ]

if not (batch_file_exists) and not (skips[1]):
    if not (batch_check(get_os())):
        SystemError("Batch file not found.  System Error.  Exiting...")

if not (skips[0]):
    check_pip()

check_git('TTS')

sub_check()

models_check(meta_file_name, output_folder)

cuda_check()

app = Flask(__name__)

# TODO : Add SSL to Flask app

@app.route('/tts', methods=['POST'])
def synthesize():

    api_check(request.headers.get('Authorization'))

    # TODO : Make the api check more secure

    data = request.get_json()
    voice = data.get('voice')
    text = data.get('text')
    emotion = data.get('emotion')
    paths = get_voice(voice)
    meta_file = meta_file_name
    model_path = paths[0]
    output_path = paths[1]
    config_path = paths[2]
    phoneme_cache_path = paths[3]

    num_chars = get_num_chars(config_path)
    if (num_chars is None):
        num_chars = 0

    config = vits_config(meta_file, phoneme_cache_path, output_path)

    if emotion:
        # TODO : integrate emotion into text and pass to model
        pass

    # TODO : convert text to phonemes and pass to model

    model = get_model(config, model_path)
    ap = get_audio_processor(config)

    syn_start_time = time.time()
    
    with torch.no_grad():
        outputs_dict = get_outputs_dict_config(model, text, config)
    
    syn_end_time = time.time()
    
    syn_time = get_timer(syn_start_time, syn_end_time, "syn")

    aud_start_time = time.time()

    final_wav_path = get_wav_path()

    ap.save_wav(outputs_dict['wav'], final_wav_path)
    with open(final_wav_path, "rb") as f:
        audio_data = f.read()
    
    aud_end_time = time.time()
    
    aud_time = get_timer(aud_start_time, aud_end_time, "aud")

    get_timer(syn_time, aud_time, "total")

    return audio_data, 200, {'Content-Type': 'audio/wav'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('LISTENING_PORT'))