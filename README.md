# HHManagement

## Setup Instructions

### 1. Set up the virtual environment

To create and activate the virtual environment, run the following commands:

```bash
python -m venv venv
```

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 2. Install the required dependencies

After activating the virtual environment, install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

### 3. Running the Flask Application

To run the Flask application, use the following command:

```bash
flask run
```

This will start the Flask development server, which will be available by default at `http://127.0.0.1:5000`.

### 4. Setting Up the Database

To set up the database, follow these steps:

1. Open the Flask shell:
   ```bash
   flask shell
   ```

2. Initialize the database:
   ```bash
   flask db init
   ```

3. Create the initial migration:
   ```bash
   flask db migrate -m "Initial migration"
   ```

4. Apply the migration to the database:
   ```bash
   flask db upgrade
   ```

This will set up the database schema according to your models.

### 5. Setting Up and Using Celery

To set up and use Celery for background tasks, follow these steps:


## Running Celery Worker

To start the Celery worker, use the following command:

```bash
celery --app app.celery worker --loglevel=info --pool=solo
```
This will set up Celery to handle background tasks in your Flask application.

## Running Celery Beat
   
To start the Celery Beat scheduler, use the following command:

```bash
celery -A app.tasks beat --loglevel=info
```
This will set up Celery Beat to schedule periodic tasks in your Flask application.


## Stopping the Celery Worker

To stop the Celery worker gracefully, use the following command:

```bash
celery --app app.celery control shutdown
```

To clear all data from the Redis database, use the following command:

```bash
redis-cli FLUSHDB
```


## Starting Redis Server
To start the Redis server, use the following command:

```bash
redis-server
```




# HHManagement

## Setup Instructions

### 1. Set up the virtual environment

To create and activate the virtual environment, run the following commands:

```bash
python -m venv venv
```

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- **Mac/Linux**:
  ```bash
   source venv/bin/activate
   ```

### 2. Install the required dependencies

After activating the virtual environment, install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

### 3. Running the Flask Application

To run the Flask application, use the following command:

```bash
flask run
```

### 4. Redis Server Setup

To start the Redis server, use the following command:

```bash
redis-server
```

To clear all data from the Redis database, use the following command:

```bash
redis-cli FLUSHDB
```

### 5. celery worker setup

To start the Celery worker, use the following command:

```bash
celery --app app.celery worker --loglevel=info --pool=solo
```

### 6. celery beat setup

To start the Celery Beat scheduler, use the following command:

```bash
celery -A app.tasks beat --loglevel=info
```


## Stopping the Celery Worker

To stop the Celery worker gracefully, use the following command:

```bash
celery --app app.celery control shutdown
```

To clear all data from the Redis database, use the following command:

```bash
redis-cli FLUSHDB
```