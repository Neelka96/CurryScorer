# CurryScorer: Data Visualization & ETL Project
`Project 3`  
`EdX(2U) & UT Data Analytics and Visualization Bootcamp`  
`Cohort UTA-VIRT-DATA-PT-11-2024-U-LOLC`  


## Overview

**CurryScorer** is designed to extract, transform, and visualize data for a specified domain (e.g., sports analytics, financial trends). The project encapsulates the ETL process and the backend for an interactive dashboard in a unified framework. By simply running the main script, the ETL pipeline is instantiated and executed, and the backend is set up to serve visualizations via a Flask web interface.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Installation & Setup](#installation--setup)
3. [Technology Requirements](#technology-requirements)
    - [Operating Systems](#operating-systems)
    - [Python Dependencies](#python-dependencies)
4. [Directory Structure & File Breakdown](#directory-structure--file-breakdown)
5. [Deployment Details](#deployment-details)
6. [Database & ORM Layer](#database--orm-layer)
7. [Usage](#usage)
8. [Limitations](#limitations)
9. [Credits & Citations](#credits--citations)

---

## Project Overview

CurryScorer processes, analyzes, and visualizes data for [insert domain-specific purpose, e.g., sports analytics or financial trends]. The project is structured to allow a seamless data flow:
- **ETL Pipeline**: Instantiated and executed directly from the main script.
- **Visualization Engine**: Generates interactive and static charts.
- **Unified Execution**: A single command (`python app.py`) launches the entire process, making it simple to run in both development and production environments.


*Feel free to delete the database that comes with the cloned repo! Just be sure to include your own `NYC_OPEN_KEY` in the `.env` file!*

> [!WARNING]  
> For local execution, please make sure to include your own `.env` file in the root/ with the lines:  
>   `ENV = 'development'` and  
>   `NYC_OPEN_KEY = <yourKeyHere>`  
> Additionally, please check to make sure the configuration paths are valid for your system.

---

## Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/CurryScorer.git
   cd CurryScorer
   ```

2. **Set Up Virtual Environment (Recommended)**

   - **Using venv (Python built-in):**

     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

   - **Using Conda:**

     ```bash
     conda create --name curryscorer_env python=3.12
     conda activate curryscorer_env
     ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   Activate your virtual environment and start the project with:
   ```bash
   python app.py
   ```
   The main script instantiates the ETL pipeline and calls `.run()`, handling the rest of the process automatically.

---

## Technology Requirements

### Operating Systems

- **Supported OS**: Windows 10 or later, macOS Catalina or later, and modern Linux distributions.
- **Minimum Hardware**:
  - CPU: Dual-core processor or higher
  - Memory: 4 GB RAM (8 GB recommended)
  - Disk Space: 500 MB free (project files and dependencies)

### Python Dependencies

- **Python Version**: 3.8 or higher (tested on Python 3.12)
- **Key Libraries**:
  - `pandas`
  - `requests`
  - `Flask`
  - `Flask_CORS`
  - `SQLAlchemy`
  - `Tenacity`
  - Other dependencies as specified in `requirements.txt`

---

## Directory Structure & File Breakdown

Below is the tree diagram of the project’s structure along with a brief explanation of each component:

```plaintext
CurryScorer/
│
├── Core/
│   ├── resources/
│   │   ├── census_population.csv   # (REQUIRED FOR NOW) Population data file read for reading in.
│   │   ├── courier_dev.sqlite      # (Optional) SQLite Database that is used for this project, created if not present.
│   │   └── fastfood.csv            # (Optional) List of fast food restaurants, created if not present.
│   │
│   ├── backend/                    # Module for creating backend of Dashboard
│   │   ├── templates/              # Flask Templates for deploying HTML
│   │   │   └── home.html           # Only file here currently - creates pretty home route
│   │   ├── init.py                 # Top level of backend - Flask App lives here
│   │   └── backend.py              # Backend Helper
│   │
│   ├── etl/
│   │   ├── extract/                # MODULE - Extracting data from source files.
│   │   │   ├── init.py             # MODULE - Holds select dataset retrieval methods
│   │   │   └── extract.py          # Extract Helper
│   │   ├── init.py                 # BLANK - For library creation
│   │   ├── transform.py            # MODULE - Cleaning and normalizing data.
│   │   └── load.py                 # MODULE - Loading data into a usable format.
│   │
│   ├── init.py                     # MODULE - Pipeline Class creation. Manages ETL process.
│   ├── database.py                 # MODULE - Holds database schema and custom session management
│   └── log_config.py               # MODULE - Configured logger function for threading through project
│
├── frontend/
│   └── js/                         # Javascript for import to index.html
│       └── logic.js
├── index.html                      # Index html 
├── app.py                          # Main script to instantiate and run the pipeline.
├── .env                            # Important: required for environmental variables
├── requirements.txt                # List of Python dependencies.
└── README.md                       # This README file.
```

### Explanation of File & Directory Connections

- **Core/resources/:**
Contains essential data files. The required census_population.csv is used for data ingestion, while optional files like courier_dev.sqlite and fastfood.csv support extended functionalities. For a different experience, feel free to delete the SQLite DataBase that is included in the `Core/resources` of this repository when cloned! If that's the case the `.env` API `NYC_OPEN_KEY` is even more important to be included in the root of this cloned repo when running as it won't be able to proceed without it.

- **Core/backend/:**
Houses the Flask backend components. The templates/ directory contains HTML templates (currently just home.html), while init.py and backend.py set up and manage the backend service.  

- **Core/etl/:**
Encapsulates the ETL process:  

  - **extract/:** Retrieves raw data using methods defined in init.py and helper functions in extract.py.  

  - **transform.py**: Cleans and normalizes the extracted data.  

  - **load.py:** Loads the transformed data into the appropriate format (e.g., databases or CSV files).  

  - The parent **init.py** in the **Core** directory initializes the Pipeline Class that orchestrates the ETL process.  

- **Core/database.py:**
  Contains the database schema definitions and manages custom session handling for database operations.  

- **Core/log_config.py:**
Provides a configured logging function to ensure consistent logging throughout the project, useful for both debugging and production monitoring.  

- **frontend/:**
Contains the user-facing components. Currently only JavaScript. The files in js/ support interactive elements.  

- **index.html:**
The main HTML file for the frontend interface, included in the root for deployment to Github pages.  

- **app.py:**
Serves as the unified entry point. When run, it instantiates the ETL pipeline (by creating an instance of the Pipeline Class defined in Core/init.py) and calls its .run() method. This script handles both local execution and production deployment seamlessly.  

- **.env:**
Lists required environmental variables for runtime to succeed. Required variables are `ENV = development` for local execution and a `NYC_OPEN_KEY = <yourKeyHere>`

- **requirements.txt:**
Lists all Python dependencies to ensure consistent setup across environments.  

---  

## Deployment Details
**Backend Deployment:**  
The backend is deployed live to Azure at https://curryscorer.azurewebsites.net. The Flask app hosted on Azure serves the dashboard using the components in Core/backend/.

**Frontend Deployment:**  
The frontend is hosted via GitHub Pages, with index.html and associated JavaScript files in the frontend/ directory providing a clean and responsive user interface.

**Database Sharing & Concurrency Control:**  
To ensure that all instances of the web app use a single instance of the database, a file share in an Azure Storage Account is linked to the web app. This integration guarantees a centralized courier_dev.sqlite database even when the web app scales across multiple instances. Future enhancements will include implementing a locking mechanism to prevent multiple simultaneous updates, ensuring data integrity during concurrent operations.  

---  


## Database & ORM Layer
CurryScorer leverages SQLAlchemy 2.0 ORM to manage all interactions with the database. Key measures include:

- Schema Definition and Session Management:
The database schema is defined in Core/database.py and is built exclusively using SQLAlchemy 2.0 ORM. This module also includes custom session management to ensure that all database interactions—whether for building the database or executing queries—are conducted within the ORM’s context.

- Querying and Transactional Consistency:
All queries and data modifications are handled via SQLAlchemy’s ORM layer, ensuring that transactions are managed with the latest best practices for reliability and performance. This design promotes clean and maintainable code, reducing the risk of SQL injection and other common database pitfalls.

- Contextual Session Handling:
SQLAlchemy’s context managers are used to guarantee that sessions are properly closed after operations, ensuring that the database remains consistent and that resource usage is optimized across both development and production environments.


---

## Usage

**Running the Pipeline**:  
  With your virtual environment activated, your `.env` file setup, and configuration confirmed, simply execute:
  ```bash
  python app.py
  ```
  This command:

- Instantiates the ETL pipeline and executes the data extraction, transformation, and loading steps.

- Sets up the Flask backend to serve the dashboard, making it accessible via the live Azure URL.

- Ensures that both the backend and frontend deployments are in sync with the central database file share.

---

## Limitations

- **Manual Data Dependency:**  
  + The Extraction phase currently doesn't have a siphon for live census data, so instead manually extraction was leveraged to build the necessary CSV file.
  + Cuisine constants are currently hard coded in configuration, later updates should include a path for extracting what are actually considered to be "ethnic cuisines".

- **Data Volume:**  
  The ETL pipeline is optimized for moderate-sized datasets. Extremely large datasets might require further optimization or integration with distributed processing tools.

- **Coupled ETL & Flask App:**
  The Flask App is currently dependent on the insurance provided by the ETL Pipeline's instantiation. Later updates will de-couple and schedule ETL as a separate task.

- **Manual Configuration:**  
  Some settings (e.g., file paths for raw and processed data) may need manual adjustments depending on your environment.

- **Error Handling:**  
  While the pipeline is designed to be robust, additional logging and error handling might be necessary for production-level deployments.

- **Python Dependency Upgrades:**  
  Future upgrades to dependencies should be tested thoroughly to ensure compatibility across modules.

- **Concurrency Control:**  
Currently, a file share is used to centralize the database among multiple instances. A more advanced locking mechanism is planned to prevent concurrent update issues.

---

## Credits & Citations

- **Project Contributors**:  
  - [Neel Agarwal](https://github.com/neelka96)
  - [Manny Guevara](https://github.com/MannyHub24)
  - [Rob LaPreze](https://github.com/rlapreze2)
  - [Samora Machel](https://github.com/samora90)

- **Key References & Documentation**:  
  - [New York City Open Data](https://opendata.cityofnewyork.us/)
    + [DOHMH DataSet](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j/about_data)
    + [FastFood Restaurants](https://data.cityofnewyork.us/Health/DOHMH-MenuStat-Historical-/qgc5-ecnb/about_data)
    + [Socrata/SODA Querying](https://dev.socrata.com/docs/queries/)
  - [Current Python Docs](https://docs.python.org/3/contents.html)
  - [pandas Documentation](https://pandas.pydata.org/docs/)
  - [Flask Documentation](https://flask.palletsprojects.com/)
  - [SQL Alchemy Documentation](https://docs.sqlalchemy.org/en/20/)
  - [Tenacity Documentation](https://tenacity.readthedocs.io/en/latest/)
  - README template and guidance inspired by previous projects and ChatGPT assistance.

- **Special Thanks**:  
  Appreciation to the UT Data Analytics and Visualization Bootcamp for the foundational materials and the project rubric that shaped the design of CurryScorer.

