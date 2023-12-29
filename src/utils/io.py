
import os
import json


def make_success_payload(username, token_name, class_name, output_file, job_id):
    return {
        "job_id": job_id,
        "status": "success",
        "custom_checkpoint_path": output_file,
        "username": username,
        "token": token_name,
        "class": class_name,
        "cleanup_complete": True
    }


def make_error_payload(error, job_id):
    print(f"Error running training: {error}")
    return {
        "job_id": job_id,
        "status": "error",
        "error": str(error),
        "cleanup_complete": True
    }


def unpack_json(json):
    username = json['username']
    images = json['images']
    resolution = json.get("training_resolution", "512,512")
    token_name = json['token']
    class_name = json['class']
    model_path = json['model_path']
    job_id = json.get('job_id', None)
    epochs = json.get('epochs', 3)
    save_every_n_epochs = json.get('save_every_n_epochs', epochs)
    batch_size = json.get('batch_size', 1)
    learning_rate = json.get('learning_rate', 0.0001)

    return username, images, resolution, token_name, class_name, model_path, job_id, save_every_n_epochs, epochs, batch_size, learning_rate


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
