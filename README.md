### Fleet Management

A comprehensive fleet management system built for ERPNext/Frappe Framework.

### Features

#### Core Management
- **Vehicle Management**: Track vehicle details, status, make, model, year, etc.
- **Driver Management**: Manage driver information, licenses, contact details
- **Vehicle Updates**: Allow drivers to submit updates with photos and videos
- **Maintenance Tracking**: Schedule and track vehicle maintenance
- **Fuel Logging**: Track fuel consumption and efficiency

#### Key Capabilities
- **Driver Updates with Media**: Drivers can submit daily updates, inspections, and incident reports with photo and video attachments
- **Maintenance Scheduling**: Automated maintenance request creation based on driver reports
- **Fuel Efficiency Tracking**: Automatic calculation of fuel efficiency based on fuel logs
- **Fleet Status Dashboard**: Real-time view of fleet status and statistics
- **Mobile-Friendly**: Optimized for use on mobile devices by drivers

### Installation

1. Install the app:
```bash
bench get-app https://github.com/your-repo/fleet_management
```

2. Install on site:
```bash
bench --site your-site install-app fleet_management
```

3. Run migration:
```bash
bench --site your-site migrate
```

### Usage

#### For Fleet Managers
1. Navigate to Fleet Management workspace
2. Create Vehicles and Drivers
3. Assign drivers to vehicles
4. Monitor updates and maintenance requests
5. View reports and analytics

#### For Drivers
1. Access Fleet Management > Vehicle Update
2. Submit daily updates with photos/videos
3. Report maintenance issues
4. Log fuel consumption
5. Update vehicle status

### DocTypes

1. **Vehicle**: Core vehicle information
2. **Driver**: Driver details and license information
3. **Vehicle Update**: Driver updates with media support
4. **Vehicle Maintenance**: Maintenance scheduling and tracking
5. **Fuel Log**: Fuel consumption tracking

### Reports

- Fleet Status Report
- Maintenance Report
- Fuel Consumption Report

### Roles

- **Fleet Manager**: Full access to all fleet management features
- **Driver**: Limited access for updates and viewing assigned vehicles

### License

MIT

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app fleet_management
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/fleet_management
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
