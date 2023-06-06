import os
import shutil


from dotenv import dotenv_values, load_dotenv, set_key
from pathlib import Path
from subprocess import CalledProcessError, run, PIPE

batch_file = "start.bat"
batch_path = os.path.join(os.getcwd(), batch_file)

def batch_check(operating_system):
    if not os.path.exists(batch_path):
        batch_builder(operating_system)
        return True
    else:
        return False
    
def batch_builder(operating_system):
    from .checks import env_check, get_os, find_anaconda
    if operating_system is None:
        vpython_answer = None
    else:
        vpython_answer = find_pyt_env(operating_system, True)

    if isinstance(vpython_answer, tuple) and len(vpython_answer) == 2:
        vpython_folder, vpython_helper = vpython_answer
    else:
        vpython_folder, vpython_helper = None, None

    if vpython_folder is not None and vpython_helper is not None:
        set_key(".env", "VENV_ENV", "venv")
        set_key(".env", "VENV_PATH", str(vpython_folder))
        set_key(".env", "VENV_HELPER", str(vpython_helper))
        operating_system = get_os()

    vpython_name = None
    vpython_folder = None
    vpython_answer = None

    if env_check() is False:
        try:
            install_pre_env()
        except Exception as e:
            print(e)
            print("Could not create .env file. Please create one manually and restart application.")
            raise SystemExit(1)
        batch_builder(operating_system)

    load_dotenv()

    vpython_name = os.getenv("VENV_NAME")
    venv_env = vpython_name.lower() if isinstance(vpython_name, str) else vpython_name

    if venv_env is None:
        vpython_answer = find_anaconda(operating_system)
        if venv_env == "conda" or venv_env == "anaconda":
            find_pyt_env(operating_system, True)
        elif venv_env == "venv":
            find_pyt_env(operating_system, True)
        else:
            print(f"Cannot find virtual env '{venv_env}' from your .env file.")
            cannot_answer = input("Would you to choose between conda or venv (Y/N)? ").lower().startswith('y')
            if cannot_answer:
                vpython_answer = find_pyt_env(operating_system, True)
            else:
                vpython_answer = None

    if isinstance(vpython_answer, tuple) and len(vpython_answer) == 2:
        vpython_folder, vpython_helper = vpython_answer
    else:
        vpython_folder, vpython_helper = None, None

    if vpython_folder is not None and vpython_helper is not None:
        try:
            build_the_batch(operating_system, vpython_answer, venv_env)
        except Exception as e:
            print('Could not build batch file.  Exiting...')
            raise SystemError(e)

def find_pyt_env(operating_system, skip=False):
    from .checks import find_anaconda, find_venv
    if not skip:
        using_venv = input("Are you using a virtual environment like conda or venv (Y/N)? ").lower().startswith('y')
        if not using_venv:
            return False

    using_anaconda = input("Are you using anaconda (Y/N)? ").lower().startswith('y')

    if using_anaconda:
        try:
            return find_anaconda(operating_system)
        except FileNotFoundError:
            anaconda_path = input("Could not find Anaconda installation. Please enter the Anaconda install path: ")
            helper_file = Path("Scripts/activate.bat" if operating_system == "Windows" else "bin/activate")
            if (Path(anaconda_path) / helper_file).is_file():
                return anaconda_path, Path(anaconda_path) / helper_file

    if not using_anaconda:
        using_venv = input("Are you using venv (Y/N)? ").lower().startswith('y')

        if using_venv:
            try:
                return find_venv(operating_system)
            except FileNotFoundError:
                venv_path = input("Could not find venv. Please enter the venv path: ")
                helper_file = Path("Scripts/activate.bat" if operating_system == "Windows" else "bin/activate")
                if (Path(venv_path) / helper_file).is_file():
                    return venv_path, Path(venv_path) / helper_file
                else:
                    print("Invalid venv path.")
                    return False
                
    try:
        return find_venv(operating_system)
    except FileNotFoundError:
        venv_path = input("Could not find venv. Please enter the venv path: ")
        helper_file = Path("Scripts/activate.bat" if operating_system == "Windows" else "bin/activate")
        if (Path(venv_path) / helper_file).is_file():
            return venv_path, Path(venv_path) / helper_file
        else:
            print("Invalid venv path.")
            return False

def find_anaconda(operating_system):
    vpython_folder = None

    if(operating_system == 'Windows'):
        vpython_folder = "C:/ProgramData/Anaconda3"
    elif(operating_system == 'Linux' or operating_system == 'MacOS'):
        vpython_folder = "/opt/anaconda3"
    else:
        raise SystemError("Operating system not supported.")
    
    if not os.path.exists(vpython_folder):
        print(f"Could not find find Anaconda installation at {vpython_folder}.")
        manual_paths = manual_location('Anaconda', operating_system)
        if not manual_paths:
            return False
        else:
            vpython_folder, vpython_helper = manual_paths
    
    if not vpython_folder is None:
        vpython_helper = os.path.join(vpython_folder, "Scripts", "activate.bat" if operating_system == 'Windows' else 'activate')
        return vpython_folder, vpython_helper

    vpython_helper = os.path.join(vpython_folder, "Scripts", "activate.bat" if operating_system == 'Windows' else 'activate')

    return vpython_folder, vpython_helper

def find_venv(operating_system):
    vpython_folder = None

    if operating_system == 'Windows':
        vpython_folder = os.path.join(os.environ['USERPROFILE'], 'venv')
    elif operating_system == 'Linux' or operating_system == 'MacOS':
        vpython_folder = os.path.join(os.environ['HOME'], 'venv')
    else:
        raise SystemError("Operating system not supported.")
    
    if not os.path.exists(vpython_folder):
        print(f"Could not find venv installation at {vpython_folder}.")
        manual_paths = manual_location('venv', operating_system)
        if not manual_paths:
            return False
        else:
            vpython_folder, vpython_helper = manual_paths
    
    if not vpython_folder is None:
        vpython_helper = os.path.join(vpython_folder, "Scripts", "activate.bat" if operating_system == 'Windows' else 'activate')
        return vpython_folder, vpython_helper
    else:
        return False

def manual_location(virtual_env_name, operating_system):
    print(f"Could not find {virtual_env_name} installation. Please enter the {virtual_env_name} install path:")
    vpython_folder = input('> ')

    if not os.path.exists(vpython_folder):
        print(f"Invalid {virtual_env_name} path.")
        return False

    vpython_helper = os.path.join(vpython_folder, "Scripts", "activate.bat" if operating_system == 'Windows' else 'activate')

    return vpython_folder, vpython_helper

def install_pre_env():

    env_file = Path('.env')
    env_example_file = Path('.env.example')

    if not env_file.exists():
        shutil.copy(env_example_file, env_file)

    load_dotenv()

    env_values = dotenv_values(".env")
    env_fields = list(env_values.keys())

    if not env_fields:
        raise ValueError("No fields found in .env file. Please create them manually.")


    for field in env_fields:
        value = os.getenv(field)
        if not value:
            default_value = os.getenv(f"{field}_DEFAULT")
            user_input = input(f"Please enter a value for {field} (default: {default_value}): ")
            if user_input:
                set_key(env_file, field, user_input)
            else:
                set_key(env_file, field, default_value)

    load_dotenv()

    for field in env_fields:
        value = os.getenv(field)
        if not value:
            print(f"Failed to set value for {field}")
            return False

    print("Success! .env file has been created and all fields have been set.")
    return True

def check_pip(skip = False):
    if not skip:
        try:
            with open('requirements.txt') as f:
                requirements = f.read().splitlines()
            for requirement in requirements:
                run(['pip', 'install', requirement], check=True)
            print("All requirements installed successfully.")
            return True
        except CalledProcessError:
            print("Failed to install requirements. Please run 'pip install -r requirements.txt' manually.")
            return False       
    else:
        return True

def build_the_batch(operating_system, vpython_answer, vpython_environment):
    vpython_env = None
    if not vpython_environment is None:
        vpython_env = vpython_environment.lower()

    working_directory = os.getcwd()
    vpython_folder, vpython_helper = vpython_answer

    while True:
        vpython_name = input(f"Enter the name of your {vpython_env} virtual environment: ")
        if ' ' in vpython_name or not vpython_name.isalnum():
            print("Invalid virtual environment name. Please enter a name without spaces or invalid characters. (CTRL+C to Exit this loop.)")
        else:
            break

    if vpython_env == 'anaconda' or vpython_env == 'conda':
        vpython_envs = run(f"{vpython_helper} env list", shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if vpython_name in vpython_envs.stdout:
            print(f"{vpython_name} already exists in {vpython_env}.")
            use_env = input(f"Would you like to use {vpython_name}? (y/n): ")
            if use_env.lower() == 'y':
                print(f"Using {vpython_name} in {vpython_env}.")
                run(f"{vpython_helper} activate {vpython_name}", shell=True, check=True)
                return True
        else:
            create_env = input(f"{vpython_name} does not exist in {vpython_env}. Would you like to create it? (y/n): ")
            if create_env.lower() == 'y':
                run(f"{vpython_helper} create --name {vpython_name} python=3.8", shell=True, check=True)
                print(f"{vpython_name} has been created in {vpython_env}.")
            else:
                print(f"{vpython_name} was not created. Exiting...")
                return False
    elif vpython_env == 'venv':
        vpython_envs = run(f"{vpython_helper} && conda env list", shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if vpython_name in vpython_envs.stdout:
            print(f"{vpython_name} already exists in {vpython_env}.")
            use_env = input(f"Would you like to use {vpython_name}? (y/n): ")
            if use_env.lower() == 'y':
                print(f"Using {vpython_name} in {vpython_env}.")
                run(f"{vpython_helper} && conda activate {vpython_name}", shell=True, check=True)
                return True
        else:
            create_env = input(f"{vpython_name} does not exist in {vpython_env}. Would you like to create it? (y/n): ")
            if create_env.lower() == 'y':
                run(f"{vpython_helper} create {vpython_name}", shell=True, check=True)
                print(f"{vpython_name} has been created in {vpython_env}.")
            else:
                print(f"{vpython_name} was not created. Exiting...")
                return False
    else:
        raise SystemError(f"Your virtual environment {vpython_env} is not supported \n" +
                          "for this automated batch builder.\n" +
                          "You will need to create your virtual environment manually.\n" +
                          "Once this is complete, activate your virtual environment, \n" +
                          "then run 'python listen.py' to start the application.")

    with open('start.bat' if operating_system == 'Windows' else 'start.sh', 'w') as f:
        if operating_system == 'Windows':
            f.write(f'@echo off\ncall {vpython_helper} {vpython_folder}\ncall conda activate {vpython_name}\ncd /d {working_directory}\ncall python.exe listen.py\n')
        else:  # Linux or MacOS
            f.write(f'#!/bin/bash\nsource {vpython_helper} {vpython_folder}\nconda activate {vpython_name}\ncd {working_directory}\npython listen.py\n')

    start_instructions = f"'.\\start.bat' from powershell (as admin), 'start.bat' from command line (as admin), or right click 'start.bat' in Windows Explorer and select 'Run As Administrator'" if operating_system == 'Windows' else f"'./start.sh' or 'bash ./start.sh'"
    print("Assuming all settings are correct, you can now start this script by:\n\n"
          + start_instructions +
          "\n\nIf this ever needs to be rebuilt, run listen.py -new to rebuild this file.\n\nEnjoy!👌")
