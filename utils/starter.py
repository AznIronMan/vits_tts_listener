import os, shutil

from dotenv import dotenv_values, load_dotenv, set_key
from pathlib import Path
from subprocess import CalledProcessError, run, PIPE

def batch_check(operating_system):
    from .vars import bat_ext, start_file, sh_ext

    win_batch_file = (start_file + bat_ext)
    win_batch_path = os.path.join(os.getcwd(), win_batch_file)
    linux_batch_file = (start_file + sh_ext)
    linux_batch_path = os.path.join(os.getcwd(), linux_batch_file)

    batch_path = win_batch_path if operating_system == "Windows" else linux_batch_path

    if not os.path.exists(batch_path):
        batch_builder(operating_system)
        return True
    else:
        return False
      
def batch_builder(operating_system):
    from .checks import env_check, get_os
    from .envinfo import env_venv_name
    from .vars import env_file, venv_env_key, venv_helper_key, venv_path_key, venv_file, anaconda_file, conda_file, venv_file, anaconda_file, conda_file, env_file, venv_file, venv_env_key, venv_helper_key, venv_path_key

    if operating_system is None:
        vpython_answer = None
    else:
        vpython_answer = find_pyt_env(operating_system, True)

    if isinstance(vpython_answer, tuple) and len(vpython_answer) == 2:
        vpython_folder, vpython_helper = vpython_answer
    else:
        vpython_folder, vpython_helper = None, None

    if vpython_folder is not None and vpython_helper is not None:
        set_key(env_file, venv_env_key, venv_file)
        set_key(env_file, venv_path_key, str(vpython_folder))
        set_key(env_file, venv_helper_key, str(vpython_helper))
        operating_system = get_os()

    vpython_name = None
    vpython_folder = None
    vpython_answer = None

    if env_check() is False:
        try:
            install_pre_env()
        except Exception as e:
            print(e)
            print(f'Could not create {env_file} file. Please create one manually and restart application.')
            raise SystemExit(1)
        batch_builder(operating_system)

    load_dotenv()

    vpython_name = env_venv_name
    venv_env = vpython_name.lower() if isinstance(vpython_name, str) else vpython_name

    if venv_env is None:
        vpython_answer = find_anaconda2(operating_system)
        if venv_env == anaconda_file or venv_env == conda_file:
            find_pyt_env(operating_system, True)
        elif venv_env == venv_file:
            find_pyt_env(operating_system, True)
        else:
            print(f"Cannot find virtual env '{venv_env}' from your {env_file} file.")
            cannot_answer = input(f"Would you to choose between {anaconda_file} or {venv_file} (Y/N)? ").lower().startswith('y')
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
    from .vars import conda_help_file_win, conda_help_file_linux, venv_help_file_win, venv_help_file_linux, anaconda_file, venv_file

    if not skip:
        using_venv = input(f'Are you using a virtual environment like {anaconda_file} or {venv_file} (Y/N)? ').lower().startswith('y')
        if not using_venv:
            return False

    using_anaconda = input(f"Are you using {anaconda_file} (Y/N)? ").lower().startswith('y')

    if using_anaconda:
        try:
            return find_anaconda2(operating_system)
        except FileNotFoundError:
            anaconda_path = input(f'Could not find {anaconda_file} installation. Please enter the {anaconda_file} install path: ')
            helper_file = Path(conda_help_file_win if operating_system == "Windows" else conda_help_file_linux)
            if (Path(anaconda_path) / helper_file).is_file():
                return anaconda_path, Path(anaconda_path) / helper_file

    if not using_anaconda:
        using_venv = input(f'Are you using {venv_file} (Y/N)? ').lower().startswith('y')

        if using_venv:
            try:
                return find_venv2(operating_system)
            except FileNotFoundError:
                venv_path = input(f'Could not find {venv_file}. Please enter the {venv_file} path: ')
                helper_file = Path(venv_help_file_win if operating_system == "Windows" else venv_help_file_linux)
                if (Path(venv_path) / helper_file).is_file():
                    return venv_path, Path(venv_path) / helper_file
                else:
                    print(f'Invalid {venv_file} path.')
                    return False
                
    try:
        return find_venv2(operating_system)
    except FileNotFoundError:
        venv_path = input(f'Could not find venv. Please enter the {venv_file} path: ')
        helper_file = Path(venv_help_file_win if operating_system == "Windows" else venv_help_file_linux)
        if (Path(venv_path) / helper_file).is_file():
            return venv_path, Path(venv_path) / helper_file
        else:
            print(f'Invalid {venv_file} path.')
            return False

def find_anaconda2(operating_system):
    from .vars import conda_win_path, conda_linux_path, bat_ext, activate_file, anaconda_file, scripts_folder

    vpython_folder = None

    if(operating_system == 'Windows'):
        vpython_folder = conda_win_path
    elif(operating_system == 'Linux' or operating_system == 'MacOS'):
        vpython_folder = conda_linux_path
    else:
        raise SystemError("Operating system not supported.")
    
    if not os.path.exists(vpython_folder):
        print(f"Could not find find {anaconda_file} installation at {vpython_folder}.")
        manual_paths = manual_location(anaconda_file, operating_system)
        if not manual_paths:
            return False
        else:
            vpython_folder, vpython_helper = manual_paths
    
    if not vpython_folder is None:
        vpython_helper = os.path.join(vpython_folder, scripts_folder, (activate_file + bat_ext) if operating_system == 'Windows' else activate_file)
        return vpython_folder, vpython_helper

    vpython_helper = os.path.join(vpython_folder, scripts_folder, (activate_file + bat_ext) if operating_system == 'Windows' else activate_file)

    return vpython_folder, vpython_helper

def find_venv2(operating_system):
    from .vars import bat_ext, activate_file, venv_file, scripts_folder  

    vpython_folder = None

    if operating_system == 'Windows':
        vpython_folder = os.path.join(os.environ['USERPROFILE'], venv_file)
    elif operating_system == 'Linux' or operating_system == 'MacOS':
        vpython_folder = os.path.join(os.environ['HOME'], venv_file)
    else:
        raise SystemError("Operating system not supported.")
    
    if not os.path.exists(vpython_folder):
        print(f"Could not find {venv_file} installation at {vpython_folder}.")
        manual_paths = manual_location(venv_file, operating_system)
        if not manual_paths:
            return False
        else:
            vpython_folder, vpython_helper = manual_paths
    
    if not vpython_folder is None:
        vpython_helper = os.path.join(vpython_folder, scripts_folder, (activate_file + bat_ext) if operating_system == 'Windows' else activate_file)
        return vpython_folder, vpython_helper
    else:
        return False

def manual_location(virtual_env_name, operating_system):
    from .vars import bat_ext, activate_file, scripts_folder  

    print(f"Could not find {virtual_env_name} installation. Please enter the {virtual_env_name} install path:")
    vpython_folder = input('> ')

    if not os.path.exists(vpython_folder):
        print(f"Invalid {virtual_env_name} path.")
        return False

    vpython_helper = os.path.join(vpython_folder, scripts_folder, (activate_file + bat_ext) if operating_system == 'Windows' else activate_file)

    return vpython_folder, vpython_helper

def install_pre_env():
    from .vars import env_file, env_ex_file

    env_file_name = Path(env_file)
    env_example_file = Path(env_ex_file)

    if not env_file_name.exists():
        shutil.copy(env_example_file, env_file_name)

    load_dotenv()

    env_values = dotenv_values(env_file)
    env_fields = list(env_values.keys())

    if not env_fields:
        raise ValueError(f"No fields found in {env_file} file. Please create them manually.")


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

    print(f"Success! {env_file} file has been created and all fields have been set.")
    return True

def check_pip(skip = False):
    from .vars import txt_ext, install_file, pip_file, requirements_file

    if not skip:
        try:
            with open(requirements_file + txt_ext) as f:
                requirements = f.read().splitlines()
            for requirement in requirements:
                run([pip_file, install_file, requirement], check=True)
            print("All requirements installed successfully.")
            return True
        except CalledProcessError:
            print(f"Failed to install requirements. Please run '{pip_file} {install_file} -r {requirements_file}{txt_ext}' manually.")
            return False       
    else:
        return True

def build_the_batch(operating_system, vpython_answer, vpython_environment):
    from .vars import bat_ext, exe_ext, py_ext, sh_ext, activate_file, anaconda_file, bash_file, conda_file, main_file, python_file, start_file

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

    if vpython_env == anaconda_file or vpython_env == conda_file:
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
        vpython_envs = run(f"{vpython_helper} && {conda_file} env list", shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if vpython_name in vpython_envs.stdout:
            print(f"{vpython_name} already exists in {vpython_env}.")
            use_env = input(f"Would you like to use {vpython_name}? (y/n): ")
            if use_env.lower() == 'y':
                print(f"Using {vpython_name} in {vpython_env}.")
                run(f"{vpython_helper} && {conda_file} {activate_file} {vpython_name}", shell=True, check=True)
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

    with open((start_file + bat_ext) if operating_system == 'Windows' else (start_file + sh_ext), 'w') as f:
        if operating_system == 'Windows':
            f.write(f'@echo off\ncall {vpython_helper} {vpython_folder}\ncall {conda_file} {activate_file} {vpython_name}\ncd /d {working_directory}\n{python_file}{exe_ext} {main_file}{py_ext}\n')
        else:  # Linux or MacOS
            f.write(f'#!/bin/bash\nsource {vpython_helper} {vpython_folder}\n{conda_file} {activate_file} {vpython_name}\ncd {working_directory}\n{python_file}{exe_ext} {main_file}{py_ext}\n')

    start_instructions = f"'.\\{start_file}{bat_ext}' from powershell (as admin), '{start_file}{bat_ext}' from command line (as admin), or right click '{start_file}{bat_ext}' in Windows Explorer and select 'Run As Administrator'" if operating_system == 'Windows' else f"'./{start_file}{sh_ext}' or '{bash_file} ./{start_file}{sh_ext}'"
    print("Assuming all settings are correct, you can now start this script by:\n\n"
          + start_instructions +
          f"\n\nIf this ever needs to be rebuilt, run {main_file}{py_ext} and select 'Run Initial Config Setup' to rebuild this file.\n\nEnjoy!👌")
