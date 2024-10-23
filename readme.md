To run the application, including setting up Redis for Celery, you can follow the steps below:

### 1. **Create and activate a virtual environment**
```bash
python3 -m venv venv  
source venv/bin/activate  
```

### 2. **Install required dependencies**
Make sure to install the dependencies specified in the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. **Start the FastAPI server using Uvicorn**
Run the FastAPI application on port 8000:
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. **Start Redis server**
Celery requires Redis (or another message broker) to function. If Redis is not installed, you can install it:

- **On Linux (Ubuntu):**
  ```bash
  sudo apt-get update
  sudo apt-get install redis-server
  ```

- **On macOS (with Homebrew):**
  ```bash
  brew install redis
  ```

- **On Windows:** You can download Redis binaries from [here](https://redis.io/download) and follow the installation instructions for Windows.

After installation, start the Redis server:
```bash
redis-server
```

To check if Redis is running, you can use:
```bash
redis-cli ping
```
You should see `PONG` if Redis is running correctly.

### 5. **Run the Celery worker**
Once Redis is up and running, you can start the Celery worker:
```bash
celery -A app.celery_app.celery_app worker --loglevel=info
```

### Summary of commands to run the application with Redis:

```bash
# Step 1: Set up and activate virtual environment
python3 -m venv venv  
source venv/bin/activate  

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Start Redis server
redis-server

# Step 4: Start FastAPI server
uvicorn app.main:app --reload --port 8000

# Step 5: Start Celery worker
celery -A app.celery_app.celery_app worker --loglevel=info
```

Let me know if you need further assistance!