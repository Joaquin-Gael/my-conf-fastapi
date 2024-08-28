import platform
import os
import json
from rich.table import Table
from rich.console import Console
from rich.text import Text
import subprocess

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
        subprocess.run(['python','-m','venv', f'{self.path_parent}/{self.project_name}/.venv'])
        subprocess.run(['pip', 'install', '-r', f'{self.path_parent}/{self.project_name}/requirements.txt'])
        os.makedirs(f'{self.path_parent}/{self.project_name}', exist_ok=True)
        try:
            if self.preact:
                os.makedirs(f'{self.path_parent}/{self.project_name}/backend', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/backend/routers', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/backend/media', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/backend/models', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/backend/midelwares', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/__init__.py', exist_ok=True, content='from .main import app\n\n__all__ = ["app"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/routers/__init__.py', exist_ok=True, content='__all__ = ["router"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/midelwares/__init__.py', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/models/__init__.py', exist_ok=True, content='from .user import User')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/models/user.py', exist_ok=True, content='from sqlalchemy import Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base\n\nclass User(Base):\n    __tablename__ = "users"\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n    email = Column(String)')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/routers/router.py', exist_ok=True, content='from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get("/")\ndef read_root():\n    return {"Hello": "World"}')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/requirements.txt', exist_ok=True, content='fastapi\nSQLAlchemy==2.0.32\nfastapi-admin==1.0.4\nrich\nPyJWT==2.9.0')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/settings.py', exist_ok=True, content='import uuid\nimport os\nimport pathlib\n\nBASE_DIR = pathlib.Path(__file__).resolve().parent\n\nSECRET_KEY = os.getenv("SECRET_KEY")\n\nDATABASE_DIR=f"sqlite:///{BASE_DIR}/backend/database/database.db"\n\nMEDIA_DIR = f"{BASE_DIR}/media"\nMEDIA_ENDPOINT = "/media/"\n\nTEMPLATES_DIR = f"{BASE_DIR}/templates"\n\nSTAICS_DIR = f"{BASE_DIR}/static"\nSTAICS_ENDPOINT = "/static/"')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/main.py', exist_ok=True, content='from fastapi import FastAPI\nfrom .routers.router import router\nfrom .settings import (MEDIA_DIR, MEDIA_ENDPOINT, STAICS_DIR, STAICS_ENDPOINT)\nfrom .middlewares.token import TokenAuthMiddleware, CORSMiddleware\n\napp = FastAPI()\n\napp.include_router(router, prefix="/api", tags=["api"],responses={404: {"description": "Not found"}})\n\napp.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])\napp.add_middleware(TokenAuthMiddleware,activate = False, debug=True)\n\n\napp.mount(STAICS_ENDPOINT, StaticFiles(directory=STAICS_DIR), name="static")\n\n\n@app.on_event("startup")\nasync def startup_event():\n    creatre_database()\n\n@app.on_event("shutdown")\nasync def shutdown_event():\n    drop_database()\n\n\n@app.get("/")\ndef read_root():\n    return {{ "Hello": "World" }}')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/database.py', exist_ok=True, content='from .settings import DATABASE_DIR\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\nfrom sqlalchemy import create_engine\n\nengine = create_engine(DATA_BASE_URL)\n\nSession = sessionmaker(bind=engine)\n\nBase = declarative_base()\n\ndef creatre_database():\n    Base.metadata.create_all(engine)\n\ndef drop_database():\n    Base.metadata.drop_all(engine)\n\ndef get_session():\n    session = Session()\n    try:\n        yield session\n    finally:\n        session.close()')
                self.makefile(f'{self.path_parent}/{self.project_name}/backend/midelwares/token_auth.py', exist_ok=True, content=r"""
from fastapi import (responses, Request, status)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from rich.pretty import pprint
from datetime import datetime

class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, activate:bool, app, debug:bool=False):
        super().__init__(app)
        self.activate = activate
        self.debug = debug

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if self.debug:
            pprint(request)
            pprint("Headers:")
            pprint(dict(request.headers))
            pprint(f"IP: {request.client.host}")
            pprint(f"Port: {request.client.port}")
            pprint(f"Url: {request.url}")
            pprint(f"Url Query: {request.url.query}")
            pprint(f"Method: {request.method}")
            pprint(f"Date: {datetime.now()}")
            pprint(f"Token: {token}")

        if (not token) and self.activate:
            return responses.JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing token"},
            )
        return await call_next(request)""")
            else:
                os.makedirs(f'{self.path_parent}/{self.project_name}/routers', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/media', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/static', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/models', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/midelwares', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/templates', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/__init__.py', exist_ok=True, content='from .main import app\n\n__all__ = ["app"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/routers/__init__.py', exist_ok=True, content='__all__ = ["router"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/midelwares/__init__.py', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/models/__init__.py', exist_ok=True, content='from .user import User')
                self.makefile(f'{self.path_parent}/{self.project_name}/models/user.py', exist_ok=True, content='from sqlalchemy import Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base\n\nclass User(Base):\n    __tablename__ = "users"\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n    email = Column(String)')
                self.makefile(f'{self.path_parent}/{self.project_name}/routers/router.py', exist_ok=True, content='from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get("/")\ndef read_root():\n    return {"Hello": "World"}')
                self.makefile(f'{self.path_parent}/{self.project_name}/requirements.txt', exist_ok=True, content='fastapi\nSQLAlchemy==2.0.32\nfastapi-admin==1.0.4\nrich\nPyJWT==2.9.0')
                self.makefile(f'{self.path_parent}/{self.project_name}/settings.py', exist_ok=True, content='import uuid\nimport os\nimport pathlib\n\nBASE_DIR = pathlib.Path(__file__).resolve().parent\n\nSECRET_KEY = os.getenv("SECRET_KEY")\n\nDATABASE_DIR=f"sqlite:///{BASE_DIR}/backend/database/database.db"\n\nMEDIA_DIR = f"{BASE_DIR}/media"\nMEDIA_ENDPOINT = "/media/"\n\nTEMPLATES_DIR = f"{BASE_DIR}/templates"\n\nSTAICS_DIR = f"{BASE_DIR}/static"\nSTAICS_ENDPOINT = "/static/"')
                self.makefile(f'{self.path_parent}/{self.project_name}/main.py', exist_ok=True, content='from fastapi import FastAPI\nfrom .routers.router import router\nfrom .settings import (MEDIA_DIR, MEDIA_ENDPOINT, STAICS_DIR, STAICS_ENDPOINT)\nfrom .middlewares.token import TokenAuthMiddleware, CORSMiddleware\n\napp = FastAPI()\n\napp.include_router(router, prefix="/api", tags=["api"],responses={404: {"description": "Not found"}})\n\napp.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])\napp.add_middleware(TokenAuthMiddleware,activate = False, debug=True)\n\n\napp.mount(STAICS_ENDPOINT, StaticFiles(directory=STAICS_DIR), name="static")\napp.mount(MEDIA_ENDPOINT, StaticFiles(directory=MEDIA_DIR), name="media")\n\n\n@app.on_event("startup")\nasync def startup_event():\n    creatre_database()\n\n@app.on_event("shutdown")\nasync def shutdown_event():\n    drop_database()\n\n\n@app.get("/")\ndef read_root():\n    return {{ "Hello": "World" }}')
                self.makefile(f'{self.path_parent}/{self.project_name}/database.py', exist_ok=True, content='from .settings import DATABASE_DIR\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\nfrom sqlalchemy import create_engine\n\nengine = create_engine(DATA_BASE_URL)\n\nSession = sessionmaker(bind=engine)\n\nBase = declarative_base()\n\ndef creatre_database():\n    Base.metadata.create_all(engine)\n\ndef drop_database():\n    Base.metadata.drop_all(engine)\n\ndef get_session():\n    session = Session()\n    try:\n        yield session\n    finally:\n        session.close()')
                self.makefile(f'{self.path_parent}/{self.project_name}/midelwares/token_auth.py', exist_ok=True, content=r"""
from fastapi import (responses, Request, status)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from rich.pretty import pprint
from datetime import datetime

class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, activate:bool, app, debug:bool=False):
        super().__init__(app)
        self.activate = activate
        self.debug = debug

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if self.debug:
            pprint(request)
            pprint("Headers:")
            pprint(dict(request.headers))
            pprint(f"IP: {request.client.host}")
            pprint(f"Port: {request.client.port}")
            pprint(f"Url: {request.url}")
            pprint(f"Url Query: {request.url.query}")
            pprint(f"Method: {request.method}")
            pprint(f"Date: {datetime.now()}")
            pprint(f"Token: {token}")

        if (not token) and self.activate:
            return responses.JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing token"},
            )
        return await call_next(request)""")
            
            self.makefile(f'{self.path_parent}/{self.project_name}/.gitignore', exist_ok=True, content='.venv/\n')
            self.makefile(f'{self.path_parent}/{self.project_name}/README.md', exist_ok=True, content=f'# {self.project_name}')
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
            pass
        else:
            error_text = Text('El archivo ya existe', style="red")
            console.print(error_text)