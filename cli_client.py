import requests
from ChargingStation import ChargingStation as charging_station
from datetime import datetime, timedelta

station = charging_station(7.4)


def menu():
    # UI.
    print("""
    1. Simulation time
    2. Total consumption
    3. Lowest pricing
    4. Energy consumption
    5. Initial charge level
    6. Final charge level
    7. Charging schedule
    8. Charging on/off
    9. Discharge on/off
    10. Exit
    """)
    choice = input("Enter your choice: ")
    return choice


if __name__ == "__main__":
    # Keep program running. 
    while True:
        choice = menu()
        if choice == "1":
            print("simulation_time", station.simulation_time())
        elif choice == "2":
            print("Total consumption:", station.total_consumption(station.baseload))
        elif choice == "3":
            print("Lowest price:", station.lowest_pricing("area3_stockholm"))
        elif choice == "4":
            start_time = datetime.now() - timedelta(days=1)
            end_time = datetime.now()
            energy_consumption = station.energy_consumption(start_time, end_time)
            print("Energy consumption:", energy_consumption, "kWh")
        elif choice == "5":
            initial_charge_level = station.start_charging(station.battery_capacity)
            print("Initial charge level:", initial_charge_level, "= 20%")
        elif choice == "6":
            final_charge_level = station.stop_charging()
            print("Final charge level:", final_charge_level, "= 80%")
        elif choice == "7":
            start_time = datetime.now()
            end_time = datetime.now() + timedelta(hours=12)
            energy_consumption = station.energy_consumption(start_time, end_time)
            charging_schedule = station.optimize_charging(start_time, end_time, station.price_list, energy_consumption)
            print("Charging schedule:", charging_schedule)
        elif choice == "8":
            print("Enter on/off and punch return: ")
            charging = input()
            data = {"charging" : str(charging)}
            response = requests.post("http://127.0.0.1:5000/charge", data = data)
            print(response)
        elif choice == "9":
            print("Enter on/off and punch return: ")
            discharge = input()
            data = {"discharge" : str(discharge)}
            response = requests.post("http://127.0.0.1:5000/discharge", data = data)
            print(response)
        elif choice == "10":

            break
        else:
            print("Invalid choice")

# Path: ChargingStation.py