import requests
import json
from datetime import datetime, timedelta
from time import sleep


class ChargingStation:


    def __init__(self, power: float):
        self.power = power # Default power of the charging station in kW.
        self.charging = requests.get("http://127.0.0.1:5000/charge").json() # Charging status.
        self.battery_capacity = requests.get("http://127.0.0.1:5000/info").json() # Battery capacity.
        self.price_list = requests.get("http://127.0.0.1:5000/priceperhour").json() # Price list for electricity.
        self.baseload = requests.get("http://127.0.0.1:5000/baseload").json() # Baseload for the area.


    #def simulation_time(self):
    #    response = requests.get("http://127.0.0.1:5000/info").json()
    #    print(response)
    #    return response


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
                #sleep(1)
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
                #sleep(1)              
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


    def stop_charging(self, battery_capacity: dict) -> float:
        
        final_charge_level = 0
        capacity = self.battery_capacity["battery_capacity_kWh"]
        final_charge_level = capacity * 0.8
        # Stop charging at 80%
        if final_charge_level >= capacity:
            requests.post("http://127.0.0.1:5000/charge", data = {'charging' : 'off'})

        return final_charge_level


    def start_discharge(self, battery_capacity: dict) -> float:
        
        inital_discharge_level = 0
        capacity = self.battery_capacity["battery_capacity_kWh"]
        initial_discharge_level = capacity * 0.8
        # Start discharge at 80%
        if initial_discharge_level >= capacity:
            requests.post("http://127.0.0.1:5000/discharge", data = {'discharging' : 'on'})

        return initial_discharge_level


    def stop_discharge(self, battery_capacity: dict) -> float:
        
        final_discharge_level = 0
        capacity = self.battery_capacity["battery_capacity_kWh"]
        final_discharge_level = capacity * 0.2
        # Stop discharge at 20%.
        if final_discharge_level >= capacity:
            requests.post("http://127.0.0.1:5000/discharge", data = {'discharging' : 'off'})
	      
        return final_discharge_level


    def optimize_charging(self, start_time: datetime, end_time: datetime, price_list: list, energy_consumption: list) -> dict:

        # Iterate time slots
        current_time = start_time
        for i in range(num_slots):
            # Calculate slot consumption
            slot_energy_consumption = energy_consumption / num_slots

            # Check if the total energy consumption is less than 11 kW
            if slot_energy_consumption < 11 and slot_energy_consumption == min(energy_consumption / num_slots):
                # Get the price for the current time slot
                slot_price = price_info[current_time.time().strftime("%H:%M")]

                # Add slot and consumption
                charging_schedule[current_time.time().strftime("%H:%M")] = slot_energy_consumption

            # Next slot
            current_time += time_interval

        return charging_schedule

"""
station = ChargingStation(7.4)

print("Battery Capacity:", station.battery_capacity)
print("Total Consumption:", station.total_consumption(station.baseload))
print("Lowest Pricing:", station.lowest_pricing("area3_stockholm"))
start_time = datetime.now() - timedelta(days=1)
end_time = datetime.now()
print("Energy Consumption:", station.energy_consumption(start_time, end_time))
initial_charge_level = station.start_charging(station.battery_capacity)
print("Initial Charge Level:", initial_charge_level, "= 20%")
final_charge_level = station.stop_charging(station.battery_capacity)
print("Final Charge Level:", final_charge_level, "= 80%")
start_time = datetime.now()
end_time = datetime.now() + timedelta(hours=12)
energy_consumption = station.energy_consumption(start_time, end_time)
charging_schedule = station.optimize_charging(start_time, end_time, station.price_list, energy_consumption)
print("Charging Schedule:", charging_schedule)
print("Charging:", station.charging)
print("Discharging:", station.discharging)
print("Power:", station.power)"""
