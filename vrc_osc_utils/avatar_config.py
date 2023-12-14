from typing import NamedTuple
import json

class AddressTypePair(NamedTuple):
    address: str
    type: str

class ConfigParameter(NamedTuple):
    name: str
    input: AddressTypePair | None = None
    output: AddressTypePair | None = None

class AvatarConfig(NamedTuple):
    id: str
    name: str
    parameters: list[ConfigParameter]

def avatar_config_object_hook(json_dict: dict):
    if 'address' in json_dict and 'type' in json_dict:
        return AddressTypePair(**json_dict)
    elif 'name' in json_dict and ('input' in json_dict or 'output' in json_dict):
        return ConfigParameter(**json_dict)
    elif 'id' in json_dict and 'name' in json_dict and 'parameters' in json_dict:
        return AvatarConfig(**json_dict)
    return None
    