# PyTest BDD Boilerplate

This project contains initial setup for pytest-bdd automation for api, database and UI tests.

## Python Installation (Windows)

1. Download and install the required Python version (^3.10)
2. Install pip

```shell 
python3 get-pip.py
```

3. Open the command prompt in the directory you want to create the virtual environment (usually the project folder you
   are working on) and create virtual environment for the specific version of python

```shell
 virtualenv -p {path_to_python_exe_file} {your_venv_name}
```

4. Run the flg command to activate the virtual environment

```shell
\path\to\env\Scripts\activate
```

### Framework Installation

1. Clone the repo from git using the following command

```commandline
git clone git@github.com:centricconsulting/pytestbdd-boilerplate.git
```

2. Install poetry
```
pip install poetry
```
   
3. Run the following command from your project root directory to install packages

```commandline
poetry install
```

## Database Testing Setup

The database used in the this project is a public sample dvdrental postgres database.
The sample database is obtained
from https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/

### Setting up test database on your local

The sample database .tar file is available in `dvdrental` folder.

1. Download and install pgAdmin from https://www.pgadmin.org/download/
#### To connect to PostgreSQL database server
2. Open pgAdmin and right-click the Servers node and select Register > Server… menu to create a server
3. Enter the server name such as Local, and click the Connection tab
4. Enter the host (localhost if the server is on your local) and password for the postgres user and click the Save button
5. Click on the Servers node to expand the server. By default, PostgreSQL has a database named postgres
#### To load dvdrental database
6. Right-click the Databases and select the Create > Database… menu option.
7. Enter the database name dvdrental and click the Save button.
   You’ll see the new empty database created under the Databases node.
8. Right-click on the dvdrental database and choose the Restore… menu item to restore the database from the
   dvdrental.tar database file available in the project.
9. Enter the path to the sample database tar file and click the Restore button.
10. Open the dvdrental database from the object browser panel, you will find tables in the public schema and other
   database objects.

For more info refer to https://www.postgresqltutorial.com/postgresql-getting-started/load-postgresql-sample-database/

## API Testing Setup

Api tests are written for a publicly available rest api site https://restcountries.com/#endpoints-name

## UI Testing Setup

UI tests are written for a publicly available sample website https://www.saucedemo.com/

Before you run UI tests in `demosite` project folder, 
- download chrome driver compatible to your Chrome browser from https://googlechromelabs.github.io/chrome-for-testing/ 
- unzip the file and save the driver application file in `lib/web_drivers`

## ElasticSearch Basic Setup (Optional)

To integrate elasticsearch reporting and analytics, we have to first setup elasticsearch.

- NOTE: after setting up elasticsearch, you need to set `turn_on` value to `True` in elasticsearch settings
  in `config/setup.yml` file

### Create API Key

1. Create a free elasticsearch trial account if you don't have one yet
2. Login to your account and go to Stack Management
3. Click API Keys menu item under 'Security'
4. Click on 'Create API key' button to create an api key (Type: Personal API key) and copy and save the key

### Create Index

5. Under 'Data' section click on Index Management
6. In Index Management click 'Create index'
7. Give it a name such as `pytestbdd-qa-logs`  and click save
8. Click on the newly created index
9. In `Add data to this index` section you will find your elasticsearch host URL.

- Copy that url including and up to the port number and save it.

10. Replace `es_index` variable in {project_name}/tests/conftest.py:

- for `countries` project `pytestbdd-qa-logs-countries`
- for `dvdrental` project `pytestbdd-qa-logs-dvdrental`

### Create Dataview

11. Under 'Kibana' section, click on 'Data Views'
12. Click on 'Create data view' button
13. Select an Index pattern such as `pytestbdd-qa-*` that matches with the index name you created
14. Click on 'Save data view to Kibana' button.

### To Connect To Elasticsearch

16. In your project go to `config/setup.yml` file
17. Modify the corresponding elasticsearch hosts (from step 9) and api_key (from step 4) values - the api key should be
    encrypted (use `lib/encryption.py` to encrypt)

## To Create Kibana Dashboard (Optional)

Follow the detailed instructions
in https://www.elastic.co/guide/en/kibana/current/create-a-dashboard-of-panels-with-web-server-data.html

## To Encrypt Passwords and Keys

1. Generate encryption key using Fernet Key Generator

```key = Fernet.generate_key()```

2. Save in proj_secrets.py file under your project root.
(NOTE: proj_secrets.py should not be checked in to git. (add it in .gitignore))

```keys = {'{project_name}}': {'{qa_environment}': {encryption_key}```

where:

- project_name in this example `countries`, `dvdrental` or `demosite`
- qa_environment is QA1 or QA2
- encryption_key is key generated in step 1

3. Create an encrypted value for a particular password/api_key (`str` in this example) using the key you created in step
   2

```encrypted_str = encrypt(str, key)```

4. Replace the password/api_key in `config/setup.yml` with the encrypted string (`encrypted_str` from step 2)

## Executing Tests

#### Commandline execution

First, point your terminal to the project root path.

Run the following command to execute project test cases.

- dvdrental testcases on test environment QA1

```commandline
poetry run pytest dvdrental --env QA1 
```

- countries testcases

```commandline
poetry run pytest countries 
```

- to run a specific test by tag such as 'test_case_id_1' tag in countries tests

```commandline
poetry run pytest countries -k "test_case_id_1" 
```

## To Debug Tests

1. Type in `breakpoint()` where you would like to debug.
2. Run the commandline with --pdb switch. For example to debug `test_case_id_1` test case

```commandline
poetry run pytest countries -k "test_case_id_1" --pdb
```

NOTE: Don't forget to remove `breakpoint()` after you complete your debugging.

## To Create Unique testcase ids for Scenarios

Test case id generation utility assigns unique test case ids incrementally for scenarios, scenario outlines and
examples.

_For scenarios and scenario outlines_ (test_case_id_1, test_case_id_2, ...).

_For scenario outline examples_ (test_case_id_2_1, test_case_id_2_2, ...)

```
poetry run pytest countries -k "assign_unique_test_id"
```

## Logs and Reports

NOTE: `project_name` is either `countries`, `demosite` or `dvdrental`

### Logs

Log levels can be set to the required value (such as DEBUG, INFO, ERROR, CRITICAL) in `config/setup.yml`

Logs are automatically generated and saved in `logs/{project_name}/` folder.

### HTML Reports

Logs are automatically generated and saved in `{project_name}/reports/` folder
