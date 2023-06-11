import torch

from TTS.utils.audio import AudioProcessor
from TTS.tts.models.vits import Vits

def get_audio_processor(config):
    return AudioProcessor.init_from_config(config)

def get_cuda():
    return torch.cuda.is_available()

def get_model(config, model_path):
    from .vars import torch_device

    model = Vits.init_from_config(config)
    cp = torch.load(model_path, map_location=torch.device(torch_device))
    model.load_state_dict(cp['model'])
    model.eval()
    model.decoder_mode = False
    device = torch.device(torch_device)
    model = model.to(device)
    return model

def get_timer(start, end, type, others = []): 
    time = end - start
    if type == "syn" or type == "aud" or type == "phon":
        return time
    elif type == "total":
        time = 0
        for t in others:
            time += t
        time += (start + end)
        return time
    else:
        print(f"{type} took {time} seconds")
    return time