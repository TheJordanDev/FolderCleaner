import os
from config import Config

def get_targets(config:Config):
    targets_files = {}
    for target in config.targets:
        if os.path.isdir(target):
            targets_files[target] = os.listdir(target)
        else:
            targets_files[target] = []
    return targets_files