# Anime-Recommender-System
deactivate

Remove-Item -Recurse -Force .venv

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

cd backend_flask

python app.py

npm install

cd frontend_react

npm run dev