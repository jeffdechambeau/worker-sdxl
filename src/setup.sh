#!/bin/bash
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



# Check for /workspace/stable-diffusion-webui and copy if not present
if [ ! -d "/workspace/stable-diffusion-webui" ]; then
    echo "stable-diffusion-webui not found in workspace. Copying now..."
    cp -r /stable-diffusion-webui /workspace/stable-diffusion-webui
fi

# Check for /workspace/kohya_ss and copy if not present
if [ ! -d "/workspace/kohya_ss" ]; then
    echo "kohya_ss not found in workspace. Copying now..."
    cp -r /kohya_ss /workspace/kohya_ss
fi

# Define paths, URLs, and softlink locations
sd_path=""/workspace/stable-diffusion-webui/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors
sd_url="https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors?download=true"
download_if_not_exists "$sd_path" "$sd_url"

rundiffusionXL_path="/workspace/stable-diffusion-webui/models/Stable-diffusion/rundiffusionXL.safetensors"
rundiffusionXL_url="https://www.dropbox.com/scl/fi/9n9q1rjbrdfnili9ca24i/rundiffusionXL_beta.safetensors?rlkey=2674n1a85jns6opu3wacp9haq&dl=1"
download_if_not_exists "$rundiffusionXL_path" "$rundiffusionXL_url"

sdxl_vae_path="/workspace/stable-diffusion-webui/models/VAE/sdxl_vae.safetensors"
sdxl_vae_url="https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors"
download_if_not_exists "$sdxl_vae_path" "$sdxl_vae_url" 

upscaler_path="/workspace/stable-diffusion-webui/models/ESRGAN/4xBox.pth"
upscaler_url="https://drive.google.com/u/0/uc?id=1KToK9mOz05wgxeMaWj9XFLOE4cnvo40D&export=download"
download_if_not_exists "$upscaler_path" "$upscaler_url" 

codeformer_path="/workspace/stable-diffusion-webui/models/Codeformer/codeformer-v0.1.0.pth"
codeformer_url="https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth" 
download_if_not_exists "$codeformer_path" "$codeformer_url"

facelib_path="/workspace/stable-diffusion-webui/repositories/CodeFormer/weights/facelib/detection_Resnet50_Final.pth"
facelib_url="https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"  
download_if_not_exists "$facelib_path" "$facelib_url"

parser_path=" /workspace/stable-diffusion-webui/repositories/CodeFormer/weights/facelib/parsing_parsenet.pth"
parser_url="https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/parsing_parsenet.pth"
download_if_not_exists "$parser_path" "$parser_url"

