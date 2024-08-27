import platform
import os
import json
from rich.table import Table
from rich.console import Console
from rich.text import Text

console = Console()

OS = platform.system()
BASE_PAHT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config():
    def __init__(self, path:str, project_name:str):
        self.path_parent = path
        self.project_name = project_name
        self.os = OS
        self.path:str = None
        self.preact:bool = False
        self.uvicorn:bool = True
        self.gunicorn:bool = False
    
    def set_path(self, path:str):
        self.path_parent = path if path != '' else self.path_parent
    
    def set_name(self, name:str):
        self.project_name = name.replace(' ', '_') if name != '' and name is not None else self.project_name
        self.path = f'{self.path_parent}/{self.project_name}'
    
    def set_preact(self, preact:bool):
        self.preact = preact
        self.save_data()
    
    def set_uvicorn(self, uvicorn:bool):
        self.uvicorn = uvicorn
        self.save_data()
    
    def set_gunicorn(self, gunicorn:bool):
        self.gunicorn = gunicorn
        self.save_data()
    
    def project_data(self):
        return {attr: getattr(self, attr) for attr in dir(self) if not attr.startswith('__') and not callable(getattr(self, attr))}
    
    def print_table(self):
        self.load_data()
        table = Table(title="Config")
        table.add_column("Nombre", justify="left", style="cyan", no_wrap=True)
        table.add_column("Valor", justify="center", style="magenta")
        for key, value in self.project_data().items():
            table.add_row(key, str(value))
        console.print(table)
    
    def build_config(self):
        self.load_data()
        os.makedirs(f'{self.path_parent}/{self.project_name}', exist_ok=True)
        try:
            os.makedirs(f'{self.path_parent}/{self.project_name}/media', exist_ok=True)
            os.makedirs(f'{self.path_parent}/{self.project_name}/static', exist_ok=True)
            os.makedirs(f'{self.path_parent}/{self.project_name}/models', exist_ok=True)
            self.makefile(f'{self.path_parent}/{self.project_name}/models/__init__.py', exist_ok=True)
            self.makefile(f'{self.path_parent}/{self.project_name}/models/user.py', exist_ok=True, content='from sqlalchemy import Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base\n\nclass User(Base):\n    __tablename__ = "users"\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n    email = Column(String)')
            self.makefile(f'{self.path_parent}/{self.project_name}/requirements.txt', exist_ok=True, content='fastapi\nSQLAlchemy==2.0.32\nfastapi-admin==1.0.4')
            self.makefile(f'{self.path_parent}/{self.project_name}/.gitignore', exist_ok=True, content='.venv/\n')
            self.makefile(f'{self.path_parent}/{self.project_name}/README.md', exist_ok=True, content=f'# {self.project_name}')
            self.makefile(f'{self.path_parent}/{self.project_name}/settings.py', exist_ok=True, content=f'import os\nimport pathlib\n\nBASE_DIR = pathlib.Path(__file__).resolve().parent\n\nSECRET_KEY = os.getenv("SECRET_KEY")')
            self.makefile(f'{self.path_parent}/{self.project_name}/main.py', exist_ok=True, content=f'from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get("/")\ndef read_root():\n    return {{ "Hello": "World" }}')
            self.makefile(f'{self.path_parent}/{self.project_name}/__init__.py', exist_ok=True, content='from .main import app\n\n__all__ = ["app"]')
        except Exception as e:
            error_text = Text(e, style="red")
            console.print(error_text)
    
    def save_data(self):
        try:
            with open('./config.json','w') as file:
                json.dump(self.project_data(), file)
        except Exception as e:
            error_text = Text(e, style="red")
            console.print(error_text)
    
    def load_data(self):
        try:
            with open('./config.json','r') as file:
                data = json.load(file)
                for key, value in data.items():
                    setattr(self, key, value)
        except Exception as e:
            error_text = Text(e, style="red")
            console.print(error_text)
    
    def makefile(self, path:str, exist_ok:bool=False, content:str=''):
        if not os.path.exists(path):
            try:
                with open(path, 'w') as file:
                    file.write(content)
            except Exception as e:
                error_text = Text(e, style="red")
                console.print(error_text)
        elif exist_ok:
            try:
                with open(path, 'w') as file:
                    file.write(content)
            except Exception as e:
                error_text = Text(e, style="red")
                console.print(error_text)
        else:
            error_text = Text('El archivo ya existe', style="red")
            console.print(error_text)