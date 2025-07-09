# Data Handling Program

A Python project for generating, storing, and visualizing sample data with Oracle database integration.

## Features

- **Data Generation**: Creates synthetic persons, pets, and occupations using Faker
- **Multiple Export Formats**: CSV, JSON, XLSX
- **Oracle Database Integration**: Stores data in Oracle database tables
- **Data Visualization**: Creates charts and graphs from the generated data

## Setup

### Prerequisites

- Python 3.11+
- Oracle Instant Client (for database connectivity)
- Oracle database access

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd data_handling_program
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with:
```bash
ORACLE_HOST=your-oracle-host
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=your-service-name
ORACLE_USER=your-username
ORACLE_PASSWORD=your-password
ORACLE_IC_PATH=~/path/to/instantclient
```

## Usage

### Generate and Export Data
```bash
python generator.py
```

### Store Data in Oracle Database
```bash
python oracle_handling.py
```

### Create Visualizations
```bash
python visualization.py
```

## Project Structure

- `generator.py` - Data generation and export functionality
- `oracle_handling.py` - Oracle database operations
- `visualization.py` - Data visualization and plotting
- `.github/workflows/ci.yml` - GitHub Actions CI/CD pipeline

## Security Notes

- Never commit your `.env` file
- Use repository secrets for CI/CD environments
- All database credentials are loaded from environment variables

## License

This project is for educational/demonstration purposes. 