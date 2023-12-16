
import os
import json


def make_success_payload(username, token_name, class_name, output_file):
    return {
        "status": "success",
        "custom_checkpoint_path": output_file,
        "username": username,
        "token": token_name,
        "class": class_name,
        "cleanup_complete": True
    }


def make_error_payload(error):
    print(f"Error running training: {error}")
    return {
        "status": "error",
        "error": str(error),
        "cleanup_complete": True
    }


def unpack_json(json):
    username = json['username']
    images = json['images']
    resolution = json['training_resolution']
    token_name = json['token']
    class_name = json['class']
    model_path = json['model_path']

    return username, images, resolution, token_name, class_name, model_path


def delete_checkpoint(delete_path):
    if "witit-custom/checkpoints" not in delete_path:
        return {
            "status": "error",
            "error": "Invalid delete path"
        }
    try:
        os.remove(delete_path)
        return {
            "status": "success",
            "deleted_path": delete_path
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
