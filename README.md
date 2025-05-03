# Weather Monitoring System

## Overview
The Weather Monitoring System is a Python-based application designed to ingest, process, and monitor weather data efficiently. It leverages containerization and automation to ensure seamless deployment and scheduling of tasks.

## Features
- **Weather Data Ingestion**: Automates the retrieval of weather data using `weather_injestion.py`.
- **Containerized Deployment**: Uses Docker for consistent and portable application environments.
- **Kubernetes Integration**: Deploys and manages the application using `deployment.yaml` and `cronjob.yaml`.
- **Scheduled Tasks**: Automates periodic data ingestion with Kubernetes CronJobs.

## Key Components
- **`weather_injestion.py`**: A Python script responsible for fetching and processing weather data.
- **`Dockerfile`**: Defines the container image for the application.
- **`deployment.yaml`**: Kubernetes manifest for deploying the application.
- **`cronjob.yaml`**: Kubernetes CronJob configuration for scheduling periodic tasks.

## Installation and Deployment
1. **Build the Docker Image**:
    ```bash
    docker build -t weather-monitoring-system .
    ```

2. **Push the Image to a Container Registry** (e.g., Docker Hub):
    ```bash
    docker tag weather-monitoring-system <your-dockerhub-username>/weather-monitoring-system
    docker push <your-dockerhub-username>/weather-monitoring-system
    ```

3. **Deploy to Kubernetes**:
    - Apply the deployment manifest:
        ```bash
        kubectl apply -f deployment.yaml
        ```
    - Apply the CronJob manifest:
        ```bash
        kubectl apply -f cronjob.yaml
        ```

4. **Verify Deployment**:
    - Check the status of pods:
        ```bash
        kubectl get pods
        ```
    - Check the logs of the ingestion script:
        ```bash
        kubectl logs <pod-name>
        ```

## Usage
- The application automatically ingests weather data at scheduled intervals.
- Monitor logs and metrics via Kubernetes to ensure smooth operation.

## Contributing
We welcome contributions to improve the Weather Monitoring System. Follow the standard Git workflow to submit your changes.


## Contact
For questions or feedback, reach out:
- **Email**: sarveshparab600@gmail.com
