# ML Prediction, Docker-X-Fastapi 
#### (incomplete)

This repository contains a FastAPI application for predicting car insurance fraud, packaged in a Docker container. A continuation from previous project, Vehicle Insurance Fraud Claim Prediction (Beta).

## Automated Deployment with GitHub Actions

This repository is set up to automatically build and deploy the Docker image using GitHub Actions. Whenever code is pushed to the `main` branch, the following steps are executed:

1. **Checkout the repository code**.
2. **Set up Docker Buildx**.
3. **Login to Docker Hub**.
4. **Build and push the Docker image** to Docker Hub.
5. **Run the Docker container**.

## Setting Up Secrets

To set up the necessary secrets for the GitHub Actions workflow:

1. Go to your repository on GitHub.
2. Navigate to `Settings` > `Secrets and variables` > `Actions`.
3. Add the following secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username.
   - `DOCKER_PASSWORD`: Your Docker Hub password.

## Accessing the API

After the Docker container is deployed, the FastAPI application will be accessible at `http://127.0.0.1:8000/docs`. You can use any API client (such as [Postman](https://www.postman.com/) or `curl`) to interact with the API.

### Example Request

- **Endpoint**: `POST http://127.0.0.1:8000/vehicle_insurance_fraud(Beta)/predict`
- **Request Body**:
  ```json
  {
    "AccidentArea": 1,
    "AgentType": 0,
    "Fault": 1,
    "MaritalStatus": 2,
    "PoliceReportFiled": 1,
    "Sex": 1,
    "VehicleCategory": 1,
    "WitnessPresent": 1
  }
