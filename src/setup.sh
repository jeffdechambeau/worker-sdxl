

source /stable-diffusion-webui/env/bin/activate
python3 launch.py & 
# Define file paths and URLs
rundiffusionXL_path="/stable-diffusion-webui/models/Stable-diffusion/rundiffusionXL.safetensors"
rundiffusionXL_url="https://www.dropbox.com/scl/fi/9n9q1rjbrdfnili9ca24i/rundiffusionXL_beta.safetensors?rlkey=2674n1a85jns6opu3wacp9haq&dl=1"

sdxl_vae_path="/stable-diffusion-webui/models/VAE/sdxl_vae.safetensors"
sdxl_vae_url="https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors"

# Check for rundiffusionXL.safetensors and download if not present
if [ ! -f "$rundiffusionXL_path" ]; then
    echo "rundiffusionXL.safetensors not found. Downloading..."
    wget -O "$rundiffusionXL_path" "$rundiffusionXL_url"
else
    echo "rundiffusionXL.safetensors already exists."
fi

# Check for sdxl_vae.safetensors and download if not present
if [ ! -f "$sdxl_vae_path" ]; then
    echo "sdxl_vae.safetensors not found. Downloading..."
    wget -O "$sdxl_vae_path" "$sdxl_vae_url"
else
    echo "sdxl_vae.safetensors already exists."
fi