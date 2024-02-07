# PyTest BDD Framework Boilerplate
This project contains initial setup for pytest-bdd automation for api, database and UI tests.
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
git clone git@github.com:SwellEnergy/gridamp-api-ez.git
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

### Executing Tests

#### Commandline execution
First, point your terminal to the project root path

Run the following command to execute all test cases in the test framework

- dvdrental testcases

```commandline
poetry run pytest dvdrental 
```

- countries testcases

```commandline
poetry run pytest countries 
```

- to run a specific test by tag such as 'test_case_id_1' tag in countries tests
```commandline
poetry run pytest countries -k "test_case_id_1" 
```