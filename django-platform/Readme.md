BE: Python 3.9 > Django Framework 4.1.7
pip: 23.0.1
    py -m pip install --upgrade pip

pip install pillow

FE: React JS SEO

Tai lieu huong dan
https://docs.djangoproject.com/en/4.1/intro/tutorial01/

1. Django install
python -m pip install django
or
python -m pip install django==2.2.11

2. Tạo project Django
django-admin startproject project_name
pip freeze > requirements.txt

3. Start Django Project
python manage.py runserver

4. Database
- Cai thu vien pyscopg2 (postgresql)
pip install psycopg2
- SQL
pip install pyodbc
pip install django-pyodbc-azure

https://www.javatpoint.com/django-database-migrations

- Chay Migrate
    * Dang ky <app_name> = 'infrastructure'
    INSTALLED_APPS = [
        ...
        'django-platform.infrastructure', # Migration entities
        ...
    ]

    + python manage.py makemigrations
        or python manage.py makemigrations <app_name>
        python manage.py makemigrations --name <migration_name> <app_name>
    + python manage.py migrate
        or python manage.py migrate <app_name>

## DevOps to Nginx
1. Set up your development environment:
    Install Python and Django on your local machine
    Create a new Django project and add your application code
    Install any necessary Python dependencies
    Test your application locally
2. Set up your production environment:
    Choose a cloud service provider, such as AWS or DigitalOcean
    Create a new virtual machine instance and configure the necessary security settings
    Install Nginx on the server
    Install any necessary system packages and dependencies
3. Configure Nginx to serve your Django application:
    Configure Nginx to listen on the appropriate ports
    Create an Nginx configuration file for your application
    Configure Nginx to serve static files
    Configure Nginx to forward requests to your Django application
4. Automate the deployment process:
    Set up a version control system, such as Git, to manage your code changes
    Write deployment scripts to automate the deployment process
    Use a tool like Ansible or Fabric to automate server configuration and deployment
    Use a continuous integration/continuous deployment (CI/CD) tool to automate the testing and deployment process
5. Monitor and maintain your production environment:
    Set up monitoring tools to track server performance and detect issues
    Implement automatic scaling to handle traffic spikes
    Regularly perform maintenance tasks, such as server updates and backups



    
