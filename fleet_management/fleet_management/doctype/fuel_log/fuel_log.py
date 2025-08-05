# Copyright (c) 2025, a Aalshehri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FuelLog(Document):
	def validate(self):
		"""Validate fuel log data before saving"""
		# Calculate price per liter if not provided
		if self.total_cost and self.quantity and not self.price_per_liter:
			self.price_per_liter = self.total_cost / self.quantity

		# Calculate total cost if not provided
		if not self.total_cost and self.price_per_liter and self.quantity:
			self.total_cost = self.price_per_liter * self.quantity

		# Update vehicle odometer if provided and greater than current
		if self.odometer_reading and self.vehicle:
			vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
			if not vehicle_doc.odometer_reading or self.odometer_reading > vehicle_doc.odometer_reading:
				vehicle_doc.odometer_reading = self.odometer_reading
				vehicle_doc.save()

		# Calculate fuel efficiency
		self.calculate_fuel_efficiency()

	def calculate_fuel_efficiency(self):
		"""Calculate fuel efficiency based on previous fuel log"""
		if not self.tank_full:
			return

		# Get previous fuel log for the same vehicle
		previous_log = frappe.get_all("Fuel Log",
			filters={
				"vehicle": self.vehicle,
				"fuel_date": ["<", self.fuel_date],
				"tank_full": 1
			},
			fields=["odometer_reading", "quantity"],
			order_by="fuel_date desc",
			limit=1
		)

		if previous_log:
			prev_odometer = previous_log[0].get("odometer_reading", 0)
			if prev_odometer and self.odometer_reading > prev_odometer:
				self.distance_covered = self.odometer_reading - prev_odometer
				if self.quantity > 0:
					self.fuel_efficiency = self.distance_covered / self.quantity

	def on_submit(self):
		"""Update vehicle fuel statistics when fuel log is submitted"""
		self.update_vehicle_fuel_stats()

	def update_vehicle_fuel_stats(self):
		"""Update vehicle fuel statistics"""
		# Calculate average fuel efficiency for the vehicle
		avg_efficiency = frappe.db.sql("""
			SELECT AVG(fuel_efficiency) as avg_efficiency
			FROM `tabFuel Log`
			WHERE vehicle = %s AND fuel_efficiency > 0
		""", (self.vehicle,))

		if avg_efficiency and avg_efficiency[0][0]:
			vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
			# Could add a custom field for average fuel efficiency
			# vehicle_doc.average_fuel_efficiency = avg_efficiency[0][0]
			# vehicle_doc.save()
