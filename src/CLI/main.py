import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import Config, BASE_PAHT
from rich.console import Console
from rich.text import Text
import pyfiglet
import click
import subprocess

console = Console()
msg = pyfiglet.figlet_format('My Conf FastAPI')
version = '1.0.0'

# Crear una instancia de Config y cargar los datos previos
config = Config(BASE_PAHT, 'default_project_name')
config.load_data()  # Cargar los datos guardados previamente

@click.group()
@click.version_option(version=version, message=f"{msg}", show_choices=True)
def main():
    pass

@main.command()
@click.option('--path', '-p', type=str, required=False, help='Ruta del proyecto')
@click.option('--name', '-n', type=str, required=False, help='Nombre del proyecto')
@click.option('--preact', '-pr', is_flag=True, help='Instalar preact')
@click.option('--uvicorn', '-u', is_flag=True, help='Instalar uvicorn')
@click.option('--gunicorn', '-g', is_flag=True, help='Instalar gunicorn')
def set_config(path, name, preact, uvicorn, gunicorn) -> None:
    npm_version = subprocess.run(['npm','--version'], capture_output=True, text=True)
    if npm_version:
        if preact:
            config.set_preact(preact)
        if uvicorn:
            config.set_uvicorn(uvicorn)
        if gunicorn:
            config.set_gunicorn(gunicorn)
    else:
        error_text = Text('Npm no está instalado o no es la versión correcta.', style="bold red")
        console.print(error_text)

    python_version = subprocess.run(['python','--version'], capture_output=True, text=True)
    if python_version:
        config.set_path(path)
        config.set_name(name)
        config.print_table()
        config.save_data()  # Guardar los cambios
        resultado_venv = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        if 'virtualenv' in resultado_venv.stdout:
            console.print("Virtualenv está instalado.")
        else:
            error_text = Text("Virtualenv no está instalado.", style="bold red")
            console.print(error_text)
    else:
        error_text = Text('Python no está instalado o no es la versión correcta.', style="bold red")
        console.print(error_text)


@main.command()
def view_config():
    config.print_table()

@main.command()
def build_config():
    config.build_config()
    config.save_data()

if __name__ == '__main__':
    main()
