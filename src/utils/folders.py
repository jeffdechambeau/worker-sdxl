import shutil
import os


def inspect_path(path):
    if not os.path.exists(path):
        print("The path does not exist.")
        return None

    if os.path.isfile(path):
        size = os.path.getsize(path)
        print(f"File Size: {size} bytes")

        if path.endswith('.log'):
            with open(path, 'r') as file:
                contents = file.read()
                return {"size": size, "contents": contents}
        else:
            return {"size": size}

    elif os.path.isdir(path):
        contents = os.listdir(path)
        print("Directory contents:")
        for item in contents:
            print(item)
        return {"contents": contents}
    else:
        print("It is neither a file nor a directory.")
        return {"nothing": True}


def delete_training_folder(folder_path):
    if 'workspace/witit' not in folder_path:
        print(f"Invalid path: {folder_path}")
        return
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Successfully deleted the folder: {folder_path}")
        except Exception as e:
            print(f"Failed to delete the folder: {folder_path}. Reason: {e}")
    else:
        print(
            f"The specified path does not exist or is not a directory: {folder_path}")
