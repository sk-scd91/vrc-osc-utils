import json
import os

from vrc_osc_utils.avatar_config import avatar_config_object_hook, AvatarConfig

def get_avatar_config_file(id: str, user_id: str = None):
    home_path = os.getenv("HOMEPATH") if os.name == "nt" else "~"
    osc_path = os.path.join(home_path, "AppData", "LocalLow", "VRChat", "VRChat", "OSC")
    for user_dir in os.listdir(osc_path):
        if not user_id or user_dir == user_id:
            file_path = os.path.join(osc_path, user_dir, "Avatars", f"{id}.json")
            if os.path.exists(file_path):
                return file_path
    raise FileNotFoundError(f"Avatar with id {id} was not found.")

def get_config_from_file(path: str) -> AvatarConfig:
    with open(path) as file:
        return json.load(file, object_hook=avatar_config_object_hook)