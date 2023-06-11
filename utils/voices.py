import os, glob

def get_voice(name):
    from .vars import samantha_name, samantha_folder, samantha_vits, phoneme_cache_folder, train_out_folder, models_folder, config_file, json_ext

    config_file_name = config_file + json_ext
    voices_path = os.path.join(os.getcwd(), models_folder)

    model = None
    vits_folder = None
    if name == samantha_name:
        model = samantha_folder
        vits_folder = samantha_vits

    if model is None:
        raise ValueError(f"Invalid voice name: {name}")

    if vits_folder is None:
        raise ValueError(f"Invalid vits folder name: {vits_folder}")

    model_path = os.path.join(voices_path, model)
    output_path = os.path.join(model_path, train_out_folder)
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
    from .vars import pth_ext, train_out_folder

    pth_files = glob.glob(os.path.join(output_folder, "*" + pth_ext))

    if not pth_files:
        raise ValueError(f"No *{pth_ext} files found in the {train_out_folder} folder.")
    
    newest_pth = max(pth_files, key=os.path.getctime)
    pth_file_path = os.path.join(output_folder, newest_pth.split("\\")[-1])

    if not os.path.exists(pth_file_path):
        raise ValueError(f'The {pth_ext} file path does not exist.')
    
    return pth_file_path

def get_model_info(name):
    from .vars import samantha_name, samantha_folder, samantha_dl_url

    if (name.lower() == samantha_name ):
        return [ str(samantha_folder), str(samantha_dl_url) ]
    else:
        raise ValueError(f"Invalid voice name: {name}")
