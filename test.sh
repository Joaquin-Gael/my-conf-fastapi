source fastapi_base/.venv/bin/activate
cd fastapi_base
pip install -r requirements.txt
pip install "fastapi[standard]"
pip freeze > requirements.txt
fastapi dev app/main.py