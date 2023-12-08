#!/bin/bash

source /stable-diffusion-webui/env/bin/activate

download_if_not_exists() {
    local file_path="$1"
    local file_url="$2"
    local file_dir

    file_dir=$(dirname "$file_path")

    if [ ! -d "$file_dir" ]; then
        echo "Directory $file_dir does not exist. Creating..."
        mkdir -p "$file_dir"
    fi

    if [ ! -f "$file_path" ]; then
        echo "$file_path not found. Downloading..."
        wget -O "$file_path" "$file_url"
    else
        echo "$file_path already exists."
    fi
}

# 

rundiffusionXL_path="/workspace/models/Stable-diffusion/rundiffusionXL.safetensors"
rundiffusionXL_url="https://www.dropbox.com/scl/fi/9n9q1rjbrdfnili9ca24i/rundiffusionXL_beta.safetensors?rlkey=2674n1a85jns6opu3wacp9haq&dl=1"
download_if_not_exists "$rundiffusionXL_path" "$rundiffusionXL_url"

sdxl_vae_path="/workspace/models/VAE/sdxl_vae.safetensors"
sdxl_vae_url="https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors"
download_if_not_exists "$sdxl_vae_path" "$sdxl_vae_url"

upscaler_path="/workspace/models/ESRGAN/4xBox.pth"
upscaler_url="https://drive.google.com/u/0/uc?id=1KToK9mOz05wgxeMaWj9XFLOE4cnvo40D&export=download"
download_if_not_exists "$upscaler_path" "$upscaler_url"

codeformer_path="/stable-diffusion-webui/models/Codeformer/codeformer-v0.1.0.pth"
codeformer_url="https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth" 
download_if_not_exists "$codeformer_path" "$codeformer_url"

facelib_path="/stable-diffusion-webui/repositories/CodeFormer/weights/facelib/detection_Resnet50_Final.pth"
facelib_url="https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"  
download_if_not_exists "$facelib_path" "$facelib_url"

parser_path=" /stable-diffusion-webui/repositories/CodeFormer/weights/facelib/parsing_parsenet.pth"
parser_url="https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/parsing_parsenet.pth"
download_if_not_exists "$parser_path" "$parser_url"

sd_path=""/stable-diffusion-webui/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors
sd_url="https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors?download=true"
download_if_not_exists "$sd_path" "$sd_url"

