
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
