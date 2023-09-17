Serverless Airflow Project
==========================

Overview
--------
This project provides a serverless solution to execute Airflow DAGs. It uses Flask to expose an endpoint where you can POST your DAG code and its configuration. The server then executes the DAG tasks and returns the logs.


Features
--------
- Run Airflow DAGs without a dedicated Airflow instance.
- Accepts both DAG code and YAML configuration via HTTP POST request.
- Logs are returned after the execution is complete.


Installation
------------
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install the required packages: `pip install -r requirements.txt`


Usage
-----
1. Start the Flask application: `flask run`
2. POST your DAG code and configuration as JSON to the endpoint:
    ```
    curl -X POST http://127.0.0.1:5000/ -d '{"dag_code": "<Your DAG Code>", "config_yml": "<Your YAML Config>"}'
    ```
3. The logs will be returned in the HTTP response.


Contributing
------------
If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.


License
-------
MIT

