import requests
import json
from datetime import datetime, timedelta
from time import sleep

class ChargingStation:


    def __init__(self, power: float):
        self.power = power # Default power of the charging station in kW
        self.charging = requests.get("http://127.0.0.1:5000/charge").json() # Charging status.
        self.discharging = requests.get("http://127.0.0.1:5000/charge").json() # Discharging status.
        self.battery_capacity = requests.get("http://127.0.0.1:5000/info").json() # Battery capacity.
        self.price_list = requests.get("http://127.0.0.1:5000/priceperhour").json() # Price list for electricity.
        self.baseload = requests.get("http://127.0.0.1:5000/baseload").json() # Baseload for the area.


    def simulation_time():
        response = requests.get("http://127.0.0.1:5000/").json()
        return response

    def total_consumption(self, baseload: list) -> float:
        consumption = 0
        for item in self.baseload:
	        # Checking if the item is a float
	        if isinstance(item, float):
	            # Adding float item to the total sum
	            consumption += item
	        else:
	            # If the item is not a float, raise an error
	            raise TypeError("Input list should only contain float items.")

        return consumption
        

    def lowest_pricing(self, area: str) -> dict:
        #lowest_price = min(self.price_list)
        slot_price = 0
        for item in self.price_list:
            if isinstance(item, float):
                slot_price = item
                print(slot_price)
                sleep(1)
            else:
                # If the item is not a float, raise an error
                raise TypeError("Input list should only contain float items.")
        
        return slot_price


    def energy_consumption(self, start_time: datetime, end_time: datetime) -> float:
        consumption = 0
        duration = end_time - start_time
        energy_consumption = 0

        for item in self.baseload:
    
            if isinstance(item, float):
                consumption = item * duration.total_seconds() / 3600
                sleep(1)              
            else:
                # If the item is not a float, raise an error
                raise TypeError("Input list should only contain float items.")

        return consumption


    def start_charging(self, battery_capacity: dict) -> float:
        
        initial_charge_level = 0
        capacity = self.battery_capacity["battery_capacity_kWh"]
        initial_charge_level = capacity * 0.2
        # Start charging at 20%.
        if initial_charge_level >= capacity:
            requests.post("http://127.0.0.1:5000/charge", data = {'charging' : 'on'})
	      
        return initial_charge_level


    def stop_charging(self):
        
        final_charge_level = 0
        capacity = self.battery_capacity["battery_capacity_kWh"]
        final_charge_level = capacity * 0.8
        # Stop charging at 80%
        if final_charge_level >= capacity:
            requests.post("http://127.0.0.1:5000/charge", data = {'charging' : 'off'})

        return final_charge_level


    def optimize_charging(self, start_time: datetime, end_time: datetime, price_list: list, energy_consumption: list) -> dict:
        

        # Calculate the duration of the optimization period
        duration = end_time - start_time

        # Calculate the number of time slots based on the duration and power of the charging station
        num_slots = int(duration.total_seconds() / (self.power * 1000))  # Convert power from kW to W

        # Calculate the time interval for each time slot
        time_interval = duration / num_slots

        # Initialize the optimized charging schedule
        charging_schedule = {}

        # Iterate over each time slot
        current_time = start_time
        for i in range(num_slots):
            # Calculate the energy consumption for the current time slot
            slot_energy_consumption = energy_consumption / num_slots

            # Check if the total energy consumption is less than 11 kW and the household consumption is at its lowest
            if slot_energy_consumption < 11 and slot_energy_consumption == min(energy_consumption / num_slots):
                # Calculate the electricity price for the current time slot
                slot_price = price_info[current_time.time().strftime("%H:%M")]

                # Add the time slot and its energy consumption to the optimized charging schedule
                charging_schedule[current_time.time().strftime("%H:%M")] = slot_energy_consumption

            # Move to the next time slot
            current_time += time_interval

        return charging_schedule


