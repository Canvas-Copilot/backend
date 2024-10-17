# Run the application

python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000

celery -A app.celery_app.celery_app worker --loglevel=info
