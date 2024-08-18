```
  _     ___                       
 | |   / _ \                      
 | | _| (_) |   ___ __ _ _ __ ___ 
 | |/ /\__, |  / __/ _` | '__/ _ \
 |   <   / /  | (_| (_| | | |  __/
 |_|\_\ /_/    \___\__,_|_|  \___|
```                               
# **ETL Project**

### **Overview**

This ETL (Extract, Transform, Load) project is designed to automate the process of extracting data from various sources, transforming it into a required format, and loading it into a target data warehouse for analysis and reporting. The project is orchestrated using Apache Airflow and containerized with Docker.

### **Table of Contents**

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

### **Project Structure**

```
.
├── dags/
│   ├── etl_dag.py             # Airflow DAG definition
│   └── etl/                   # Core ETL logic
│       ├── config.py          # Configuration management
│       ├── extractors/        # Data extraction modules
│       ├── transformers/      # Data transformation modules
│       ├── repositories/      # Data store/repository modules
│       ├── loaders/           # Data loading modules
│       ├── logging_config.py  # Logging configuration
|       └── error_reporting.py # Reporting configuration
├── tests/                     # Unit and integration tests
├── Dockerfile.airflow         # Dockerfile for Airflow
├── docker-compose.yml         # Docker Compose setup
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

### **Prerequisites**

Before you begin, ensure you have met the following requirements:

- **Docker**: Install Docker and Docker Compose on your system.
- **Python 3.8+**: Ensure Python is installed if you plan to run the scripts locally.
- **Apache Airflow**: Airflow will be set up automatically using Docker Compose.

### **Installation**

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/nmmanas/k9_care_etl.git
   cd k9_care_etl
   ```

2. **Set Environment Variables:**
   Edit the appropriate environment file with the following details:

   Run in docker:
   ```
   ENV="docker"
   DB_URI="postgresql://postgres:password@postgres:5432/k9_care"
   ```

   Run locally:
   ```
   ENV="dev"
   DB_URI="postgresql://postgres:password@localhost:5432/k9_care"
   ```

3. **Set Up the Environment:**

   Ensure Docker is running, then execute the following command to set up the environment:

   ```bash
   docker-compose up -d
   ```

   This will build and start the Airflow containers, setting up the ETL environment.

4. **Running Locally:**

   If running locally, install the required Python packages:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   Run the orchestrator script:

   ```bash
   python main_etl.py
   ```

### **Usage**

1. **Access Airflow:**

   After starting the containers, you can access the Airflow web interface at `http://localhost:8080`. The default login credentials are `admin` for both the username and password.

   Create new airflow user:                                  
  ```
  docker-compose exec airflow airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
  ```


2. **Trigger the ETL Process:**

   In the Airflow web interface, navigate to the `etl_dag` and trigger it manually or set it up for scheduled runs.

3. **Monitor the ETL Process:**

   Airflow provides a visual representation of the DAG and task execution status, allowing you to monitor the ETL process in real-time.

### **Configuration**

- **Configuration Files:**
  
  The configuration for the ETL process is managed in `dags/etl/config.py`. Update this file to modify settings such as data source URLs, database connection strings, and other environment-specific variables.

- **Environment Variables:**

  You can override configuration settings using environment variables. Set them in the `docker-compose.yml` or in your environment.

### **Testing**

1. **Run Unit Tests:**

   Unit tests are available for extractors, transformers, and loaders. Run them using:

   ```bash
   pytest tests/
   ```

2. **Integration Testing:**

   Integration tests are included to validate the entire ETL pipeline. Ensure Docker is running, then execute the tests.

### **Deployment**

1. **Production Deployment:**

   For production, the ETL pipeline can be deployed using a cloud-based Docker orchestration tool such as Kubernetes. Ensure the environment variables are set appropriately for the production environment.

2. **Scaling:**

   The system is designed to scale horizontally by adding more workers to the Airflow cluster. Update the `docker-compose.yml` to increase the number of worker instances.

```json
facts = [
   {
	   “fact”: “interesting fact!”,
	   “Created_date”: "2023-12-12T15:44:51.527Z"
   },
   …
]
```
