import torch
from pathlib import Path

# Models
available_models = [ 'samantha' ]
formatter_name = 'ljspeech'
model_conf_arg_1 = 'model_args'
model_conf_arg_2 = 'num_chars'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Included Model Info
samantha_name = "samantha"
samantha_dl_url = "https://xmn.def.mybluehost.me/samantha/models/tts_vits_samantha_ai_3.0.7z"
samantha_folder = "samantha_ai_3.0"
samantha_vits = "vits-ljspeech-2023-06-01_170300"

# Paths
conda_possible_locations = [ Path.home() / 'anaconda3', Path.home() / 'miniconda3' ]
conda_win_path = 'C:/ProgramData/Anaconda3'
conda_linux_path = '/opt/anaconda3'
conda_help_file_win = 'Scripts/activate.bat'
conda_help_file_linux = 'bin/activate'
venv_possible_locations = [
    Path.home() / '.virtualenvs', Path.home() / 'venvs', Path.home() / 'envs', 
    Path.home() / 'virtualenvs', Path.home() / '.vens', Path.home() / '.envs' 
    ]
venv_help_file_win = 'Scripts/activate.bat'
venv_help_file_linux = 'bin/activate'

# Default Audio Configs
aud_sample_rate = 22050
aud_win_length = 1024
aud_hop_length = 256
aud_num_mels = 80
aud_mel_fmin = 0
aud_mel_fmax = None

# Default Vits Configs
run_name = "vits_ljspeech"
batch_size = 16
eval_batch_size = 16
batch_group_size = 16
num_loader_workers = 4
num_eval_loader_workers = 4
run_eval = True
test_delay_epochs = -1
epochs = 8500
save_step = 1000
save_checkpoints = True
save_n_checkpoints = 4
save_best_after = 1000
text_cleaner = "multilingual_cleaners"
use_phonemes = True
phoneme_language = "en-us"
compute_input_seq_cache = True
print_step = 25
print_eval = True
mixed_precision = True
cudnn_benchmark = False

# Default Aux Inputs
aux_inputs =  { "speaker_id": None, "d_vector": None, "style_wav": None }

# Default Dictionary Output Configs
dict_with_output = True
dict_no_output = False
dict_griffin_lim = True
dict_trim_silence = False

# Git Configs
git_tts = 'TTS'
git_tts_url = "https://github.com/coqui-ai/TTS.git"

# Web Server Configs
web_tts_route = '/tts'
web_tts_auth_get = 'Authorization'
web_tts_route_method = 'POST'
web_tts_route_response_type = 'audio/wav'
web_tts_route_response_code = 200
web_tts_route_response_error_code = 400

# Extensions
aac_ext = '.aac'
bat_ext = '.bat'
csv_ext = '.csv'
exe_ext = '.exe'
json_ext = '.json'
mp3_ext = '.mp3'
pth_ext = '.pth'
py_ext = '.py'
sh_ext = '.sh'
txt_ext = '.txt'
wav_ext = '.wav'

# Folder Names
completed_folder = 'completed'
models_folder = 'models'
output_wavs_folder = 'output_wavs'
phoneme_cache_folder = 'phoneme_cache'
scripts_folder = 'Scripts'
sources_folder = 'sources'
train_out_folder = 'traineroutput'

# File Names
activate_file = 'activate'
anaconda_file = 'anaconda'
bash_file = 'bash'
brew_file = 'brew'
choco_file = 'choco'
clone_file = 'clone'
conda_file = 'conda'
config_file = 'config'
env_file = '.env'
env_ex_file = '.env.example'
git_file = 'git'
install_file = 'install'
main_file = 'main'
meta_file = 'metadata'
pip_file = 'pip'
progress_file = 'progress'
python_file = 'python'
requirements_file = 'requirements'
start_file = 'start'
sudo_apt_file = 'sudo apt-get'
venv_file = 'venv'

# Key Names
venv_env_key = 'VENV_ENV'
venv_helper_key = 'VENV_HELPER'
venv_path_key = 'VENV_PATH'
