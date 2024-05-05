import requests
from datetime import datetime, timedelta


class ChargingStationClient:

    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def get_simulation_time(self):
        response = self.get_request("info")
        print("Simulation Time Response:", response)
        if response and "sim_time" in response:
            return response["sim_time"]
        return None

    def get_price_information(self, area):
        response = self.get_request("priceperhour")
        print("Price Information Response:", response)
        return response

    def get_energy_consumption(self, start_time: datetime, end_time: datetime):
        response = self.get_request("baseload")
        print("Energy Consumption Response:", response)
        return response

    def start_charging(self):
        response = self.post_request("charge", {"charging": "on"})
        print("Start Charging Response:", response)
        return response

    def stop_charging(self):
        response = self.post_request("charge", {"charging": "off"})
        print("Stop Charging Response:", response)
        return response

    def get_request(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error accessing {endpoint}: {e}")
            return None

    def post_request(self, endpoint, data):
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error accessing {endpoint}: {e}")
            return None


if __name__ == "__main__":
    client = ChargingStationClient()

    # Get simulation time
    simulation_time = client.get_simulation_time()
    print("Simulation Time:", simulation_time)

    # Get price information
    price_info = client.get_price_information("area3_stockholm")
    print("Price Information:", price_info)

    # Get energy consumption
    start_time = datetime.now() - timedelta(days=1)
    end_time = datetime.now()
    energy_consumption = client.get_energy_consumption(start_time, end_time)
    print("Energy Consumption:", energy_consumption)

    # Start charging
    print("Starting Charging...")
    charging_response = client.start_charging()
    print("Charging Response:", charging_response)

    # Stop charging
    print("Stopping Charging...")
    stopping_response = client.stop_charging()
    print("Stopping Response:", stopping_response)
