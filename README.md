# Adrian's Python Advanced Diploma (APAD) - Twitter Clone

The API can still be used by another frontend application separately as all endpoints are available. 
It's fully asynchronous and easy to use. It can be 

## **Manual Configuration**

### Step 1: Prerequisites

Before you begin, make sure you have the following prerequisites installed on your system (Linux-based OS):

- **Docker Desktop 4.22.1**
- **docker-compose 1.29.2**

### Step 2: Cloning the Repository

- Clone the project repository to your computer
> ``git clone https://gitlab.skillbox.ru/adrian_babira/python_advanced_diploma.git``

### Step 3: **Docker-Compose**
- Enter the repository in terminal:  
> ``cd python_advanced_diploma/run_scripts``
- If necessary, modify the variables from the app.env and db.env files.
- Run in terminal to perform testing:
> ``sh start_tests.sh``

- Run in terminal to start application:

> ``sh start_prod.sh``
   
### Step 4: Use app:
- Open in internet browser http://localhost to open start page. 
- Open http://localhost:8000/docs to open Swagger


### Step 4: Use linters:
- Before you begin, make sure you have the following prerequisites installed on your system (Linux-based OS):
- **Python 3.11.5**
- Enter the repository in terminal:  
> ``cd python_advanced_diploma``
- To isolate project dependencies and avoid conflicts with system libraries, it's recommended to create and activate a virtual environment. Follow these steps:

1. Create a virtual environment in the project's root folder:

   ```bash
   python -m venv venv
2. Activate the virtual environment based on your operating system:
   * ***Linux***
    ```bash
    source venv/bin/activate
    ```
After activating the virtual environment, install the project dependencies using the package manager for your application stack:
- For python use `pip`:
  * ***Dependencies for the linters environment:***
   ```bash
   pip install -r requirements_test.txt
    ```

- Enter the run_scripts folder in terminal:
> ``cd run_scripts``
- Run in terminal to perform linters:
> ``sh start_linters.sh``



**APAD** uses:

- [Python](https://www.python.org/) as the main programming language;
- [FastAPI](https://fastapi.tiangolo.com/) for the backend;
- [SQLAlchemy 2.0](https://www.sqlalchemy.org) for the ORM
- [Postresql](https://www.postgresql.org) as database

## Contact me

- If you have any backend requests that you could benefit from;
- If you have any projects you would like me to be part of;

Add me on [LinkedIn](https://www.linkedin.com/in/adrian-babira-61021137/) or send an email to adrianbabira@gmail.com