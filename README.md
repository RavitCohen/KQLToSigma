# KQLToSigma

This repository provides tools for converting KQL queries into Sigma rules. The project includes parsing KQL queries and generating equivalent Sigma rules.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

Run the main script and provide a string of KQL query as input:

```bash
python main.py
```

You will be prompted to enter a KQL query, and the corresponding Sigma rule will be generated and displayed.

## Project Components

- `main.py`: The main entry point for the program, handling user input and conversion.
- `KQL.py`: Parses and extracts relevant information from KQL queries.
- `SigmaRuleGenerator.py`: Generates Sigma rules based on parsed KQL queries.
- `utils/`: Contains helper functions and configurations for processing queries.

## KQL to Sigma Conversion

This tool extracts key components from a KQL query, such as table names, projected fields, and conditions, and maps them into a Sigma rule format.

### Example

**KQL Query:**
```kql
SecurityEvent | project EventID, CommandLine | where EventID == 4688
```

**Generated Sigma Rule:**
```yaml
logsource:
  product: windows
  service: security

detection:
  selection:
    EventID: 4688
    process_cmd: '*'

condition: selection
```

## License

This project is licensed under the MIT License.

## Contributors

- Shira Weiss Edri
- Ravit Cohen
- Noaa Kless

