import os, time, torch

from flask import Flask, request
from waitress import serve

def listen():
    from .checks import get_os, env_check, sub_check, models_check, cuda_check, api_check, batch_file_exists, get_wav_path
    from .configs import get_num_chars, vits_config, get_outputs_dict_config
    from .envinfo import env_skip_pip, env_skip_batch, env_listen_port, env_listen_name, env_listen_host, env_listen_ipv6, env_listen_threads
    from .gitclone import check_git
    from .procs import get_model, get_audio_processor, get_timer
    from .starter import batch_check, check_pip
    from .vars import meta_file, csv_ext, train_out_folder, web_tts_route, web_tts_route_method, web_tts_auth_get, git_tts, web_tts_route_response_code, web_tts_route_response_type
    from .voices import get_voice

    operating_system = get_os()
    meta_file_name = meta_file + csv_ext

    env_check()

    if not (batch_file_exists) and not (env_skip_batch):
        if not (batch_check(operating_system)):
            SystemError("Batch file not found.  System Error.  Exiting...")

    if not (env_skip_pip):
        check_pip()

    check_git(git_tts)

    sub_check()

    models_check(meta_file_name, train_out_folder)

    cuda_check()

    app = Flask(__name__)

    @app.route(web_tts_route, methods=[web_tts_route_method]) # /tts
    def synthesize():

        api_check(request.headers.get(web_tts_auth_get))

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

        if not emotion:
            emotion = None

        # TODO : figure out how to integrate emotion into the model

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

        print("Time Breakdown:")
        print(f"Synthesis Time: {syn_time} | Audio Time: {aud_time}")
        print(f"Total Time: {syn_time + aud_time}")

        return audio_data, web_tts_route_response_code, {'Content-Type': web_tts_route_response_type}

    os.system('cls' if os.name == 'nt' else 'clear')
    tts_server_name = env_listen_name
    tts_host = env_listen_host
    tts_port = env_listen_port
    tts_ipv6 = env_listen_ipv6
    tts_threads = env_listen_threads
    print(f"Starting {tts_server_name} on {tts_host}:{tts_port}...")
    print(f"Listening...")
    serve(app, host=tts_host, port=tts_port, ipv6=tts_ipv6, ident=tts_server_name.lower(), threads=tts_threads)

    return app
