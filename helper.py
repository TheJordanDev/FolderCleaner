from os import path, listdir
from pathlib import Path
from fnmatch import fnmatch
from config import Config, Target, Filter
from ui import MainWindowTab

class FileInstance:
    def __init__(self, file, config:Config, target:Target):
        self.file = file
        self.config = config
        
        self._target = target

        self.filter = None
        self.origin = None
        self.target = None

    def apply_filter(self, filter:Filter):
        self.filter = filter
        self.origin = path.join(self._target.path, self.file)
        self.target = path.join(self._target.path, filter.folder, self.file)

class FileInstance:
    def __init__(self, file, config:Config, target:Target):
        self.file = file
        self.config = config
        self.target = target
        self.filter = None
        self.origin:Path = Path(target.path) / file
        self.target_path:Path = None

    def apply_filter(self, filter:Filter):
        self.filter = filter
        self.target_path = Path(self.target.path) / filter.folder / self.file

def clean_folders(config: Config, window: 'MainWindowTab'):
    files: list[FileInstance] = []
    
    window.progress_bar.setValue(0)
    window.progress_bar.setMaximum(0)
    window.progress_bar.setLabelText('Looking for files to move...')

    filters_folders = [filter.folder for filter in config.filters]

    for target in config.targets:
        if path.isdir(target.path):
            for file in listdir(target.path):
                full_path = path.join(target.path, file)
                if path.isdir(full_path) and file in filters_folders:
                    continue
                file_instance = FileInstance(file, config, target)
                files.append(file_instance)

    window.progress_bar.setMaximum(len(files))
    window.progress_bar.setValue(0)
    window.progress_bar.setLabelText('Applying filters...')
    for file_instance in files:
        matched = False
        for filter in config.filters:
            for expression in filter.expressions:
                if fnmatch(file_instance.file, expression):
                    file_instance.apply_filter(filter)
                    matched = True
                    break
            if matched:
                break
        window.progress_bar.increment()

    window.progress_bar.setMaximum(len(files))
    window.progress_bar.setValue(0)
    window.progress_bar.setLabelText('Moving files...')
    moved_count = 0
    for file_instance in files:
        if file_instance.filter:
            target_dir = file_instance.target_path.parent
            if not target_dir.exists():
                target_dir.mkdir(parents=True, exist_ok=True)
            file_instance.origin.replace(file_instance.target_path)
            moved_count += 1
        window.progress_bar.increment()

    window.progress_bar.setLabelText(f'Done! Moved {moved_count} files.')
    window.progress_bar.setMaximum(100)
    window.progress_bar.setValue(100)