# Railway Deployment Guide for Django Todo App with Image Uploads

This guide provides step-by-step instructions for deploying the Django todo project to Railway, including PostgreSQL database integration and handling static and media files (like profile pictures) using Cloudinary.

## 1. Prerequisites

- A [Railway](https://railway.app) account.
- A [Cloudinary](https://cloudinary.com/) account (the free tier is sufficient).
- The [Railway CLI](https://docs.railway.app/cli/installation) installed on your local machine.
- [Git](https://git-scm.com/downloads) installed on your local machine.

## 2. Local Setup for Production

Before deploying, you need to prepare your Django project to work with PostgreSQL and Cloudinary.

### Step 2.1: Install Required Packages

Install packages for PostgreSQL, database URL parsing, Gunicorn (web server), and Cloudinary for media file storage.

```bash
pip install psycopg2-binary dj-database-url gunicorn cloudinary cloudinary-storage django-storages
```

### Step 2.2: Update `settings.py`

Modify `todo_project/settings.py` to handle database connections, static files, and media files for production.

```python
# todo_project/settings.py
import dj_database_url
import os

# ... (keep other settings like BASE_DIR, SECRET_KEY)

# Set DEBUG to False for production. It's better to use an environment variable.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Update ALLOWED_HOSTS to accept your Railway app's domain
ALLOWED_HOSTS = ['*'] # Or more securely, your railway app domain

# Add 'storages' to your INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    "todos",
    "storages",
]

# ... (keep MIDDLEWARE)

# Database Configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}')
    )
}

# ... (keep other settings)

# Static and Media Files (Cloudinary)
# ------------------------------------------------------------------------------
# Add this new section at the end of your settings.py

# Cloudinary credentials from environment variables
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Set the default file storage to Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# The URL that will be used to serve media files
MEDIA_URL = '/media/'
```

### Step 2.3: Update `.gitignore`

Ensure your `.gitignore` file is up to date to prevent committing local artifacts and environment files.

**`.gitignore`**:

```
# Python
__pycache__/
*.pyc
.venv/
db.sqlite3
media/
static/

# Environment
.env

# IDE
.vscode/
```

## 3. Create Configuration Files

Railway needs a few files to understand how to build and run your project.

### Step 3.1: `Procfile`

This file tells Railway what command to run to start your web server. Create a file named `Procfile` (no extension) in the root of your project.

**`Procfile`**:

```
web: gunicorn todo_project.wsgi
```

### Step 3.2: `runtime.txt`

This file specifies the Python version to use. Create a file named `runtime.txt` in the root directory.

**`runtime.txt`**:

```
python-3.12.6
```

_(Adjust the version if you used a different one locally)_.

### Step 3.3: Freeze Dependencies

Create a `requirements.txt` file so Railway knows which packages to install.

```bash
pip freeze > requirements.txt
```

## 4. Deploy to Railway

Now you're ready to initialize your project with Git and deploy it.

### Step 4.1: Initialize Git Repository

If you haven't already, initialize a Git repository and make your first commit.

```bash
git init
git add .
git commit -m "Prepare for deployment"
```

### Step 4.2: Initialize Railway Project

Log in to the Railway CLI and initialize your project.

```bash
railway login
railway init
```

Follow the prompts, choosing to create a new project.

### Step 4.3: Add PostgreSQL Service

From the Railway dashboard:

1.  Navigate to your newly created project.
2.  Click **+ New** and select **Database**.
3.  Choose **Add PostgreSQL**.

### Step 4.4: Configure Environment Variables

You need to provide Railway with your secret keys for Django, the database, and Cloudinary.

1.  **Get Cloudinary Credentials**:
    - Log in to your Cloudinary account.
    - On the dashboard, you will find your `Cloud Name`, `API Key`, and `API Secret`.

2.  **Set Variables in Railway**:
    - In your Railway project dashboard, go to the **Variables** tab for your Django app service.
    - The `DATABASE_URL` will be injected automatically by Railway.
    - Add the following new variables:
      - `SECRET_KEY`: Generate a new secret key. You can run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.
      - `DEBUG`: `False`
      - `CLOUDINARY_CLOUD_NAME`: Your Cloudinary Cloud Name.
      - `CLOUDINARY_API_KEY`: Your Cloudinary API Key.
      - `CLOUDINARY_API_SECRET`: Your Cloudinary API Secret.

### Step 4.5: Deploy the Code

Deploy your project by pushing your code to the `main` branch of the Railway-provided repository.

```bash
# This command may vary based on your git remote name
git push railway main
```

Railway will detect the push, build your project using `requirements.txt`, and start it using the `Procfile` command.

## 5. Post-Deployment: Run Migrations

After the first deployment, you must run your database migrations on the Railway server.

1.  Open the Railway dashboard for your project.
2.  Go to the **Deployments** tab and click on your latest deployment.
3.  You will see a shell/terminal interface. Run the migrate command:

```bash
python manage.py migrate
```

You may also want to create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

Your Django To-Do application is now live on Railway, with image uploads handled by Cloudinary!

You may also want to create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

Your Django To-Do application is now live on Railway!
