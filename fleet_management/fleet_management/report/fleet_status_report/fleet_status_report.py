# Copyright (c) 2025, a Aalshehri and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Vehicle"),
			"fieldname": "vehicle_name",
			"fieldtype": "Link",
			"options": "Vehicle",
			"width": 200
		},
		{
			"label": _("License Plate"),
			"fieldname": "license_plate",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Make/Model"),
			"fieldname": "make_model",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Current Driver"),
			"fieldname": "current_driver",
			"fieldtype": "Link",
			"options": "Driver",
			"width": 150
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Odometer Reading"),
			"fieldname": "odometer_reading",
			"fieldtype": "Float",
			"precision": 2,
			"width": 130
		},
		{
			"label": _("Last Update"),
			"fieldname": "last_update",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": _("Next Maintenance Due"),
			"fieldname": "next_maintenance",
			"fieldtype": "Date",
			"width": 130
		}
	]


def get_data(filters):
	conditions = []
	values = []

	if filters.get("status"):
		conditions.append("v.status = %s")
		values.append(filters.get("status"))

	if filters.get("vehicle_type"):
		conditions.append("v.vehicle_type = %s")
		values.append(filters.get("vehicle_type"))

	where_clause = ""
	if conditions:
		where_clause = "WHERE " + " AND ".join(conditions)

	query = f"""
		SELECT
			v.name as vehicle_name,
			v.license_plate,
			CONCAT(v.make, ' ', v.model) as make_model,
			v.current_driver,
			v.status,
			v.odometer_reading,
			(SELECT MAX(update_date) FROM `tabVehicle Update`
			 WHERE vehicle = v.name) as last_update,
			(SELECT MIN(scheduled_date) FROM `tabVehicle Maintenance`
			 WHERE vehicle = v.name AND status = 'Scheduled') as next_maintenance
		FROM `tabVehicle` v
		{where_clause}
		ORDER BY v.vehicle_name
	"""

	return frappe.db.sql(query, values, as_dict=1)
