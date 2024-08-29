import platform
import os
import json
from rich.table import Table
from rich.console import Console
from rich.text import Text
import subprocess

html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Config FastAPI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background-color: white;
            color: black;
        }
        .logo {
            width: 100px;
            height: auto;
        }
        h1 {
            font-size: 4rem;
            margin-bottom: 1.5rem;
        }
        .btn-group {
            margin-top: 1.5rem;
        }
    </style>
</head>
<body>
    <!-- Logo de FastAPI -->
    <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaWRZTWlkIiB2aWV3Qm94PSIwIDAgMjU2IDI1NiI+PHBhdGggZD0iTTEyOCAwQzU3LjMzIDAgMCA1Ny4zMyAwIDEyOHM1Ny4zMyAxMjggMTI4IDEyOCAxMjgtNTcuMzMgMTI4LTEyOFMyMDEuNjcgMCAxMjggMFptLTYuNjcgMjMwLjYwNXYtODAuMjg4SDc2LjY5OWw2NC4xMjgtMTI0LjkyMnY4MC4yODhoNDIuOTY2TDEyMS4zMyAyMzAuNjA1WiIgZmlsbD0iIzAwOTY4OCI+PC9wYXRoPjwvc3ZnPg==" alt="FastAPI logo" class="logo">

    <!-- Texto Principal -->
    <h1>My Config FastAPI</h1>

    <!-- Botones -->
    <div class="btn-group">
        <a href="/api/admin" class="btn btn-dark">Admin</a>
        <a href="/docs" class="btn btn-outline-dark">Docs</a>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

admin_html = """
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Administrador</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .sidebar {
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 100;
            width: 250px;
            background: #f8f9fa;
            padding: 20px;
        }

        .sidebar a {
            text-decoration: none;
            color: #333;
            display: block;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 5px;
        }

        .sidebar a:hover {
            background-color: #e9ecef;
        }

        .main-content {
            margin-left: 250px;
            padding: 20px;
        }
    </style>
</head>

<body>

    <div class="sidebar">
        <h4>Admin Panel</h4>
        <a href="#">Dashboard</a>
        <a href="#">Gestión de Usuarios</a>
        <a href="#">Gestión de Contenidos</a>
        <a href="#">Configuración</a>
        <a href="#">Estadísticas</a>
        <a href="#">API</a>
    </div>

    <div class="main-content">
        <header class="d-flex justify-content-between align-items-center mb-4">
            <h1>Dashboard</h1>
            <button class="btn btn-primary">Cerrar sesión</button>
        </header>

        <section>
            <h2>Bienvenido al Panel de Administrador</h2>
            <p>Aquí puedes gestionar todos los aspectos de la web, servidor, y API.</p>

            <!-- Puedes agregar aquí más contenido, gráficos, tablas, etc. -->
        </section>
    </div>

    <!-- jQuery CDN -->
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.7/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.min.js"></script>
    <script type="module" src="/static/js/index.js"></script>

</body>

</html>
"""

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
        self.only_api:bool = False
    
    def set_api(self, only_api:bool):
        self.only_api = only_api
        self.save_data()

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
        os.makedirs(f'{self.path_parent}/{self.project_name}', exist_ok=True)
        try:
            if self.preact:
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/backend', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/backend/routers', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/backend/media', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/backend/models', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/backend/middlewares', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/__init__.py', exist_ok=True, content='from .main import app\n\n__all__ = ["app"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/routers/__init__.py', exist_ok=True, content='__all__ = ["router"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/middlewares/__init__.py', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/models/__init__.py', exist_ok=True, content='from .user import User')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/models/user.py', exist_ok=True, content='from sqlalchemy import Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base\n\nclass User(Base):\n    __tablename__ = "users"\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n    email = Column(String)')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/routers/router.py', exist_ok=True, content='from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get("/")\ndef read_root():\n    return {"Hello": "World"}')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/settings.py', exist_ok=True, content='import uuid\nimport os\nimport pathlib\n\nBASE_DIR = pathlib.Path(__file__).resolve().parent\n\nSECRET_KEY = os.getenv("SECRET_KEY")\n\nDATABASE_DIR=f"sqlite:///{BASE_DIR}/backend/database.db"\n\nMEDIA_DIR = f"{BASE_DIR}/media"\nMEDIA_ENDPOINT = "/media/"\n\nTEMPLATES_DIR = f"{BASE_DIR}/templates"\n\nSTAICS_DIR = f"{BASE_DIR}/static"\nSTAICS_ENDPOINT = "/static/"')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/main.py', exist_ok=True, content='from fastapi import FastAPI\nfrom .routers.router import router\nfrom .settings import (MEDIA_DIR, MEDIA_ENDPOINT, STAICS_DIR, STAICS_ENDPOINT)\nfrom .middlewares.token_auth import TokenAuthMiddleware, CORSMiddleware\nfrom .database import (creatre_database, drop_database)\n\napp = FastAPI()\n\napp.include_router(router, prefix="/api", tags=["api"],responses={404: {"description": "Not found"}})\n\napp.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])\napp.add_middleware(TokenAuthMiddleware,activate = False, debug=True)\n\n\napp.mount(STAICS_ENDPOINT, StaticFiles(directory=STAICS_DIR), name="static")\n\n\n@app.on_event("startup")\nasync def startup_event():\n    creatre_database()\n\n@app.on_event("shutdown")\nasync def shutdown_event():\n    drop_database()\n\n\n@app.get("/")\ndef read_root():\n    return { "Hello": "World" }')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/database.py', exist_ok=True, content='from .settings import DATABASE_DIR\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\nfrom sqlalchemy import create_engine\n\nengine = create_engine(DATA_BASE_URL)\n\nSession = sessionmaker(bind=engine)\n\nBase = declarative_base()\n\ndef creatre_database():\n    Base.metadata.create_all(engine)\n\ndef drop_database():\n    Base.metadata.drop_all(engine)\n\ndef get_session():\n    session = Session()\n    try:\n        yield session\n    finally:\n        session.close()')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/backend/middlewares/token_auth.py', exist_ok=True, content=r"""
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
            elif self.only_api:
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/routers', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/media', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/models', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/middlewares', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/__init__.py', exist_ok=True, content='from .main import app\n\n__all__ = ["app"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/routers/__init__.py', exist_ok=True, content='__all__ = ["router"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/middlewares/__init__.py', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/models/__init__.py', exist_ok=True, content='from .user import User')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/models/user.py', exist_ok=True, content='from sqlalchemy import Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base\n\nclass User(Base):\n    __tablename__ = "users"\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n    email = Column(String)')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/routers/router.py', exist_ok=True, content='from fastapi import APIRouter, Request\nfrom fastapi.templating import Jinja2Templates\nfrom ..settings import TEMPLATES_DIR\n\ntemplates = Jinja2Templates(directory=TEMPLATES_DIR)\n\ntemplates = Jinja2Templates(directory=TEMPLATES_DIR)\n\n\nrouter = APIRouter()\n\n@router.get("/")\ndef read_root():\n    return {"Hello": "World"}\n\n@router.get("/index")\nasync def index(request: Request):\n    return templates.TemplateResponse("index.html", {"request": request})')
                self.makefile(f'{self.path_parent}/{self.project_name}/requirements.txt', exist_ok=True, content='fastapi\nSQLAlchemy==2.0.32\nfastapi-admin==1.0.4\nrich\nPyJWT==2.9.0')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/settings.py', exist_ok=True, content='import uuid\nimport os\nimport pathlib\n\nBASE_DIR = pathlib.Path(__file__).resolve().parent\n\nSECRET_KEY = os.getenv("SECRET_KEY")\n\nDATABASE_DIR=f"sqlite:///{BASE_DIR}/database.db"\n\nMEDIA_DIR = f"{BASE_DIR}/media"\nMEDIA_ENDPOINT = "/media/"')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/main.py', exist_ok=True, content='from fastapi import FastAPI\nfrom fastapi.staticfiles import StaticFiles\nfrom .routers.router import router\nfrom .settings import (MEDIA_DIR, MEDIA_ENDPOINT, STAICS_DIR, STAICS_ENDPOINT)\nfrom .middlewares.token_auth import TokenAuthMiddleware, CORSMiddleware\nfrom .database import (creatre_database, drop_database)\n\napp = FastAPI()\n\napp.include_router(router, prefix="/api", tags=["api"],responses={404: {"description": "Not found"}})\n\napp.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])\napp.add_middleware(TokenAuthMiddleware,activate = False, debug=True)\n\n\napp.mount(STAICS_ENDPOINT, StaticFiles(directory=STAICS_DIR), name="static")\napp.mount(MEDIA_ENDPOINT, StaticFiles(directory=MEDIA_DIR), name="media")\n\n\n@app.on_event("startup")\nasync def startup_event():\n    creatre_database()\n\n@app.on_event("shutdown")\nasync def shutdown_event():\n    drop_database()\n\n\n@app.get("/")\ndef read_root():\n    return { "Hello": "World" }')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/database.py', exist_ok=True, content='from .settings import DATABASE_DIR\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\nfrom sqlalchemy import create_engine\n\nengine = create_engine(DATABASE_DIR)\n\nSession = sessionmaker(bind=engine)\n\nBase = declarative_base()\n\ndef creatre_database():\n    Base.metadata.create_all(engine)\n\ndef drop_database():\n    Base.metadata.drop_all(engine)\n\ndef get_session():\n    session = Session()\n    try:\n        yield session\n    finally:\n        session.close()')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/middlewares/token_auth.py', exist_ok=True, content=r"""
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
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/routers', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/media', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/static', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/models', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/middlewares', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/templates', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/static/css', exist_ok=True)
                os.makedirs(f'{self.path_parent}/{self.project_name}/app/static/js', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/static/js/index.js', exist_ok=True, content='$(()=>{\n    alert("Hello World")\n});')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/templates/index.html', exist_ok=True, content=html)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/templates/admin.html', exist_ok=True, content=admin_html)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/__init__.py', exist_ok=True, content='from .main import app\n\n__all__ = ["app"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/routers/__init__.py', exist_ok=True, content='__all__ = ["router"]')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/middlewares/__init__.py', exist_ok=True)
                self.makefile(f'{self.path_parent}/{self.project_name}/app/models/__init__.py', exist_ok=True, content='from .user import User')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/models/user.py', exist_ok=True, content='from sqlalchemy import Column, Integer, String\nfrom sqlalchemy.ext.declarative import declarative_base\n\nBase = declarative_base\n\nclass User(Base):\n    __tablename__ = "users"\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n    email = Column(String)')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/routers/router.py', exist_ok=True, content='from fastapi import APIRouter, Request\nfrom fastapi.templating import Jinja2Templates\nfrom ..settings import TEMPLATES_DIR\n\ntemplates = Jinja2Templates(directory=TEMPLATES_DIR)\n\ntemplates = Jinja2Templates(directory=TEMPLATES_DIR)\n\n\nrouter = APIRouter()\n\n@router.get("/")\ndef read_root():\n    return {"Hello": "World"}\n\n@router.get("/index")\nasync def index(request: Request):\n    return templates.TemplateResponse("index.html", {"request": request}) \n\n@router.get("/admin")\ndef admin(request: Request):\n    return templates.TemplateResponse("admin.html", {"request": request})')
                self.makefile(f'{self.path_parent}/{self.project_name}/requirements.txt', exist_ok=True, content='fastapi\nSQLAlchemy==2.0.32\nfastapi-admin==1.0.4\nrich\nPyJWT==2.9.0')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/settings.py', exist_ok=True, content='import uuid\nimport os\nimport pathlib\n\nBASE_DIR = pathlib.Path(__file__).resolve().parent\n\nSECRET_KEY = os.getenv("SECRET_KEY")\n\nDATABASE_DIR=f"sqlite:///{BASE_DIR}/database.db"\n\nMEDIA_DIR = f"{BASE_DIR}/media"\nMEDIA_ENDPOINT = "/media/"\n\nTEMPLATES_DIR = f"{BASE_DIR}/templates"\n\nSTAICS_DIR = f"{BASE_DIR}/static"\nSTAICS_ENDPOINT = "/static/"')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/main.py', exist_ok=True, content='from fastapi import FastAPI\nfrom fastapi.staticfiles import StaticFiles\nfrom .routers.router import router\nfrom .settings import (MEDIA_DIR, MEDIA_ENDPOINT, STAICS_DIR, STAICS_ENDPOINT)\nfrom .middlewares.token_auth import TokenAuthMiddleware, CORSMiddleware\nfrom .database import (creatre_database, drop_database)\n\napp = FastAPI()\n\napp.include_router(router, prefix="/api", tags=["api"],responses={404: {"description": "Not found"}})\n\napp.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])\napp.add_middleware(TokenAuthMiddleware,activate = False, debug=True)\n\n\napp.mount(STAICS_ENDPOINT, StaticFiles(directory=STAICS_DIR), name="static")\napp.mount(MEDIA_ENDPOINT, StaticFiles(directory=MEDIA_DIR), name="media")\n\n\n@app.on_event("startup")\nasync def startup_event():\n    creatre_database()\n\n@app.on_event("shutdown")\nasync def shutdown_event():\n    drop_database()\n\n\n@app.get("/")\ndef read_root():\n    return { "Hello": "World" }')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/database.py', exist_ok=True, content='from .settings import DATABASE_DIR\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\nfrom sqlalchemy import create_engine\n\nengine = create_engine(DATABASE_DIR)\n\nSession = sessionmaker(bind=engine)\n\nBase = declarative_base()\n\ndef creatre_database():\n    Base.metadata.create_all(engine)\n\ndef drop_database():\n    Base.metadata.drop_all(engine)\n\ndef get_session():\n    session = Session()\n    try:\n        yield session\n    finally:\n        session.close()')
                self.makefile(f'{self.path_parent}/{self.project_name}/app/middlewares/token_auth.py', exist_ok=True, content=r"""
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
            self.makefile(f'{self.path_parent}/{self.project_name}/requirements.txt', exist_ok=True, content="""
aiofiles==24.1.0
aioredis==2.0.1
aiosqlite==0.17.0
annotated-types==0.7.0
anyio==4.4.0
async-timeout==4.0.3
babel==2.16.0
bcrypt==4.2.0
certifi==2024.7.4
click==8.1.7
dnspython==2.6.1
email_validator==2.2.0
fastapi==0.112.2
fastapi-cli==0.0.5
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.5
httptools==0.6.1
httpx==0.27.2
idna==3.8
iso8601==1.1.0
Jinja2==3.1.4
markdown-it-py==3.0.0
MarkupSafe==2.1.5
mdurl==0.1.2
pendulum==3.0.0
pydantic==2.8.2
pydantic_core==2.20.1
Pygments==2.18.0
PyJWT==2.9.0
pypika-tortoise==0.1.6
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
python-multipart==0.0.9
pytz==2024.1
PyYAML==6.0.2
rich==13.8.0
shellingham==1.5.4
six==1.16.0
sniffio==1.3.1
SQLAlchemy==2.0.32
starlette==0.38.2
time-machine==2.15.0
tortoise-orm==0.21.6
typer==0.12.5
typing_extensions==4.12.2
tzdata==2024.1
uvicorn==0.30.6
uvloop==0.20.0
watchfiles==0.24.0
websockets==13.0.1
""")
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
        self.makefile(f'./config.json', exist_ok=True, content='{}')
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