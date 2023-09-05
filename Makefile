CONFIG_PATH=config/local/config.yml
${CONFIG_PATH}:
	touch ${CONFIG_PATH}

RAW_FOLDER=data/raw/
${RAW_FOLDER}:
	touch ${RAW_FOLDER}

S3_FOLDER=Data/
${S3_FOLDER}:
	touch ${S3_FOLDER}

DATA_FOLDER=output/data_from_s3/
${DATA_FOLDER}:
	touch ${DATA_FOLDER}

RAW_PATH=output/raw_data.csv
${RAW_PATH}:
	touch ${RAW_PATH}

CLEAN_PATH=output/cleaned_data.csv
${CLEAN_PATH}:
	touch ${CLEAN_PATH}

PROCESSED_PATH=output/processed_data.csv
${PROCESSED_PATH}:
	touch ${PROCESSED_PATH}

PREDICTIONS_PATH=model/prediction_results.csv
${PREDICTIONS_PATH}:
	touch ${PREDICTIONS_PATH}

METRICS_PATH=model/model_metrics.csv
${METRICS_PATH}:
	touch ${METRICS_PATH}

MODEL_PATH=model/trained_model.sav
${MODEL_PATH}:
	touch ${MODEL_PATH}

APP_MODEL=app/trained_model_for_app.sav
${APP_MODEL}:
	touch ${APP_MODEL}

FULL_PROCESSED=output/processed_data_full.csv
${FULL_PROCESSED}:
	touch ${FULL_PROCESSED}

# Upload data from local to s3
upload:
	python3 run.py local_to_s3 --config=${CONFIG_PATH} --input_path=${RAW_FOLDER} --output_path=${S3_FOLDER}

# Running model pipeline
acquire:
	python3 run.py acquire --config=${CONFIG_PATH} --input_path='Data/' --output_path=${DATA_FOLDER}

${RAW_PATH}: ${CONFIG_PATH}
	python3 run.py load --config=${CONFIG_PATH} --input_path=${DATA_FOLDER} --output_path=${RAW_PATH}

load: ${RAW_PATH}

${CLEAN_PATH}: ${CONFIG_PATH} ${RAW_PATH}
	python3 run.py clean --config=${CONFIG_PATH} --input_path=${RAW_PATH} --output_path=${CLEAN_PATH}
clean: ${CLEAN_PATH}

${PROCESSED_PATH}: ${CONFIG_PATH} ${CLEAN_PATH}
	python3 run.py features --config=${CONFIG_PATH} --input_path=${CLEAN_PATH} --dir_path=${DATA_FOLDER} --output_path=${PROCESSED_PATH}
features: ${PROCESSED_PATH}

modeling: ${CONFIG_PATH} ${PROCESSED_PATH}
	python3 run.py modeling --config=${CONFIG_PATH} --input_path=${PROCESSED_PATH} --output_path=${METRICS_PATH} --model_path=${MODEL_PATH} --predictions_path=${PREDICTIONS_PATH}

all: acquire load clean features modeling

# Creating the database
${FULL_PROCESSED}:
	python3 run.py download_processed --input_path='processed_data_full.csv' --output_path=${FULL_PROCESSED}

create_db: ${CONFIG_PATH}  ${FULL_PROCESSED}
	python3 run.py create_db --config=${CONFIG_PATH}  --input_path=${FULL_PROCESSED}

full_create_db: ${FULL_PROCESSED} create_db

# Running tests
helper_tests:
	python3 run.py helper_tests

load_data_tests:
	python3 run.py load_data_tests

clean_data_tests:
	python3 run.py clean_data_tests

generate_features_test:
	python3 run.py generate_features_tests

modeling_test:
	python3 run.py modeling_tests

tests: helper_tests load_data_tests clean_data_tests generate_features_test modeling_test 

# Running the app
download_model: 
	python3 run.py download_model --input_path='trained_model_for_app.sav'

run_app:
	python3 app.py

full_app: download_model run_app




