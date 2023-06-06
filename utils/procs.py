import torch

from TTS.utils.audio import AudioProcessor
from TTS.tts.models.vits import Vits

def get_audio_processor(config):
    return AudioProcessor.init_from_config(config)

def get_cuda():
    return torch.cuda.is_available()

def get_model(config, model_path):
    cuda = get_cuda();
    model = Vits.init_from_config(config)
    cp = torch.load(model_path, map_location=torch.device('cuda'))
    model.load_state_dict(cp['model'])
    model.eval()
    model.decoder_mode = False
    device = torch.device('cuda' if cuda else 'cpu')
    model = model.to(device)
    return model

def get_timer(start, end, type): 
    time = end - start
    if type == "syn":
        print(f"synthesis took {time} seconds")
    elif type == "aud":
        print(f"audio processing took {time} seconds")
    elif type == "total":
        time = start + end
        print(f"total time was {time} seconds")
    else:
        print(f"{type} took {time} seconds")
    return time