# PyTest BDD Boilerplate
This project contains initial setup for pytest-bdd automation for api, database and UI(coming soon) tests.
## Python installation
1. Download and install the required Python version
2. Install pip 
```shell 
python3 get-pip.py
```
3. open the command prompt in the directory you want to create the virtual environment (usually the project folder you are working on) and create virtual environment for the specific version of python
```shell
 virtualenv -p {path_to_python_exe_file} {venv_name}
```
4. Run the flg command to activate the virtual environment
```shell
\path\to\env\Scripts\activate
```

### Framework installation

1. Clone the repo from git using the following command

```commandline
git clone git@github.com:ccezana/pytestbdd-boilerplate.git
```

2. Run the following command from your project root directory

```commandline
poetry install
```
## Database testing setup
The database used in the test is a sample dvdrental postgres database. 
The sample database is obtained from https://www.postgresqltutorial.com/postgresql-getting-started/postgresql-sample-database/
### Setting up test database on your local
The sample database .tar file is available in the dvdrental folder. 

1. Download and install pgAdmin from https://www.pgadmin.org/download/
2. launch the pgAdmin tool and connect to the PostgreSQL server
3. right-click the Databases and select the Create > Database… menu option.
4. enter the database name dvdrental and click the Save button. 
You’ll see the new empty database created under the Databases node.
5. right-click on the dvdrental database and choose the Restore… menu item to restore the database from the dvdrental.tar database file available in the project.
6. enter the path to the sample database tar file and click the Restore button.
7. open the dvdrental database from the object browser panel, you will find tables in the public schema and other database objects.

For more info refer to https://www.postgresqltutorial.com/postgresql-getting-started/load-postgresql-sample-database/

## API Testing setup
Api tests are written for a publicly available rest api site https://restcountries.com/#endpoints-name


## ElasticSearch basic setup (Optional)
To integrate elasticsearch reporting and analytics, we have to first setup elasticsearch.
- NOTE: after setting up elasticsearch, you need to set `turn_on` value to `True` in elasticsearch settings in `config/setup.yml` file
### Create API key
1. Create a free elasticsearch trial account if you don't have one yet
2. Login to your account and go to Stack Management
3. Click API Keys menu item under 'Security'
4. Click on 'Create API key' button to create an api key (Type: Personal API key) and copy and save the key
### Create index
6. Under 'Data' section click on Index Management 
7. In Index Management click 'Create index'
8. Give it a name such as `pytestbdd-qa-logs`  and click save
9. Click on the newly created index
10. In `Add data to this index` section you will find the elasticsearch host URL. 
- Copy that url including and up to the port number and save it.
9. Replace `es_index` variable in {project_name}/tests/conftest.py:
- for `countries` project `pytestbdd-qa-logs-countries`
- for `dvdrental` project `pytestbdd-qa-logs-dvdrental`
### Create Dataview
10. Under 'Kibana' section, click on 'Data Views'
11. Click on 'Create data view' button
12. Select an Index pattern such as `pytestbdd-qa-*` that matches with the index name you created
13. Click on 'Save data view to Kibana' button.
14. Copy the url upto the port number and that will be your Elasticsearch hosts url.
### Connecting to Elasticsearch
15. In your project go to `config/setup.yml` file 
16. Modify the corresponding elasticsearch hosts (from step 14) and api_key (from step 4) values - the api key should be encrypted (use `lib/encryption.py` to encrypt)

## Create Kibana dashboard (Optional)
Follow the detailed steps in https://www.elastic.co/guide/en/kibana/current/create-a-dashboard-of-panels-with-web-server-data.html

## Encrypting passwords and keys
1. Generate encryption key using Fernet Key Generator 

```key = Fernet.generate_key()```

2. Save in proj_secrets.py file under your project root. 

NOTE: This file should not be checked in to git. (add it in .gitignore)
```keys = {'{project_name}}': {'{qa_environment}': {encryption_key}```

where:
- project_name in this example `countries` or `dvdrental`
- qa_environment is QA1 or QA2
- encryption_key is key generated in step 1

2. Create an encrypted value for a particular password/api_key (`str` in this example) using the key you created in step 1
 
```encrypted_str = encrypt(str, key)```

3. Replace the password/api_key in `config/setup.yml` with the encrypted string (`encrypted_str` from step 2) 

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
## Debugging tests
1. Type in `breakpoint()` where you would like to debug.
2. Run the commandline with --pdb switch. For example to debug `test_case_id_1` test case

```commandline
poetry run pytest countries -k "test_case_id_1" --pdb
```
NOTE: Don't forget to remove `breakpoint()` after you complete your debugging.

## Create unique test ids for scenarios
Test case id generation utility assigns unique test case ids incrementally for scenarios, scenario outlines and examples.

_For scenarios and scenario outlines_ (test_case_id_1, test_case_id_2, ...).

_For scenario outline examples_ (test_case_id_2_1, test_case_id_2_2, ...)

```
poetry run pytest countries -k "assign_test_case_id"
```
## Logs and Reports
NOTE: `project_name` is either `countries` or `dvdrental`
### Logs
Log levels can be set to the required value (such as DEBUG, INFO, ERROR, CRITICAL) in `config/setup.yml`

Logs are automatically generated and saved in `logs/{project_name}/` folder.

### HTML Reports
Logs are automatically generated and saved in `{project_name}/reports/` folder
