# TIA Synthetic Data Generator
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or newer
- Access to a running MySQL database server

### Setup Instructions

Follow these steps to set up your local development environment.

#### 1. Clone the Repository

First, clone the project to your local machine:
```bash
git clone https://github.com/TIA-PARTNERS-GROUP/TIA-SYNTHETIC-DATA-GENERATION/ && cd TIA-SYNTHETIC-DATA-GENERATION
```

#### 2. Create a virtual environment named 'venv'
```bash
python -m venv venv
```

## Activate the virtual environment
### On Windows:
```bash
venv\Scripts\activate
```
### On macOS and Linux:
```bash
source venv/bin/activate
```
## Now, install all the necessary packages using pip:
```bash
pip install -r requirements.txt
```
## Configure the Application
The application is configured using the config.toml file.

If it doesn't exist, create a file named config.toml in the root of the project.

Copy the following content into it and adjust the values to match your environment.

```toml
# config.toml

# The number of base entities (like users) to generate.
# Other entities will be scaled based on this number.
data_generation_size = 50

# Your full database connection string.
# Format: "mysql+mysqlconnector://<user>:<password>@<host>:<port>/<database_name>"
database_connection_string = "mysql+mysqlconnector://root:your_password@localhost:3306/your_db"
```

## Usage
Once the setup is complete, you can run the seeder script from the root directory of the project.

The script will:

* Connect to the database.

* Drop all existing tables to ensure a clean slate.

* Recreate the tables based on your SQLAlchemy models.

Populate the tables with freshly generated data.
```bash
python main.py
```

## Makefile (Optional)
For convenience, you can use a Makefile to automate the setup and execution steps.

### Makefile Commands
```bash
make setup
```
```bash
make run
```
```bash
make clean
```
