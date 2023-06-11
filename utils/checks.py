import datetime as dt
import os, platform, shutil, socket, torch

from dotenv import load_dotenv as LoadDotEnv
from flask import jsonify as FlaskJsonify
from typing import Tuple

def env_check():
    from .envinfo import env_api_key, env_listen_port

    try:
        LoadDotEnv()
        if not env_api_key:
            raise ValueError('API_KEY is missing in .env file')
        if not env_listen_port:
            raise ValueError('PORT is missing in .env file')
        return True
    except Exception as e:
        print(f"Error loading .env file - {e}")
        raise SystemExit('Missing .env file.  Exiting...')

def api_check(api_key):
     from .envinfo import env_api_key

     if not api_key:
        return FlaskJsonify({'error': 'API key is missing'}), 401
     else:
        try:
            LoadDotEnv()
            if(env_api_key != api_key):
                return FlaskJsonify({'error': 'Invalid API key'}), 401
            else:
                return True
        except:
            return FlaskJsonify({'error': 'Invalid API key'}), 401

def cuda_check(show = True):
    cuda = torch.cuda.is_available()
    if show and not cuda:
        print("***WARNING***  CUDA is not available.  Falling back to CPU.")
    return cuda

def find_anaconda(operating_system: str) -> Tuple[str, str] or bool:
    from .vars import conda_possible_locations, conda_help_file_win, conda_help_file_linux

    possible_locations = conda_possible_locations
    helper_file = conda_help_file_win if operating_system == "Windows" else conda_help_file_linux

    for location in possible_locations:
        if (location / helper_file).is_file():
            str_location = str(location)
            str_helper_file = str(location / helper_file)
            return str_location, str_helper_file
    raise FileNotFoundError("Anaconda not found.")

def find_venv(operating_system: str) -> Tuple[str, str] or bool:
    from .vars import venv_possible_locations, venv_help_file_win, venv_help_file_linux

    possible_locations = venv_possible_locations
    helper_file = venv_help_file_win if operating_system == "Windows" else venv_help_file_linux

    for location in possible_locations:
        for venv in location.glob("*"):
            if (venv / helper_file).is_file():
                str_venv = str(venv)
                str_helper_file = str(venv / helper_file)
                return str_venv, str_helper_file
    raise FileNotFoundError("venv not found.")

def folder_check(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path

def get_wav_path():
    from .vars import wav_ext, output_wavs_folder

    file_ext = wav_ext
    folder_name = output_wavs_folder
    now = dt.datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S") + file_ext
    folder_path = os.path.join(os.getcwd(), folder_name)
    folder_check(folder_path)
    final_path = os.path.join(folder_path, filename)
    return final_path

def get_os():
    operating_system = platform.system()
    if(operating_system == 'Windows'):
        return 'Windows'
    elif(operating_system == 'Linux'):
        return 'Linux'
    elif(operating_system == 'Darwin'):
        return 'MacOS'
    else:
        return None

def sub_check():
    from .vars import models_folder, output_wavs_folder

    try:
        models = os.path.join(os.getcwd(), models_folder)
        output_wavs = os.path.join(os.getcwd(), output_wavs_folder)

        folders = [models, output_wavs]

        for folder in folders:
            folder_check(folder)
        
        return True
    except Exception as e:
        print(f"Error creating folders - {e}")
        raise SystemExit('Error creating folders.  Exiting...')
    
def batch_file_exists():
    from .starter import batch_check
    from .vars import bat_ext, sh_ext, start_file

    batch_file = os.path.join(os.getcwd(), (start_file + bat_ext)) or os.path.join(os.getcwd(), start_file + sh_ext)
    if os.path.exists(batch_file):
        try:
            batch_check(get_os())
        except Exception as e:
            print(f"Error with batch file - {e}")
            raise SystemExit('Error creating batch file.  Exiting...')
        return True
    else:
        return False
    
def models_check(meta_file_name, output_folder):
    from .envinfo import env_default_model, env_custom_models
    from .vars import models_folder, available_models
    from .voices import get_model_info

    operating_system = get_os()

    LoadDotEnv()

    models = []
    default_model = env_default_model
    custom_models = env_custom_models

    if default_model:
        models.append(default_model)

    if custom_models:
        models.extend(custom_models.split(","))

    used_models = models

    retrieve_models = []

    check_7zip(operating_system)

    path_7z = get_7zip_path(operating_system)

    for model in available_models:
        if model in used_models:
            retrieve_models.append(model)

        for model in retrieve_models:
            modelroot = os.getcwd() + '/' + models_folder
            modelinfo = get_model_info(model)
            modelfolder = modelinfo[0]
            url = modelinfo[1]
            file_name = url.split('/')[-1].split('_')[2]
            remaining_name = url.split('/')[-1].split('_')[3:]
            if remaining_name:
                file_name += '_' + '_'.join(remaining_name)
            foldername = modelroot + '/' + modelfolder
            folder_check(foldername)
            if not os.path.exists(foldername):
                raise SystemError(f'Error with {foldername} folder.  Exiting...')
            elif os.path.exists(modelroot + '/' + file_name):
                if not os.path.exists(foldername + '/' + meta_file_name) and os.path.exists(foldername + '/' + output_folder):
                    try:
                        print(f'Extracting {file_name} to {foldername}...')
                        if operating_system == 'Windows':
                            os.system(f'powershell -Command "& \'{path_7z}\' x {modelroot}/{file_name} -o{modelroot}"')
                        else:
                            os.system(f"7z x {modelroot}/{file_name} -o{modelroot}")
                        print(f'Extraction of {file_name} to {foldername} complete...')
                    except Exception as e:
                        raise SystemExit(f'Error with {model} model and {file_name}. Exiting...')
            else:
                if not os.path.exists(foldername + '/' + meta_file_name) and os.path.exists(foldername + '/' + output_folder):
                    try:
                        if operating_system == 'Windows':
                            print(f'Downloading {file_name} to {modelroot} via powershell...')
                            os.system(f'powershell -Command "(New-Object System.Net.WebClient).DownloadFile(\'{url}\', \'{modelroot}/{file_name}\')"')
                            print(f'Download of {file_name} complete.')
                        elif operating_system == 'MacOS':
                            print(f'Downloading {file_name} to {modelroot} via curl...')
                            os.system(f'curl -o {modelroot}/{file_name} {url}')
                            print(f'Download of {file_name} complete.')
                        else:
                            print(f'Downloading {file_name} to {modelroot} via wget...')
                            os.system(f'wget {url} -P {modelroot}')
                            print(f'Download of {file_name} complete.')
                        print(f'Extracting {file_name} to {foldername}...')
                        if operating_system == 'Windows':
                            os.system(f'powershell -Command "& \'{path_7z}\' x {modelroot}/{file_name} -o{modelroot}"')
                        else:
                            os.system(f"7z x {modelroot}/{file_name} -o{modelroot}")
                        print(f'Extraction of {file_name} to {foldername} complete...')
                    except Exception as e:
                        print(f'Error with {model} model and downloading {file_name}. Exiting...')
                        raise SystemExit(f'Error: {e}')
            if os.path.exists(foldername + '/' + meta_file_name) and os.path.exists(foldername + '/' + output_folder):
                continue
            else:
                raise SystemExit(f'Error with {model} model. Exiting...')
    
    select_all_models_7z = os.path.join(os.getcwd(), "models", "*.7z")

    if os.path.exists(select_all_models_7z):
        if operating_system == 'Windows':
            os.system(f'del {select_all_models_7z}')
        elif operating_system == 'MacOS' or 'Linux':
            os.system(f'rm {select_all_models_7z}')

def check_chocolatey():
    from .vars import choco_file

    if not shutil.which(choco_file):
        try:
            print("Chocolatey is not installed.  Installing Chocolatey...")
            os.system("powershell -Command \"Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))\"")
            print("Chocolatey installed successfully.")
            return True
        except Exception as e:
            print("***ERROR***  Chocolatey installation failed.  Please install Chocolatey manually and try again.")
            print(f"Error: {e}")
            raise SystemExit('Chocolatey installation failed.  Exiting...')

def check_brew():
    from .vars import brew_file

    if not shutil.which(brew_file):
        try:
            print("Homebrew is not installed.  Installing Homebrew...")
            os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            print("Homebrew installed successfully.")
            return True
        except Exception as e:
            print("***ERROR***  Homebrew installation failed.  Please install Homebrew manually and try again.")
            print(f"Error: {e}")
            raise SystemExit('Homebrew installation failed.  Exiting...')

def check_7zip(operating_system):
    from .vars import choco_file, brew_file, sudo_apt_file

    the_path = get_7zip_path(operating_system)
    if(operating_system == "Windows"):
        if not os.path.exists(the_path):
            if check_chocolatey():
                try:
                    print("7zip is not installed.  Installing 7zip...")
                    os.system(f"{choco_file} install 7zip -y")
                    print("7zip installed successfully.")
                    return True
                except Exception as e:
                    print("***ERROR***  7zip installation failed.  Please install 7zip manually and try again.")
                    print(f"Error: {e}")
                    raise SystemExit('7zip installation failed.  Exiting...')
        elif(operating_system == "MacOS"):
            if not os.path.exists(the_path):
                if check_brew():
                    try:
                        print("7zip is not installed.  Installing 7zip...")
                        os.system(f"{brew_file} install p7zip -y")
                        print("7zip installed successfully.")
                        return True
                    except Exception as e:
                        print("***ERROR***  7zip installation failed.  Please install 7zip manually and try again.")
                        print(f"Error: {e}")
                        raise SystemExit('7zip installation failed.  Exiting...')
        elif(operating_system == "Linux"):
            if not os.path.exists(the_path):
                try:
                    print("7zip is not installed.  Installing 7zip...")
                    os.system(f"{sudo_apt_file} update")
                    os.system(f"{sudo_apt_file} install -y p7zip-full")
                    print("7zip installed successfully.")
                    return True
                except Exception as e:
                    print("***ERROR***  7zip installation failed.  Please install 7zip manually and try again.")
                    print(f"Error: {e}")
                    raise SystemExit('7zip installation failed.  Exiting...')
                
def get_7zip_path(operating_system):
    standard_paths = []
    if operating_system == "Windows":
        standard_paths = [r"C:\Program Files\7-Zip\7z.exe", r"C:\Program Files (x86)\7-Zip\7z.exe"]
    elif operating_system == "MacOS":
        standard_paths = [r"/usr/local/bin/7z"]
    elif operating_system == "Linux":
        standard_paths = [r"/usr/bin/7z"]
    else:
        raise SystemExit('Operating system not supported. Exiting...')

    for path in standard_paths:
        if os.path.exists(path):
            return path

    manual_path = input("Please enter the path to your 7zip executable: ")
    if os.path.exists(manual_path):
        return manual_path
    else:
        raise SystemExit('7zip installation failed. Exiting...')
    
def port_check(port_number):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', int(port_number))) == 0