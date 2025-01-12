# SimpleFIN Financial Data Retrieval Tool

This project contains a set of Python scripts designed to retrieve and transform financial transaction data from a SimpleFIN-enabled account. The goal is to make it easier for users to access and format their bank data for personal use, while adhering to SimpleFIN's API structure and requirements.

## Features

- **SimpleFIN API Integration**:
  - Use a SimpleFIN setup token to claim an access URL, username, and password for API calls.
  - Query all financial account and transaction data linked to the SimpleFIN account.
- **Date-Restricted Queries**:
  - Fetch transactions based on a specified date range: Daily, Monthly, or All.
  - Avoid importing duplicate or old transactions.
- **Data Transformation**:
  - Clean and standardize transaction data.
  - Remove currency symbols and format the output to meet application requirements.
- **Export Options**:
  - Output data to CSV files for easy integration with other tools or apps.

## Installation

### Prerequisites

- Python 3.8 or later
- `pip` package manager
- Internet connection to access the SimpleFIN API

### Required Libraries

Install the necessary Python packages using the following command:

```bash
pip install requests pandas python-dotenv
```

## Setup

### 1. Environment Variables

Create a `.env` file in the project directory and populate it with the following placeholders:

```plaintext
SIMPLEFIN_SETUP_TOKEN='your-simplefin-token-here' # Fill this in before running `convert-setup-token.py`.
SIMPLEFIN_URL='https://beta-bridge.simplefin.org/simplefin/accounts' # Provided after running `convert-setup-token.py`.
SIMPLEFIN_USERNAME='your-simplefin-user-here' # Provided after running `convert-setup-token.py`.
SIMPLEFIN_PASSWORD='your-simplefin-pass-here' # Provided after running `convert-setup-token.py`.
JSON_OUTPUT_FILE='get_response' # Filename for debugging JSON responses (without extension).
ACCOUNTS_OUTPUT_FILE='accounts' # Filename for accounts CSV output (without extension).
TRANSACTIONS_OUTPUT_FILE='transactions' # Filename for transactions CSV output (without extension).
DEBUG_MODE=False # Set to True to enable detailed debugging output.
```

### 2. Obtain Setup Token

To use the tool, obtain a SimpleFIN setup token from your financial institution or service provider.

### 3. Claim Access

Run the `convert-setup-token.py` script to decode the setup token and claim access credentials:

```bash
python convert-setup-token.py
```

This will output the access URL, username, and password, which you should populate in the `.env` file.

## Usage

Run the `retrieve-data.py` script to fetch and process your financial data:

```bash
python retrieve-data.py [mode]
```

### Modes

- `Daily`: Fetch transactions from the last day.
- `Monthly`: Fetch transactions from the start of the current month.
- `All`: Fetch all available transactions starting from January 1, 2000. Note: This may be restricted to time limitations that SimpleFIN has in place.

Example:

```bash
python retrieve-data.py Monthly
```

### Output

- **Accounts CSV**: Account details, including balance and currency, will be exported to `accounts_<date>.csv`.
- **Transactions CSV**: Cleaned and formatted transaction data will be exported to `transactions_<date>.csv`.

## File Overview

### `.env`
Contains environment variables for API credentials, file names, and debug settings.

### `convert-setup-token.py`
- Decodes the SimpleFIN setup token (Base64) and retrieves the access URL, username, and password.
- Outputs credentials needed for API calls.

### `retrieve-data.py`
- Fetches account and transaction data using the SimpleFIN API.
- Processes, cleans, and exports the data based on the selected mode.

## Debugging

Enable debugging by setting `DEBUG_MODE=True` in the `.env` file. This will:
- Save the raw API response JSON to a file for analysis.

## Contributing

Feel free to fork the repository and submit pull requests. Suggestions for improving functionality, efficiency, or documentation are always welcome.

## License

This project is licensed under the MIT License.

## Acknowledgments

This tool was developed to simplify financial data retrieval and transformation using SimpleFIN. Special thanks to the SimpleFIN team for providing detailed API documentation.
