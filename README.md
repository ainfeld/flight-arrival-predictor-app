# MSiA423 Template Repository
Name: Amanda Infeld QA: Megan Hazlet

<!-- toc -->

- [Directory structure](#directory-structure)
- [Getting started](#getting-started)
  * [1. Set up your environment](#1-set-up-your-environment)
  * [2. Open docker desktop app and confirm it is running](#2-open-docker-desktop-app-and-confirm-it-is-running)
- [To acquire data](#to-acquire-data)
  * [1. Airplane delay data ](#1-airplane-delay-data)
  * [2. International airports data ](#2-international-airports-data)
- [Uploading raw data to S3](#uploading-raw-data-to-s3)
  * [1. Build the image to upload raw data](#1-build-the-image-to-upload-raw-data)
  * [2. Credentials for uploading raw data](#2-credentials-for-uploading-raw-data)
  * [3. Configurations for uploading raw data](#3-configurations-for-uploading-raw-data)
  * [4. Running the container to upload raw data](#4-running-the-container-to-upload-raw-data)
- [Running the model pipeline](#running-the-model-pipeline)
  * [1. Build the image to run the model pipeline](#1-build-the-image-to-run-the-model-pipeline)
  * [2. Credentials for running the model pipeline](#2-credentials-for-running-the-model-pipeline)
  * [3. Configurations for running the model pipeline](#3-configurations-for-running-the-model-pipeline)
  * [4. Running the container to build model pipeline](#4-running-the-container-to-build-model-pipeline)
- [Unit tests](#unit-tests)
  * [1. Build the image to run unit tests](#1-build-the-image-to-run-unit-tests)
  * [2. Running the container for unit tests](#2-running-the-container-for-unit-tests)
- [Database creation](#database-creation)
  * [1. Build the image to create the database](#1-build-the-image-to-create-the-database)
  * [2. Credentials for creating the database](#2-credentials-for-creating-the-database)
  * [3. Configurations for creating the database](#3-configurations-for-creating-the-database)
  * [4. Running the container to create the database](#4-running-the-container-to-create-the-database)
- [Running the app](#running-the-app)
  * [1. Build the image to run the app](#1-build-the-image-to-run-the-app)
  * [2. Credentials for running the app](#2-credentials-for-running-the-app)
  * [3. Configurations for running the app](#3-configurations-for-running-the-app)
  * [4. Running the container for the app](#4-running-the-container-for-the-app)
  * [5. Launching the app](#5-launching-the-app)
  * [6. Kill the container](#6-kill-the-container)



<!-- tocstop -->

## Project Charter 

#### Vision 
These days flying has become a fairly ubiquitous activity. However, often airline passengers find their actual arrival time differs from the estimated arrival time. To allow for better planning, this app will help flyers predict that difference and adjust expectations accordingly. 
 
#### Mission 
Users will input their date of travel, departure and arrival airports, and airline. Based on this information, the app will train a supervised learning model on the historical data to predict approximately how far off the actual arrival time is from the expected arrival time (earlier or later).
 
Data: https://www.transtats.bts.gov/DataIndex.asp
(Airline On-Time Performance Data > Reporting Carrier On-Time Performance (1987-present))
 
#### Success criteria
Machine learning criteria: As this app will be using a supervised model, the performance metrics used to evaluate the model will be F1-score. It is ready for deployment if the F1-score is above 80%. 
 
Business criteria: The success of the app from a business standpoint should be based on user engagement. The point of the app is for users to use it before they fly somewhere. The hope is the app is accurate enough that users trust it and visit it whenever they fly. Therefore, it should be considered successful if there is a high volume of user traffic and repeat users (approximately, 80% of first-time users over a year return to the app at least once within a year since their first visit).

### Planning
Initiative 1: Prepare training dataset and use to train, build, and evaluate the model 
* Epic 1: Data cleaning and exploratory data analysis
  * Story 1: Download and compile raw data set
  * Story 2: Evaluate and address missing values and outliers
  * Story 3: Evaluate and address other data anomalies 
  * Story 4: Conduct feature engineering 
  * Story 5: Select relevant variables to address business question 
* Epic 2: Develop and deploy the best model to predict expected difference in actual and estimated arrival time
  * Story 1: Test different types of supervised regression models 
  * Story 2: Calculate MSE of each model and compare across all tested models to choose the best one 

Initiative 2: Develop attributes of the app and set it up
* Epic 1: Construct data pipeline 
  * Story 1: Create an RDS DB instance through AWS
  * Story 2: Store data S3 bucket on AWS 
* Epic 2: Configure layout of user interface of the app 
  * Story 1: Create initial page of the app
  * Story 2: Create layout for user input 
  * Story 3: Create results page of the app
* Epic 3: Build Flask App 

Initiative 3: Deploy and test the app to evaluate usability and user engagement 
* Epic 1: Deploy the best model 
  * Story 1: Test configuration of the model 
* Epic 2: Build unit tests to evaluate functionality 
* Epic 3: Conduct A/B testing to evaluate different versions of the app

Backlog
1.  Initiative1.Epic1.Story1 (1 point) – PLANNED 
2.  Initiative1.Epic1.Story2 (2 points) – PLANNED
3.  Initiative1.Epic1.Story3 (1 point) – PLANNED 
4.  Initiative1.Epic1.Story4 (2 points) – PLANNED
5.  Initiative1.Epic1.Story5 (1 point) – PLANNED
6.  Initiative1.Epic2.Story1 (4 points) – PLANNED 
7.  Initiative1.Epic2.Story2 (2 points) – PLANNED

Icebox
* Initiative2.Epic1.Story1
* Initiative2.Epic1.Story2
* Initiative2.Epic2.Story1
* Initiative2.Epic2.Story2
* Initiative2.Epic2.Story3
* Initiative2.Epic3 
* Initiative3.Epic1.Story1
* Initiative3.Epic2
* Initiative3.Epic3

## Directory structure 

```
├── README.md                         <- You are here
├── app
│   ├── static/                       <- CSS, JS files that remain static
│       ├── basic.css                 <- CSS template for html pages
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│       ├── error.html                <- HTML page to display if an error occurs in the app
│       ├── index.html                <- HTML page to display as you open the app
│       ├── results.html              <- HTML page to display results of the request  
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│       ├──                           <- Yaml configuration file to store inputs for model pipeline
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder to store raw data
│   ├── raw/                          <- Data to upload to S3, will not be synced with git 
│
├── deliverables/                     <- Presentations 
│   ├── Final_presentation.pdf        <- Final presentation deck of app
│
├── model/                            <- Folder to save trained model objects (TMOs), model predictions, and/or model summaries
│
├── output/                           <- Folder to save output throughout running the model pipeline
│   ├── data_from_s3/                 <- Folder to save data downloaded from S3
│
├── src/                              <- Source data for the project 
│   ├── acquire_data.py               <- Script for downloaded data from S3 
│   ├── add_flights.py                <- Script for creating the database
│   ├── clean_data.py                 <- Script for cleaning the raw data 
│   ├── generate_features.py          <- Script for feature engineering
│   ├── helpers.py                    <- Script with useful functions used in other scripts
│   ├── load_data.py                  <- Script to load data downloaded from S3
│   ├── local_to_s3.py                <- Script for uploaded raw data stored locally into S3
│   ├── modeling.py                   <- Script for training model
│   ├── test_clean_data.py            <- Unit tests of the clean_data script 
│   ├── test_generate_features.py     <- Unit tests of the generate_features script
│   ├── test_helpers.py               <- Unit tests of the helpers script 
│   ├── test_load_data.py             <- Unit tests of the load_data script 
│   ├── test_modeling.py              <- Unit tests of the modeling script
│
├── Dockerfile                        <- Dockerfile for building image to run non app parts
├── Makefile                          <- File for organizing all parts
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```
## Getting started

### 1. Set up your environment 
Clone this repo onto your local computer: 
```bash
git clone https://github.com/MSIA/2020-msia423-Infeld.git
```

Navigate to the root of the directory: 
```bash
cd 2020-msia423-Infeld
```

### 2. Open docker desktop app and confirm it is running

The model pipeline uses a large amount of data. It may be necessary to change docker configurations to keep the docker app from automaticlly quitting when the model pipeline is run. 
  * Go to `Preferences` > `Resources` within the docker app. You have an option to increase `Memory` and `Disk image size`.

## To acquire data 
### 1. Airplane delay data 

Navigate to the following URL: 
<https://www.transtats.bts.gov/Tables.asp?DB_ID=120&DB_Name=Airline%20On-Time%20Performance%20Data&DB_Short_Name=On-Time>

Click on the `Download` button in the bottom right corner of the `Reporting Carrier On-Time Performance (1987-present)` box. Check the box for `Prezipped File`.

#### To download data for each month from January 2017 through December 2019: 
Navigate to the `Filter Year` and `Filter Period` dropdown menus in the top right of the box. For each month-year combination, click `Download`. Unzip the downloaded file, and open the unzipped folder. Copy the csv file 
`On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_<year>_<month_num>.csv` to a folder that will store only the data files needed for this app. The folder location is up to the user. The default specifications will work if the data is saved in `data/raw/`.

### 2. International airports data 
Navigate to the following URL:
```bash
https://en.wikipedia.org/wiki/List_of_international_airports_by_country#United_States
```
Copy all contents of the `United States` table into an excel document. Save the document as `International_airports.xlsx` in the same folder as the airplane delay data is stored. 

## Uploading raw data to S3

If the data to be used for the model pipeline is already stored in S3 skip to `Running the model pipeline`. 

### 1. Build the image to upload raw data

The Dockerfile for running the scripts is in the root of the repo. To build the image, run the following from this directory (the root of the repo): 
```bash
 docker build -f Dockerfile -t airplane .
```
This command builds the Docker image, with the tag `airplane`, based on the instructions in `Dockerfile` and the files existing in this directory.

### 2. Credentials for uploading raw data

To upload data to S3 you need to include your AWS credentials and specifcy which bucket in S3 you want to upload the data to. Run the lines below to export your credentials, setting the values to your specifications. Do NOT add quotes around any of the values. If this has already been done you can skip to `3. Configurations for uploading raw data`.
  ```bash
  export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY 
  export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
  export AWS_BUCKET=YOUR_AWS_BUCKET
  ```

### 3. Configurations for uploading raw data

To change configurations for acquiring data see below. If no changes are made all default values will be used. Include all changed configurations in the docker run line below: 
  * To change the location of the yaml configuration file, set `CONFIG_PATH` to the new file path. The default is `config/local/config.yml`.
  ```bash
  CONFIG_PATH=NEW_PATH
  ```
  * To change the location the raw data is stored locally to be uploaded to S3, set `RAW_FOLDER` to the new file path. The default is `data/raw/`. 
  ```bash
  RAW_FOLDER=NEW_PATH
  ```
  * To change the location in S3 where the data is uploaded to, set `S3_FOLDER` to the new file path. The default is `Data/`.
  ```bash
  S3_FOLDER=NEW_PATH
  ```

### 4. Running the container to upload raw data

Run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `upload`: 
```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_BUCKET --mount type=bind,source="$(pwd)",target=/app/ airplane upload
```

## Running the model pipeline

As the total size of all files used to train the model object used in the app is too large for docker, I have adjusted the pipeline to pull a subset of files from S3. 

### 1. Build the image to run the model pipeline

#### (1) If you have already created the image below, skip to `2. Credentials for running the model pipeline`

#### (2) If you need to rebuild the image, follow the directions below.

The Dockerfile for running the scripts is in the root of the repo. To build the image, run the following from this directory (the root of the repo): 
```bash
 docker build -f Dockerfile -t airplane .
```
This command builds the Docker image, with the tag `airplane`, based on the instructions in `Dockerfile` and the files existing in this directory.

### 2. Credentials for running the model pipeline

The model pipeline includes acquiring data from S3 through training and scoring a model. In order to acquire data from S3 you need to include your AWS credentials. Run the lines below to export your credentials, setting the values to your specifications. Do NOT add quotes around any of the values. If this has already been done you can skip to `3. Configurations for running the model pipeline`.
  ```bash
  export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY 
  export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
  ```

### 3. Configurations for running the model pipeline

To change configurations of the the model pipeline see below. If no changes are made all default values will be used. Include all changed configurations in the docker run line below: 
  * To change the location of the yaml configuration file, set `CONFIG_PATH` to the new file path. The default is `config/local/config.yml`.
  ```bash
  CONFIG_PATH=NEW_PATH
  ```
  * To change the location of the local folder to save downloaded data from S3, set `DATA_FOLDER` to the new path. The default is `output/data_from_s3/`.
  ```bash
  DATA_FOLDER=NEW_PATH
  ```
  * To change the location the raw data is saved, set `RAW_PATH` to the new file path. The default is `output/raw_data.csv`.
  ```bash
  RAW_PATH=NEW_PATH
  ```
  * To change the location the cleaned data is saved, set `CLEAN_PATH` to the new file path. The default is `output/cleaned_data.csv`.
  ```bash
  CLEAN_PATH=NEW_PATH
  ```
  * To change the location the processed data is saved, set `PROCESSED_PATH` to the new file path. The default is `output/processed_data.csv`. 
  ```bash
  PROCESSED_PATH=NEW_PATH
  ```
  * To change the location the model metrics are saved, set `METRICS_PATH` to the new file path. The default is `model/model_metrics.csv`.
  ```bash
  METRICS_PATH=NEW_PATH
  ```
  * To change the location the prediction results are saved, set `PREDICTIONS_PATH` to the new file path. The default is `model/prediction_results.csv`.
  ```bash
  PREDICTIONS_PATH=NEW_PATH
  ```
  * To change the location the trained model object is saved, set `MODEL_PATH` to the new file path. The default is `model/trained_model.csv`.
  ``` bash
  MODEL_PATH=NEW_PATH
  ```

### 4. Running the container to build model pipeline

Run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `all`: 
```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)",target=/app/ airplane all
```

## Unit tests

### 1. Build the image to run unit tests

#### (1) If you have already created the image below, skip to `2. Running the container for unit tests`

#### (2) If you need to rebuild the image, follow the directions below. 

The Dockerfile for running the scripts is in the root of the repo. To build the image, run the following from this directory (the root of the repo): 
```bash
 docker build -f Dockerfile -t airplane .
```
This command builds the Docker image, with the tag `airplane`, based on the instructions in `Dockerfile` and the files existing in this directory.

### 2. Running the container for unit tests

Run the following from this directory (the root of the repo).
```bash
docker run airplane tests
```

## Database creation 
If you have already created the database you want the app to query, skip to `Running the app`.

### 1. Build the image to create the database

#### (1) If you have already created the image below, skip to `2. Credentials for creating the database`

#### (2) If you need to rebuild the image, follow the directions below.

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run the following from this directory (the root of the repo):

```bash
docker build -f app/Dockerfile -t flight .
```
This command builds the Docker image, with the tag `flight`, based on the instructions in `app/Dockerfile` and the files existing in this directory.

### 2. Credentials for creating the database

As the total size of all files used in the app is too large for docker, I have saved the full processed data set used to create the database table queried by the app in S3. In order to acquire this data from S3 you need to include your AWS credentials. Run the lines below to export your credentials, setting the values to your specifications. Do NOT add quotes around any of the values. If this has already been done you can skip this step. 
```bash
export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY 
export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
```
You have an option of creating the database queried by the app locally or within RDS. By default, the database will be created locally and stored at `output/flights.db`.

If you want to create the table within RDS, you need to include your MYSQL credentials and specify which database you want to add the `flights` table to. Run the lines below to export your credentials, setting the values to your specifications. Do NOT add quotes around any of the values. If this has already been done you can skip to `3. Configurations for creating the database`.
```bash
export MYSQL_USER=YOUR_MYSQL_USERNAME
export MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD
export MYSQL_HOST=YOUR_MYSQL_HOSTNAME
export MYSQL_PORT=YOUR_MYSQL_PORT
export MYSQL_DATABASE=YOUR_MYSQL_DATABASE
```

### 2. Configurations for creating the database

To change configurations for creating the database see below. If no changes are made all default values will be used. Include all changed configurations in the docker run line below: 
  * To change the location the full processed data downloaded from S3 is saved locally, set `FULL_PROCESSED` to the new file path. The default is `output/processed_data_full.csv`.
  ```bash
  FULL_PROCESSED=NEW_PATH
  ```
  * To change the location of the yaml configuration file, set `CONFIG_PATH` to the new file path. The default is `config/local/config.yml`.
  ```bash
  CONFIG_PATH=NEW_PATH
  ```
  * To change the location the database is saved locally, run the line below, replacing the value for `<NEW_PATH>`.
  ```bash
  export SQLALCHEMY_DATABASE_URI=sqlite:///<NEW_PATH>
  ```

### 3. Running the container to create the database

#### (a) If creating the database locally and using the default path

Run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `full_create_db`: 
```bash 
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)",target=/app/ airplane full_create_db
```

### (b): If creating the database locally and specifying a new path 

Run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `full_create_db`: 
```bash 
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(pwd)",target=/app/ airplane full_create_db
```

### (c): Storing the table in RDS

Make sure you are on the Northwestern VPN.

Run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `full_create_db`: 
```bash
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e MYSQL_USER -e MYSQL_PASSWORD -e MYSQL_HOST -e MYSQL_PORT -e MYSQL_DATABASE --mount type=bind,source="$(pwd)",target=/app/ airplane full_create_db
```

## Running the app

### 1. Build the image to run the app

The Dockerfile for running the flask app is in the `app/` folder. To build the image, run the following from this directory (the root of the repo):

```bash
docker build -f app/Dockerfile -t flight .
```
This command builds the Docker image, with the tag `flight`, based on the instructions in `app/Dockerfile` and the files existing in this directory.

### 2. Credentials for running the app

As the total size of all files used to train the model object used in the app is too large for docker, I have saved the trained model object to be used for the app in S3. When running the app, the trained model object will automatically be downloaded to the local environment for use. In order to do this you need to include your AWS credentials. Run the lines below to export your credentials, setting the values to your specifications. Do NOT add quotes around any of the values. If this has already been done you can skip this step. 
```bash
export AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY 
export AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
```

To run the app you need to specify which database includes the `flights` table you would like the app to query. By default, the app will use the database stored locally at `output/flights.db`.

If you want to use the table stored in RDS, you will need to run the following using the specified connection string.
```bash
export SQLALCHEMY_DATABASE_URI=CONNECTION_STRING
```

### 3. Configurations for running the app
To change configurations for running the app see below. If no changes are made all default values will be used. Include all changed configurations in the docker run line below:  
  * By default the trained model object downloaded from S3 will be saved in `app/trained_model_for_app.sav`. If using the default, nothing needs to be added to the docker run line for this configuration. 
  * To change the location the trained model object will be saved locally, add the following after `docker run`, and set `TRAINED_MODEL` to the new path.
  ```bash
  -e TRAINED_MODEL=NEW_PATH
  ```
  * To change the location of where the locally stored database to be queried by the app is, run the line below, replacing the value for `<NEW_PATH>`.
  ```bash
  export SQLALCHEMY_DATABASE_URI=sqlite:///<NEW_PATH>
  ```

### 4. Running the container for the app

#### (a) If the app will be querying a locally stored database saved in the default location

If using the app for the first time, run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `full_create_db`: 
```bash 
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY --mount type=bind,source="$(pwd)",target=/app/ -p 5000:5000 --name app flight full_app
```

To use the app again without redownloading the model object run the following. Include any of the configuration changes made above in the docker run line after `run_app`
```bash
docker run -p 5000:5000 --name app flight run_app
```

### (b): If the app will be querying a locally stored database saved in a different location

If using the app for the first time, run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `full_create_db`: 
```bash 
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(pwd)",target=/app/ -p 5000:5000 --name app flight full_app
```

To use the app again without redownloading the model object run the following. Include any of the configuration changes made above in the docker run line after `run_app`
```bash
docker run -e SQLALCHEMY_DATABASE_URI  -p 5000:5000 --name app flight run_app
```

### (c): If the app will be querying the database stored in my RDS instance

Confirm you are on the Northwestern VPN

If using the app for the first time, run the following from this directory (the root of the repo). Include any of the configuration changes made above in the docker run line after `full_create_db`: 
```bash 
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI --mount type=bind,source="$(pwd)",target=/app/ -p 5000:5000 --name app flight full_app
```

To use the app again without redownloading the model object run the following. Include any of the configuration changes made above in the docker run line after `run_app`
```bash
docker run -e SQLALCHEMY_DATABASE_URI  -p 5000:5000 --name app flight run_app
```

### 5. Launching the app
You should now be able to access the app at <http://0.0.0.0:5000/> in your browser.

### 6. Kill the container 
Once finished with the app, you will need to kill the container. To do so open a new terminal window and run the following:

```bash
docker kill app
```










