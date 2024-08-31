# Powerplant Coding Challenge

## Overview

This project provides a REST API to calculate and allocate power production to meet a given load using available power plants, prioritizing the most cost-effective options. The API supports configuration through environment variables and is managed using Poetry for dependency management.

## Project Structure

```
powerplant_challenge/ 
├── api/ 
│ └── v1/ 
│ └── init.py 
│ └── production_plan.py 
├── tests/ 
│ ├── init.py 
│ ├── test_production_plan.py 
├── .env 
├── app.py 
├── pyproject.toml 
├── poetry.lock 
└── README.md
```

## Installation

### Docker Compose Setup

1. **Build and Run the Docker Container**
    ```bash
    docker compose up
    ```
2. **Run Tests**

   ```bash
   docker compose run --rm app poetry run python -m unittest discover -s tests
   ```

## API Endpoints

### `GET /`

Returns a welcome message.

**Response:**

```json
{
  "message": "Powerplant Coding Challenge"
}
```

### `POST /api/v1/productionplan`

Calculate and allocate power production to meet a given load using available power plants.

**Request Payload:**

```json
{
  "load": 910,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "windpark1",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 150
    }
    // More power plants
  ]
}
```

**Response:**

```json
[
  {"name": "windpark1", "p": 90.0},
  {"name": "gasfiredbig1", "p": 460.0}
  // More results
]
```

**Error Response:**

```json
{
  "error": "Unable to match the exact load"
}
```

## Configuration

The application reads configuration values from the .env file. The available configuration parameters are:

* CO2_RATIO: The ratio of CO2 emissions per MWh (default: 0.3)
* CO2_COST_PER_TON: Cost of CO2 emission allowances per ton (default: 20)

## Author

Reinaldo Ramos (reiramos1989@gmail.com)
