
import os

script_path = '/workspace/kohya_ss/sdxl_train.py'
model_path = '/workspace/stable-diffusion-webui/models/Stable-diffusion/sd_xl_base_1.0.safetensors'
train_dir_base = '/workspace/witit-custom/active_training'

SCRIPT_PATH = os.environ.get('SCRIPT_PATH', script_path)
PRETRAINED_MODEL_PATH = os.environ.get('PRETRAINED_MODEL_PATH', model_path)
LOGGING_DIR = os.environ.get('LOGGING_DIR', '/workspace/logs/')
CONFIG_PATH = os.environ.get('CONFIG_PATH', '/workspace/config/kohya_ss.json')
MAX_CPU_THREADS = os.environ.get('MAX_CPU_THREADS', 4)
TRAIN_DATA_DIR_BASE = os.environ.get('TRAIN_DATA_DIR_BASE', train_dir_base)
