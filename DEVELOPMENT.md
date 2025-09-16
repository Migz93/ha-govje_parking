# GOV.JE Parking Integration Development Guide

This document provides information about developing and maintaining the GOV.JE Parking integration for Home Assistant.

## Project Structure

The integration is organized as follows:

```
custom_components/govje_parking/
├── __init__.py        # Main integration setup and coordinator
├── const.py           # Constants used throughout the integration
├── config_flow.py     # Configuration flow for setup in UI
├── manifest.json      # Integration metadata
├── sensor.py          # Sensor entity implementations
├── strings.json       # Translation strings for the config flow
└── translations/      # Localization files (if any)
```

## File Descriptions

### `__init__.py`

This file is the entry point for the integration. It contains:
- Integration setup code (`async_setup_entry` and `async_unload_entry`)
- Data coordinator implementation that fetches and parses JSON data from the GOV.JE parking Azure Blob Storage endpoint
- Platform setup for sensor entities

The coordinator is responsible for:
1. Fetching JSON data from the GOV.JE parking Azure Blob Storage endpoint
2. Parsing the JSON to extract car park names, available spaces, and additional attributes
3. Tracking both the last scrape time and the source's last update time
4. Providing the parsed data to all sensor entities

### `const.py`

Contains constants used throughout the integration:
- Domain name
- API URLs
- Default scan interval
- Attribute names
- Other configuration constants

This file centralizes all constants to make maintenance easier and ensure consistency.

### `config_flow.py`

Implements the configuration flow for the integration:
- Defines the ConfigFlow class for initial setup
- Implements the OptionsFlowHandler for changing settings after setup
- Handles validation of user input

### `manifest.json`

Defines metadata for the integration:
- Domain name
- Name displayed in Home Assistant
- Documentation URLs
- Dependencies
- Requirements
- Version number

**Important**: When making changes to the integration, always increment the version number in this file.

### `sensor.py`

Implements sensor entities for the integration:
- Implements the `JerseyParkingSensor` class
- Sets up sensor entities with the async_setup_entry function
- Creates a sensor for each car park with available spaces as the state

Each sensor entity extracts specific data from the parsed HTML and presents it as a Home Assistant entity.

### `strings.json`

Contains translation strings for the configuration flow UI:
- Setup step descriptions
- Field labels
- Error messages

## Version Management

### Version Numbering

The integration follows semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features, non-breaking
- PATCH: Bug fixes and minor improvements

### Updating Versions

**Important**: When making any changes to the integration, you must increment the version number in:

1. `custom_components/govje_parking/manifest.json` - The `version` field
2. `hacs.json` - The `hacs` field

Example:
```json
// manifest.json
{
  "version": "0.1.1"
}

// hacs.json
{
  "hacs": "1.0.0"
}
```

Failing to update these version numbers will prevent Home Assistant from recognizing the updated integration when installed via HACS.

## Development Workflow

1. Make code changes
2. Test locally
3. Increment version numbers in both `manifest.json` and `hacs.json`
4. Commit changes
5. Create a release (if publishing)

## Entity Naming Conventions

- All sensor entities use the naming pattern: "[Car Park Name] Parking"
- Entity unique IDs use the "govje_parking_" prefix followed by the car park name (lowercase with spaces replaced by underscores)

### JSON Parsing Strategy

The integration parses JSON data from the GOV.JE parking Azure Blob Storage endpoint. The parsing strategy follows these steps:

1. Fetch JSON data from the Azure Blob Storage endpoint
2. Parse the JSON response
3. Extract the timestamp from `carparkData.Timestamp`
4. Extract car park data from `carparkData.Jersey.carpark` array
5. For each car park:
   - Extract the name from the `name` field
   - Extract the available spaces from the `spaces` field
   - Extract all additional fields (code, type, status, etc.)
   - Check if the car park is open using the `carparkOpen` field

### Car Park Detection

The integration dynamically detects car parks from the JSON data. This approach allows the integration to automatically add new car parks as they become available in the data source without requiring code changes.

The integration creates a sensor entity for each car park found in the JSON data, using the name provided in the data.

### Parsing Challenges

The GOV.JE parking data may present challenges for parsing:
- The car park data structure might change over time
- New car parks might be added or existing ones removed

To handle these challenges, the integration uses:
- Dynamic car park detection to automatically adapt to changes
- Robust error handling for JSON parsing
- Fallback mechanisms when parsing fails

## Data Structure

The integration stores car park data in the following structure:

```python
{
    "Car Park Name": {
        "free_spaces": 100,  # Number of available spaces
        "code": "CARPARK_CODE",  # Car park code
        "type": "Short stay",  # Car park type
        "status": "good",  # Status information
        "carparkOpen": True,  # Whether the car park is open
        "carparkInformation": "Information about the car park",  # Additional information
        "numberOfUnusableSpaces": 10,  # Number of unusable spaces
        "numberOfSpacesConsideredLow": 20,  # Threshold for low spaces
        # Additional fields from the JSON data
    },
    # Additional car parks...
}
```

The coordinator also tracks:
- `last_scrape_time`: When data was last fetched (formatted as YYYY-MM-DD HH:MM:SS)
- `latest_timestamp`: The timestamp from the data source

## Testing

To test changes:
1. Install the integration in a development Home Assistant instance
2. Verify that all entities appear with correct names
3. Check that data is updated correctly
4. Verify that the update interval works as expected

## Troubleshooting

Common issues:
- JSON parsing failures: Check the Azure Blob Storage endpoint response and update the parsing logic
- Entity naming issues: Check the unique_id generation in entity classes
- Data not updating: Check the coordinator update interval and website response
- Missing entities: Verify the entity setup in async_setup_entry functions

### Debugging JSON Parsing

If the integration is not correctly parsing the car park data:

1. Check the Home Assistant logs for error messages related to JSON parsing
2. Verify that the Azure Blob Storage endpoint is returning valid JSON data
3. Update the parsing logic in `__init__.py` if the JSON structure changes

## Future Improvements

Potential improvements for future versions:
- Add support for total spaces and percentage full if this data becomes available
- Implement more robust timestamp validation strategies
- Add support for additional parking-related data
- Create a map card integration to show car park locations
