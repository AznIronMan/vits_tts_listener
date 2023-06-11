import os

from dotenv import load_dotenv

load_dotenv()

env_api_key: str = str(os.getenv('API_KEY', 'default_api_key'))
env_listen_port: int = int(os.getenv('LISTENING_PORT', '8080'))
env_skip_pip: bool = os.getenv('SKIP_PIP', 'False').lower() == 'true'
env_skip_batch: bool = os.getenv('SKIP_BATCH', 'False').lower() == 'true'
env_default_model: str = str(os.getenv('DEFAULT_MODEL', 'samantha'))
env_listen_host: str = str(os.getenv('LISTENING_HOST', 'localhost'))
env_listen_name: str = str(os.getenv('LISTENING_NAME', 'vits_tts_listener'))
env_listen_ipv6: bool = os.getenv('LISTENING_IPV6', 'False').lower() == 'true'
env_listen_threads: int = int(os.getenv('LISTENING_THREADS', '4'))
env_listen_ssl: bool = os.getenv('LISTENING_SSL', 'False').lower() == 'true'
env_venv_name: str = str(os.getenv('VENV_NAME', 'venv'))

env_custom_models = os.getenv('CUSTOM_MODELS', None)