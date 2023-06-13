from TTS.TTS.config import load_config
from TTS.TTS.config.shared_configs import BaseDatasetConfig
from TTS.TTS.tts.configs.vits_config import VitsConfig
from TTS.TTS.tts.models.vits import VitsAudioConfig
from TTS.TTS.tts.utils.synthesis import synthesis

def dataset_config(meta_file_name, output_path):
    from .vars import formatter_name

    return BaseDatasetConfig(formatter_name, meta_file_train=meta_file_name, path=output_path)

def audio_config():
    from .vars import aud_sample_rate, aud_win_length, aud_hop_length, aud_num_mels, aud_mel_fmin, aud_mel_fmax

    return VitsAudioConfig(
        sample_rate=aud_sample_rate, 
        win_length=aud_win_length, 
        hop_length=aud_hop_length, 
        num_mels=aud_num_mels, 
        mel_fmin=aud_mel_fmin, 
        mel_fmax=aud_mel_fmax
    )

def vits_config(meta_file_name, phoneme_path, output_path):
    from .vars import run_name, batch_size, eval_batch_size, batch_group_size, num_loader_workers, num_eval_loader_workers, run_eval, test_delay_epochs, epochs, save_step, save_checkpoints, save_n_checkpoints, save_best_after, text_cleaner, use_phonemes, phoneme_language, compute_input_seq_cache, print_step, print_eval, mixed_precision, cudnn_benchmark

    return VitsConfig(
        audio=audio_config(),
        run_name=run_name,
        batch_size=batch_size,
        eval_batch_size=eval_batch_size,
        batch_group_size=batch_group_size,
        num_loader_workers=num_loader_workers,
        num_eval_loader_workers=num_eval_loader_workers,
        run_eval=run_eval,
        test_delay_epochs=test_delay_epochs,
        epochs=epochs,
        save_step=save_step,
        save_checkpoints=save_checkpoints,
        save_n_checkpoints=save_n_checkpoints,
        save_best_after=save_best_after,
        text_cleaner=text_cleaner,
        use_phonemes=use_phonemes,
        phoneme_language=phoneme_language,
        phoneme_cache_path=phoneme_path,
        compute_input_seq_cache=compute_input_seq_cache,
        print_step=print_step,
        print_eval=print_eval,
        mixed_precision=mixed_precision,
        output_path=output_path,
        datasets=[dataset_config(meta_file_name, output_path)],
        cudnn_benchmark=cudnn_benchmark,
    )

def get_num_chars(config_path):
    from .vars import model_conf_arg_1, model_conf_arg_2

    model_config = load_config(config_path)
    return model_config[model_conf_arg_1][model_conf_arg_2]

def get_outputs_dict_config(model, text, config):
    from .procs import get_cuda
    from .vars import dict_griffin_lim, dict_trim_silence, aux_inputs

    return synthesis(
        model, 
        text, 
        config,
        use_cuda = get_cuda(),
        speaker_id = aux_inputs['speaker_id'], 
        d_vector = aux_inputs['d_vector'], 
        style_wav = aux_inputs['style_wav'],
        use_griffin_lim = dict_griffin_lim,
        do_trim_silence = dict_trim_silence,
    )