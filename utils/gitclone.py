import os, shutil, subprocess

def get_git_url(repo_name):
    from .vars import git_tts, git_tts_url

    if repo_name == git_tts:
        return git_tts_url
    else:
        raise ValueError(f"No automation set up for {repo_name}. Please try manually.")

def check_git(repo_name):
    from .vars import git_file, clone_file, pip_file, install_file

    folder_path = os.path.join(os.getcwd(), repo_name)
    if os.path.exists(folder_path):
        try:
            subprocess.check_call([pip_file, 'show', repo_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            confirm = input(f"The package {repo_name} exists but is not installed. Do you want to delete the folder and reinstall? (Y/N) ")
            if confirm.lower() == 'y':
                shutil.rmtree(folder_path)
            else:
                print(f"The folder {folder_path} needs to be removed to continue.")
                return False
    else:
        try:
            git_url = get_git_url(repo_name)
            subprocess.check_call([git_file, clone_file, git_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.check_call([pip_file, install_file, '-e', folder_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to clone or install {repo_name}. Please try manually.")
            return False
