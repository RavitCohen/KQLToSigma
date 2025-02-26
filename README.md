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
```**KQL Query:**
events_all
| where data_source_type_id in (456, 460, 501, 502, 507, 440, 347) and (_eventSource =~ 'sts.amazonaws.com' and _eventName =~ 'AssumeRoleWithSAML') or (_eventSource =~ 'iam.amazonaws.com' and _eventName =~ 'UpdateSAMLProvider')
```

**Generated Sigma Rule:**
```yaml
logsource:
  product: aws
  service: cloudtrail

detection:
  selection_1:
    eventName:'AssumeRoleWithSAML'
    eventSource:'sts.amazonaws.com' 
  selection_2:
    eventName:'UpdateSAMLProvider'
    eventSource:'iam.amazonaws.com'
  condition: 1 of selection_*
```


## License

This project is licensed under the MIT License.

## Contributors

- Shira Weiss Edri
- Ravit Cohen
- Noaa Kless

