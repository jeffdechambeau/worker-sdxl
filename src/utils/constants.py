
import os
is_dev = os.environ.get('IS_DEV')

LOCAL_URL = "http://127.0.0.1:3000"

script_path = '/workspace/kohya_ss/sdxl_train.py'
model_path = '/workspace/stable-diffusion-webui/models/Stable-diffusion/sd_xl_base_1.0.safetensors'
train_dir_base = '/workspace/witit-custom/active_training'


SCRIPT_PATH = os.environ.get('SCRIPT_PATH', script_path)
PRETRAINED_MODEL_PATH = os.environ.get('PRETRAINED_MODEL_PATH', model_path)
TRAIN_DATA_DIR_BASE = os.environ.get('TRAIN_DATA_DIR_BASE', train_dir_base)

LOGGING_DIR = os.environ.get('LOGGING_DIR', '/workspace/logs/')
CONFIG_FOLDER_PATH = os.environ.get('CONFIG_FOLDER', '/workspace/config')
MAX_CPU_THREADS = os.environ.get('MAX_CPU_THREADS', 4)


if is_dev:
    LOCAL_URL = "https://a8lbi00mdlwpal-3001.proxy.runpod.net"
    CONFIG_FOLDER_PATH = '/Users/jds/code/upwork/active/Nathaniel/worker-sdxl/builder/config'

KOHYA_CONFIG_PATH = CONFIG_FOLDER_PATH + '/kohya_ss.json'
ADETAILER_CONFIG_PATH = CONFIG_FOLDER_PATH + '/adetailer.json'
