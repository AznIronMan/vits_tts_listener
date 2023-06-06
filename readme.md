# TTS_Listener
by [ClarkTribeGames, LLC](https://www.clarktribegames.com)

## Description

git remote add origin https://github.com/AznIronMan/vits_tts_listener.git


## Installation

Clone the repository:
```bash
git clone https://github.com/AznIronMan/TTS_Listener
```

We recommend using a virtual environment using `venv` or `conda` for this project. Python 3.8-3.10 works best.

To create a virtual environment using `venv`:
```bash
python3 -m venv /path/to/new/virtual/environment
```

Activate it:

```bash
source /path/to/new/virtual/environment/bin/activate
```

To create a virtual environment using conda:

```bash
conda create --name myenv
```

Activate it:

```bash
conda activate myenv
```

**For GPU Users**

Before proceeding, check if your GPU is supported: [Nvidia CUDA GPUs](https://developer.nvidia.com/cuda-gpus).

Install PyTorch by following the instructions based on your OS and model video card from [PyTorch's official website](https://pytorch.org/get-started/locally/).

## Post Installation Steps

From within the TTS_Listener folder, clone the repository:
```bash
git clone https://github.com/coqui-ai/TTS
```

Install the necessary dependencies:
```bash
pip install -r requirements.txt
```
Copy .env.example to .env
Modify the .env file as appropriate: the **API_KEY** and the **LISTENING_PORT** are required.

**Note:** You may need to update your firewall settings or disable it entirely *(not recommended)*. Additionally, you may have to adjust your antivirus or antimalware program settings. See the software vendor for details.

## Port Forwarding

If your computer is behind a NAT, port forwarding will be required. [Here is a good tutorial on how to setup port forwarding](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide/). 

**Note:** Without port forwarding, the API request will only work either from the localhost or the LAN, if the firewall port is opened properly on the server.

## Usage

You can interact with the TTS_Listener through API calls, POSTMAN, CURL etc. Here's an example of how to do so using CURL:

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: API_KEY" -d '{"voice": "samantha", "text": "THIS_IS_WHERE_THE_TEXT_TO_BE_CONVERTED_GOES"}' http://your_ip_or_dns_name_here:LISTENING_PORT/tts --output NAME_OF_OUTPUT_FILE.wav
```

**Note:** The voice "*samantha*" is currently the only voice with this package. *More will be added soon.*

## Disclaimer

This is meant for private use as Flask is not for production. Feel free to fork and modify. Enjoy!

## Support
Reach us at: https://www.clarktribegames.com or [info@clarktribegames.com](mailto:info@clarktribegames.com)

## Product Usage
This product is used by: https://narrative.nexus | https://sam.antha.dev



Thanks,
- AznIronMan