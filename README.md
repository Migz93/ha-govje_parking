# GOVJE Parking Integration for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Maintainer][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

This custom integration for Home Assistant provides sensors for car park spaces in Jersey, based on data from the Government of Jersey website.

## Features

- Creates a sensor for each open car park in Jersey
- Each sensor shows the number of available parking spaces
- Additional attributes for each car park showing details like type, status, and capacity information
- Diagnostic entities for Last API Update and Last Scrape timestamps (disabled by default)
- Refresh Data button to trigger an immediate update
- Configurable update interval (2–120 minutes)

![example][exampleimg]

## Installation

### HACS Custom Repository (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance.
2. Add this repository as a custom repository in HACS:
   - Go to HACS > Integrations > Three dots in the top right > Custom repositories
   - Add `https://github.com/Migz93/ha-govje_parking` with category "Integration"
3. Click "Install" on the GOVJE Parking integration.
4. Restart Home Assistant.

### Manual Installation

1. Download the latest release from the [GitHub repository](https://github.com/Migz93/ha-govje_parking).
2. Extract the contents.
3. Copy the `custom_components/govje_parking` folder to your Home Assistant's `custom_components` directory.
4. Restart Home Assistant.

## Configuration

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "GOVJE Parking"
4. Optionally give it a custom name, then click Submit — no credentials required

### Options

After setup, click **Configure** to adjust:

- **Update Interval**: How frequently to check for updates (2–120 minutes, default: 5 minutes)

## Usage

After installation the integration creates a sensor for each open car park in Jersey. The state of each sensor is the number of available parking spaces. Each sensor also exposes attributes with additional details (car park type, status, unusable spaces, etc.).

### Platforms

| Platform | Description                                                                                                                       |
| -------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `sensor` | One sensor per open car park showing free spaces; plus optional diagnostic sensors for last scrape and last API update timestamps |
| `button` | Refresh Data — triggers an immediate data update                                                                                  |

### Services

| Service                     | Description                                              |
| --------------------------- | -------------------------------------------------------- |
| `govje_parking.reload_data` | Force an immediate refresh of car park data from the API |

### Example Automation

```yaml
automation:
  - alias: "Notify when Sand Street car park has less than 20 spaces"
    trigger:
      - platform: numeric_state
        entity_id: sensor.govje_parking_sand_street
        below: 20
    action:
      - service: notify.mobile_app
        data:
          title: "Parking Alert"
          message: "Sand Street car park has less than 20 spaces available!"
```

> **Note:** Entity IDs follow the pattern `sensor.{integration_name}_{car_park_name}`. Find the exact entity ID for each car park in Settings → Devices & Services → GOVJE Parking → your device.

## Data Source

This integration fetches data from the Government of Jersey Azure Blob Storage endpoint:
`https://sojpublicdata.blob.core.windows.net/sojpublicdata/carpark-data.json`

The data is provided in JSON format and includes near real-time information about car park spaces in Jersey. Only car parks marked as open are included.

## Troubleshooting

If the integration is not working as expected:

1. Check the Home Assistant logs for any error messages related to `govje_parking`
2. Verify that the Government of Jersey data endpoint is accessible
3. Try reducing the update interval if data appears stale
4. If a car park's data is not available, the sensor will show `unknown` state
5. Download diagnostics from Settings → Devices & Services → GOVJE Parking → three dots → Download diagnostics

### Enable Debug Logging

Add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.govje_parking: debug
```

## Contributing

Contributions are welcome! Please read the [Contribution guidelines](CONTRIBUTING.md) before opening a pull request.

---

## 🤖 AI-Assisted Development

> **ℹ️ Transparency Notice**
>
> This integration was developed with assistance from AI coding agents (Claude Code and others). While the codebase follows Home Assistant Core standards and Silver Quality Scale patterns, AI-generated code may not be reviewed or tested to the same extent as manually written code.
>
> If you encounter any issues, please [open an issue](https://github.com/Migz93/ha-govje_parking/issues) on GitHub.

---

## Credits

- Parking data provided by the Government of Jersey
- Integration developed by [Migz93](https://github.com/Migz93)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

[buymecoffee]: https://www.buymeacoffee.com/Migz93
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/Migz93/ha-govje_parking.svg?style=for-the-badge
[commits]: https://github.com/Migz93/ha-govje_parking/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[exampleimg]: https://raw.githubusercontent.com/Migz93/ha-govje_parking/main/docs/images/example.png
[license]: https://github.com/Migz93/ha-govje_parking/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/Migz93/ha-govje_parking.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Migz93-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Migz93/ha-govje_parking.svg?style=for-the-badge
[releases]: https://github.com/Migz93/ha-govje_parking/releases
[user_profile]: https://github.com/Migz93
