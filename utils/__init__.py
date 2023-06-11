from .checks import env_check, api_check, cuda_check, find_anaconda, find_venv, folder_check, get_wav_path, get_os, sub_check, batch_file_exists, models_check, check_chocolatey, check_brew, check_7zip, get_7zip_path, port_check
from .configs import dataset_config, vits_config, get_num_chars, get_outputs_dict_config
from .envinfo import env_api_key, env_listen_port, env_skip_pip, env_skip_batch, env_default_model, env_listen_host, env_listen_name, env_listen_ipv6, env_listen_threads, env_listen_ssl, env_venv_name, env_custom_models
from .filer import get_datetime_file_formatted, get_files_from_location, remove_non_alphanumeric_to_file
from .gitclone import get_git_url, check_git
from .procs import get_audio_processor, get_cuda, get_model, get_timer 
from .starter import batch_check, batch_builder, find_pyt_env, find_anaconda2, find_venv2, manual_location, install_pre_env, check_pip, build_the_batch
from .vars import available_models, formatter_name, model_conf_arg_1, model_conf_arg_2, torch_device, samantha_name, samantha_dl_url, samantha_folder, samantha_vits, conda_possible_locations, conda_win_path, conda_linux_path, conda_help_file_win, conda_help_file_linux, venv_possible_locations, venv_help_file_win, venv_help_file_linux, aud_sample_rate, aud_win_length, aud_hop_length, aud_num_mels, aud_mel_fmin, aud_mel_fmax, run_name, batch_size, eval_batch_size, batch_group_size, num_eval_loader_workers, run_eval, test_delay_epochs, epochs, save_step, save_n_checkpoints, save_best_after, text_cleaner, use_phonemes, phoneme_language, compute_input_seq_cache, print_step, print_eval, mixed_precision, cudnn_benchmark, aux_inputs, dict_with_output, dict_no_output, dict_griffin_lim, dict_trim_silence, git_tts, git_tts_url, web_tts_route, web_tts_auth_get, web_tts_route_method, web_tts_route_response_type, web_tts_route_response_code, web_tts_route_response_error_code, aac_ext, bat_ext, csv_ext, exe_ext, json_ext, mp3_ext, pth_ext, py_ext, sh_ext, txt_ext, wav_ext, completed_folder, models_folder, output_wavs_folder, phoneme_cache_folder, scripts_folder, sources_folder, train_out_folder, activate_file, anaconda_file, bash_file, brew_file, choco_file, clone_file, conda_file, env_file, env_ex_file, git_file, install_file, main_file, meta_file, pip_file, progress_file, python_file, requirements_file, start_file, sudo_apt_file, venv_file, venv_env_key, venv_helper_key, venv_path_key
from .voices import get_voice, find_pth, get_model_info

from .formatter import blank_line as blank_line
from .formatter import bold as B_text
from .formatter import bold_underline as BU_text
from .formatter import bold_underline_italic as BUI_text
from .formatter import clear_console as cls
from .formatter import color_text as C_text
from .formatter import italic as I_text
from .formatter import strikethrough as S_text
from .formatter import underline as U_text
from .formatter import underline_italic as UI_text
from .formatter import yes_or_no as YN_to_TF

from .listen import listen as start_serve