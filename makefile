install-local:
	curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
	mkdir -p dags plugins logs
	@echo "AIRFLOW_UID=$$(id -u)" > .env
	@echo "AIRFLOW_GID=0" >> .env
	docker-compose up airflow-init
	docker-compose up