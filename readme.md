# Apache Airflow Docker Setup

This guide provides step-by-step instructions to set up Apache Airflow in a Docker environment for local development.

## Prerequisites

- Docker installed on your machine: [Docker Installation Guide](https://docs.docker.com/get-docker/)
- Download the airflow docker-compose file in your project folder:
   ```bash
  curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

## Installation Instructions

1. **Create Default Folders:**
   ```bash
   mkdir ./dags ./plugins ./logs 

This command creates the necessary directories to store Airflow DAGs, plugins, and logs.

2. **Set User and Group Permissions:**
    ```bash
   echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

This command ensures proper user and group permissions for Airflow on macOS or Linux.

3. **Initialize Airflow Instance:**
    ```bash
   docker-compose up airflow-init

This command initializes the Airflow instance, setting up the required database and configurations.

4. **Start Airflow Services:**
    ```bash
   docker-compose up

This command starts the Airflow services, allowing you to access the Airflow UI and execute DAGs.

## Accessing Airflow UI

Once the services are up and running, you can access the Airflow UI by navigating to http://localhost:8080 in your web
browser.

## Additional Notes

Make sure to wait for the initialization process to complete before starting Airflow services.

Adjust Docker Compose configurations in the docker-compose.yml file as needed for your specific requirements.

Explore and customize the ./dags and ./plugins directories to organize your Airflow DAGs and plugins.