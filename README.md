# GOVJE Parking Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Maintainer][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

This custom integration for Home Assistant provides sensors for car park spaces in Jersey, based on data from the Government of Jersey website.

## Features

- Creates a sensor for each car park in Jersey
- Each sensor shows the number of available parking spaces
- Additional attributes for each car park showing details like type, status, and capacity information
- Diagnostic entities for 'Last Update', 'Last Scrape' and a "Refresh Data" button.
- Configurable update interval

![example][exampleimg]

## Installation

### HACS Custom Repository (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.
2. Add this repository as a custom repository in HACS:
   - Go to HACS > Integrations > Three dots in the top right > Custom repositories
   - Add `https://github.com/migz93/ha-govje-parking` with category "Integration"
3. Click "Install" on the GOV.JE Parking integration.
4. Restart Home Assistant.

### Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/migz93/ha-govje-parking).
2. Extract the contents.
3. Copy the `custom_components/govje_parking` folder to your Home Assistant's `custom_components` directory.
4. Restart Home Assistant.

## Configuration

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "GOVJE Parking"
4. Follow the configuration steps

### Options

- **Scan Interval**: How frequently to check for updates (2-120 minutes, default: 5 minutes)

## Usage

After installation, the integration will create a sensor for each car park in Jersey. The state of each sensor represents the number of available parking spaces.

### Example Automation

```yaml
automation:
  - alias: "Notify when Sand Street car park has less than 20 spaces"
    trigger:
      - platform: numeric_state
        entity_id: sensor.sand_street_parking
        below: 20
    action:
      - service: notify.mobile_app
        data:
          title: "Parking Alert"
          message: "Sand Street car park has less than 20 spaces available!"
```

## Data Source

This integration fetches data from the Government of Jersey Azure Blob Storage endpoint:
https://sojpublicdata.blob.core.windows.net/sojpublicdata/carpark-data.json

The data is provided in JSON format and includes near real-time information about car park spaces in Jersey.

## Troubleshooting

If the integration is not working as expected:

1. Check the Home Assistant logs for any error messages related to `govje_parking`
2. Verify that the Government of Jersey website is accessible
3. Try increasing the update interval if the website is slow to respond
4. If a car park's data is not available, the sensor will show `unknown` state instead of a number

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

- Parking data provided by the Government of Jersey
- Integration developed by [Migz93](https://github.com/migz93)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

***

[buymecoffee]: https://www.buymeacoffee.com/Migz93
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/migz93/ha-govje-parking.svg?style=for-the-badge
[commits]: https://github.com/migz93/ha-govje-parking/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[exampleimg]: https://raw.githubusercontent.com/migz93/ha-govje-parking/main/example.png
[license]: https://github.com/migz93/ha-govje-parking/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/custom-components/integration_blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Migz93-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/migz93/ha-govje-parking.svg?style=for-the-badge
[releases]: https://github.com/migz93/ha-govje-parking/releases
[user_profile]: https://github.com/migz93
