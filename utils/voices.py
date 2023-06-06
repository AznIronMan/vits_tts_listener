import os
import glob

voices_path = os.path.join(os.getcwd(), "models")

meta_file_name = "metadata.csv"
output_folder = "traineroutput"
config_file_name = "config.json"
phoneme_cache_folder = "phoneme_cache"

samantha_url = "https://xmn.def.mybluehost.me/samantha/models/tts_vits_samantha_ai_3.0.7z"
samantha_folder = "samantha_ai_3.0"

def get_voice(name):
    model = None
    vits_folder = None
    if name == "samantha":
        model = samantha_folder
        vits_folder = "vits-ljspeech-2023-06-01_170300"

    if model is None:
        raise ValueError(f"Invalid voice name: {name}")

    if vits_folder is None:
        raise ValueError(f"Invalid vits folder name: {vits_folder}")

    model_path = os.path.join(voices_path, model)
    output_path = os.path.join(model_path, output_folder)
    vits_path = os.path.join(output_path, vits_folder)
    config_path = os.path.join(vits_path, config_file_name)
    phoneme_cache_path = os.path.join(output_path, phoneme_cache_folder)
    full_model_path = os.path.join(vits_path, find_pth(vits_path))

    paths = [full_model_path, output_path, config_path, phoneme_cache_path]

    non_existing_paths = [path for path in paths if not os.path.exists(path)]
    print(non_existing_paths)
    if non_existing_paths:
        raise ValueError(f"The following paths do not exist: {non_existing_paths}")

    paths.append(find_pth(vits_path))

    return paths
    
def find_pth(output_folder):
    pth_files = glob.glob(os.path.join(output_folder, "*.pth"))

    if not pth_files:
        raise ValueError("No *.pth files found in the output folder.")
    
    newest_pth = max(pth_files, key=os.path.getctime)
    pth_file_path = os.path.join(output_folder, newest_pth.split("\\")[-1])

    if not os.path.exists(pth_file_path):
        raise ValueError("The pth file path does not exist.")
    
    return pth_file_path

def get_model_info(name):
    if (name.lower() == "samantha" ):
        return [ str(samantha_folder), str(samantha_url) ]
    else:
        raise ValueError(f"Invalid voice name: {name}")
