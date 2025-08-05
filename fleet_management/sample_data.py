"""
Sample data creation for Fleet Management app
Run this in the Frappe console to create sample data
"""

import frappe
from frappe.utils import today, nowdate, add_days
import random

def create_sample_data():
    """Create sample data for fleet management"""

    # Create sample drivers
    drivers_data = [
        {"name": "Ahmed Al-Salem", "phone": "+966501234567", "license": "SAU1234567890"},
        {"name": "Mohammed Al-Rashid", "phone": "+966509876543", "license": "SAU0987654321"},
        {"name": "Khalid Al-Otaibi", "phone": "+966551234567", "license": "SAU1122334455"},
        {"name": "Abdullah Al-Fahad", "phone": "+966559876543", "license": "SAU5566778899"},
        {"name": "Salman Al-Dosari", "phone": "+966501357924", "license": "SAU9988776655"}
    ]

    created_drivers = []
    for driver_data in drivers_data:
        driver = frappe.get_doc({
            "doctype": "Driver",
            "naming_series": "DRV-.YYYY.-",
            "driver_name": driver_data["name"],
            "phone": driver_data["phone"],
            "license_number": driver_data["license"],
            "status": "Active",
            "hire_date": add_days(today(), -random.randint(30, 365)),
            "license_expiry": add_days(today(), random.randint(90, 730))
        })
        driver.insert()
        created_drivers.append(driver)
        print(f"Created driver: {driver.driver_name}")

    # Create sample vehicles
    vehicles_data = [
        {"name": "Toyota Camry 2022", "plate": "RYD123", "make": "Toyota", "model": "Camry", "year": 2022},
        {"name": "Honda Accord 2021", "plate": "JED456", "make": "Honda", "model": "Accord", "year": 2021},
        {"name": "Nissan Altima 2023", "plate": "DAM789", "make": "Nissan", "model": "Altima", "year": 2023},
        {"name": "Hyundai Sonata 2022", "plate": "MED101", "make": "Hyundai", "model": "Sonata", "year": 2022},
        {"name": "Kia Optima 2021", "plate": "TAB202", "make": "Kia", "model": "Optima", "year": 2021}
    ]

    created_vehicles = []
    for i, vehicle_data in enumerate(vehicles_data):
        vehicle = frappe.get_doc({
            "doctype": "Vehicle",
            "naming_series": "VEH-.YYYY.-",
            "vehicle_name": vehicle_data["name"],
            "license_plate": vehicle_data["plate"],
            "make": vehicle_data["make"],
            "model": vehicle_data["model"],
            "year": vehicle_data["year"],
            "vehicle_type": "Car",
            "fuel_type": "Petrol",
            "status": "Active",
            "current_driver": created_drivers[i].name if i < len(created_drivers) else None,
            "assigned_date": today(),
            "odometer_reading": random.randint(5000, 50000),
            "color": random.choice(["White", "Black", "Silver", "Blue", "Red"])
        })
        vehicle.insert()
        created_vehicles.append(vehicle)
        print(f"Created vehicle: {vehicle.vehicle_name}")

    # Create sample vehicle updates
    for vehicle in created_vehicles[:3]:  # Only for first 3 vehicles
        for days_ago in range(1, 8):  # Last 7 days
            update = frappe.get_doc({
                "doctype": "Vehicle Update",
                "naming_series": "VUP-.YYYY.-",
                "vehicle": vehicle.name,
                "driver": vehicle.current_driver,
                "update_date": add_days(today(), -days_ago),
                "update_type": random.choice(["Daily Check", "Pre-Trip Inspection", "Post-Trip Inspection"]),
                "description": f"Daily update for {vehicle.vehicle_name}. All systems normal.",
                "fuel_level": random.choice(["Full", "3/4", "1/2", "1/4"]),
                "odometer_reading": vehicle.odometer_reading + random.randint(50, 200) * days_ago,
                "status": "Submitted"
            })
            update.insert()

    print("Sample vehicle updates created")

    # Create sample fuel logs
    for vehicle in created_vehicles:
        for weeks_ago in range(1, 5):  # Last 4 weeks
            fuel_log = frappe.get_doc({
                "doctype": "Fuel Log",
                "naming_series": "FL-.YYYY.-",
                "vehicle": vehicle.name,
                "driver": vehicle.current_driver,
                "fuel_date": add_days(today(), -weeks_ago * 7),
                "odometer_reading": vehicle.odometer_reading + random.randint(200, 400) * weeks_ago,
                "fuel_type": "Petrol",
                "quantity": random.randint(30, 60),
                "total_cost": random.randint(150, 300),
                "fuel_station": random.choice(["ARAMCO", "ALDREES", "ALDREES CO-OP", "PETROMIN"]),
                "payment_method": "Company Account",
                "tank_full": 1
            })
            fuel_log.insert()

    print("Sample fuel logs created")

    # Create sample maintenance records
    for vehicle in created_vehicles[:2]:  # Only for first 2 vehicles
        maintenance = frappe.get_doc({
            "doctype": "Vehicle Maintenance",
            "naming_series": "VM-.YYYY.-",
            "vehicle": vehicle.name,
            "maintenance_type": "Preventive",
            "description": f"Regular service for {vehicle.vehicle_name}",
            "priority": "Medium",
            "status": random.choice(["Scheduled", "Completed"]),
            "requested_date": add_days(today(), -random.randint(1, 30)),
            "scheduled_date": add_days(today(), random.randint(1, 14)),
            "estimated_cost": random.randint(500, 1500),
            "service_provider": "Al-Jazirah Automotive Services"
        })
        maintenance.insert()

    print("Sample maintenance records created")
    print("Sample data creation completed!")

# Run this function to create sample data
if __name__ == "__main__":
    create_sample_data()
