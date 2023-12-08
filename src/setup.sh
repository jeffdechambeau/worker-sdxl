#!/bin/bash

# Activate your environment
source /stable-diffusion-webui/env/bin/activate

# Function to download a file if it does not exist
download_if_not_exists() {
    local file_path="$1"
    local file_url="$2"
    local file_dir

    # Extract the directory path from the file_path
    file_dir=$(dirname "$file_path")

    # Ensure the directory exists
    if [ ! -d "$file_dir" ]; then
        echo "Directory $file_dir does not exist. Creating..."
        mkdir -p "$file_dir"
    fi

    # Download the file if it does not exist
    if [ ! -f "$file_path" ]; then
        echo "$file_path not found. Downloading..."
        wget -O "$file_path" "$file_url"
    else
        echo "$file_path already exists."
    fi
}

# Paths and URLs for the files
rundiffusionXL_path="/workspace/models/Stable-diffusion/rundiffusionXL.safetensors"
rundiffusionXL_url="https://www.dropbox.com/scl/fi/9n9q1rjbrdfnili9ca24i/rundiffusionXL_beta.safetensors?rlkey=2674n1a85jns6opu3wacp9haq&dl=1"

sdxl_vae_path="/workspace/models/VAE/sdxl_vae.safetensors"
sdxl_vae_url="https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors"

upscaler_path="/workspace/models/ESRGAN/4xBox.pth"
upscaler_url="https://drive.google.com/u/0/uc?id=1KToK9mOz05wgxeMaWj9XFLOE4cnvo40D&export=download"

codeformer_path="/stable-diffusion-webui/models/Codeformer/codeformer-v0.1.0.pth"
codeformer_url="https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth" 

facelib_path="/stable-diffusion-webui/repositories/CodeFormer/weights/facelib/detection_Resnet50_Final.pth"
facelib_url="https://github.com/xinntao/facexlib/releases/download/v0.1.0/detection_Resnet50_Final.pth"  

parser_path=" /stable-diffusion-webui/repositories/CodeFormer/weights/facelib/parsing_parsenet.pth"
parser_url="https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/parsing_parsenet.pth"

sd_path=""/stable-diffusion-webui/models/Stable-diffusion/v1-5-pruned-emaonly.safetensors
sd_url="https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors?download=true"

# Call the function with the path and URL for each file
# Uncomment the lines below as needed
download_if_not_exists "$rundiffusionXL_path" "$rundiffusionXL_url"
download_if_not_exists "$sdxl_vae_path" "$sdxl_vae_url"
download_if_not_exists "$upscaler_path" "$upscaler_url"
download_if_not_exists "$codeformer_path" "$codeformer_url"
download_if_not_exists "$facelib_path" "$facelib_url"
download_if_not_exists "$parser_path" "$parser_url"
download_if_not_exists "$sd_path" "$sd_url"

