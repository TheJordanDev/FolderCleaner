import os, sys
from json import dumps, loads, JSONEncoder
from pathlib import Path
home = Path.home()

class Filter(JSONEncoder):
    def __init__(self, name, expressions, folder):
        self.name = name
        self.expressions = expressions
        self.folder = folder

    @staticmethod
    def from_json(data):
        return Filter(data['name'], data['expressions'], data['folder'])
    
    def json(self):
        return {
            'name': self.name,
            'expressions': self.expressions,
            'folder': self.folder
        }

    def __str__(self):
        return f'{self.name} ({", ".join(self.expressions)})'

    def __repr__(self):
        return f'Filter({self.name}, {self.expressions}, {self.folder})'

class Target(JSONEncoder):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    @staticmethod
    def from_json(data):
        return Target(data['name'], data['path'])

    def json(self):
        return {
            'name': self.name,
            'path': self.path
        }

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Target({self.name}, {self.path})'

class Config:
    theme = 'dark_blue.xml'
    filters = [
        Filter('Applications', ['*.exe', '*.msi', '*.dmg', '*.deb', '*.rpm'], 'Applications'),
        Filter('Archives', ['*.zip', '*.rar', '*.7z', '*.tar'], 'Archives'),
        Filter('Documents', ['*.doc', '*.docx', '*.pdf', '*.txt', '*.ppt', '*.pptx', '*.xls', '*.xlsx'], 'Documents'),
        Filter('Images', ['*.jpg', '*.png', '*.jpeg', '*.gif', '*.bmp'], 'Images'),
        Filter('Music', ['*.mp3', '*.wav', '*.ogg', '*.flac', '*.wma'], 'Music'),
        Filter('Scripts', ['*.py', '*.js', '*.sh', '*.bat', '*.cmd'], 'Scripts'),
        Filter('Videos', ['*.mp4', '*.mkv', '*.avi', '*.mov', '*.flv'], 'Videos'),
        Filter('Others', [ '*' ], 'Others')
    ]

    targets = [
        Target("Téléchargements", (home / 'Downloads').as_posix()),
    ]

    def __init__(self):
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (e.g., with PyInstaller)
            self.exe_path = Path(sys.executable).parent
        else:
            # If the application is run as a script
            self.exe_path = Path(__file__).parent

        if not os.path.exists(self.exe_path / 'fc.conf'):
            self.save()
        else:
            self.load()

    def save(self):
        if not os.path.exists(self.exe_path):
            os.makedirs(self.exe_path, exist_ok=True)
        with open(self.exe_path / 'fc.conf', 'w', encoding="utf-8") as f:
            f.write(dumps(self.json(), ensure_ascii=False))

    def load(self):
        if not os.path.exists(self.exe_path):
            os.makedirs(self.exe_path, exist_ok=True)
        with open(self.exe_path / 'fc.conf', 'r', encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                self.save()
                return
            data = loads(content)
            self.theme = data['theme']
            self.filters = [Filter.from_json(filter) for filter in data['filters']]
            self.targets = [Target.from_json(target) for target in data['targets']]

    def json(self):
        return {
            'theme': self.theme,
            'filters': [filter.json() for filter in self.filters],
            'targets': [target.json() for target in self.targets]
        }