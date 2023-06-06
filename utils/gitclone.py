import os
import shutil
import subprocess

def get_url(repo_name):
    if repo_name == "TTS":
        return "https://github.com/coqui-ai/TTS.git"
    else:
        raise ValueError(f"No automation set up for {repo_name}. Please try manually.")

def check_git(repo_name):
    folder_path = os.path.join(os.getcwd(), repo_name)
    if os.path.exists(folder_path):
        try:
            subprocess.check_call(['pip', 'show', repo_name])
            return True
        except subprocess.CalledProcessError:
            confirm = input(f"The package {repo_name} exists but is not installed. Do you want to delete the folder and reinstall? (Y/N) ")
            if confirm.lower() == 'y':
                shutil.rmtree(folder_path)
            else:
                print(f"The folder {folder_path} needs to be removed to continue.")
                return False
    try:
        git_url = get_url(repo_name)
        subprocess.check_call(['git', 'clone', git_url])
        subprocess.check_call(['pip', 'install', '-e', folder_path])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to clone or install {repo_name}. Please try manually.")
        return False
