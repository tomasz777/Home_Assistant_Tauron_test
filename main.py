import requests
import json
from datetime import datetime, timedelta
import logging

class TauronAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.base_url = "https://elicznik.tauron-dystrybucja.pl"
        self.logged_in = False
        self.prosument_ratio = 0.8  # Współczynnik oddania dla prosumentów
        
        # Konfiguracja loggera
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def login(self):
        """Logowanie do serwisu Tauron."""
        try:
            login_data = {
                "username": self.username,
                "password": self.password,
                "service": "https://elicznik.tauron-dystrybucja.pl"
            }
            
            response = self.session.post(
                f"{self.base_url}/login", 
                data=login_data
            )
            
            if response.ok:
                self.logged_in = True
                self.logger.info("Zalogowano pomyślnie do Tauron")
                return True
            else:
                self.logger.error("Błąd logowania do Tauron")
                return False
                
        except Exception as e:
            self.logger.error(f"Wystąpił błąd podczas logowania: {str(e)}")
            return False

    def get_energy_data(self, start_date=None, end_date=None):
        """Pobiera dane o zużyciu i produkcji energii z określonego okresu."""
        if not self.logged_in:
            if not self.login():
                return None

        if not start_date:
            start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # Pobieranie danych o poborze energii
            params_consumption = {
                "from": start_date,
                "to": end_date,
                "type": "Day"
            }
            
            # Pobieranie danych o produkcji energii
            params_production = {
                "from": start_date,
                "to": end_date,
                "type": "Day",
                "direction": "production"
            }
            
            response_consumption = self.session.get(
                f"{self.base_url}/api/chart/data",
                params=params_consumption
            )
            
            response_production = self.session.get(
                f"{self.base_url}/api/chart/data",
                params=params_production
            )
            
            if response_consumption.ok and response_production.ok:
                consumption_data = response_consumption.json()
                production_data = response_production.json()
                return self.process_energy_data(consumption_data, production_data)
            else:
                self.logger.error("Błąd pobierania danych o zużyciu/produkcji energii")
                return None
                
        except Exception as e:
            self.logger.error(f"Wystąpił błąd podczas pobierania danych: {str(e)}")
            return None

    def process_energy_data(self, consumption_data, production_data):
        """Przetwarza surowe dane o zużyciu i produkcji energii."""
        try:
            processed_data = {
                "total_consumption": 0,
                "total_production": 0,
                "energy_balance": 0,
                "energy_returned": 0,
                "energy_stored": 0,
                "hourly_consumption": [],
                "hourly_production": [],
                "peak_consumption_hour": None,
                "peak_consumption_value": 0,
                "peak_production_hour": None,
                "peak_production_value": 0,
                "average_consumption": 0,
                "average_production": 0
            }
            
            if not consumption_data or "values" not in consumption_data or \
               not production_data or "values" not in production_data:
                return processed_data
                
            consumption_values = consumption_data["values"]
            production_values = production_data["values"]
            
            total_consumption = 0
            total_production = 0
            
            for hour in range(len(consumption_values)):
                consumption = consumption_values[hour] if hour < len(consumption_values) else 0
                production = production_values[hour] if hour < len(production_values) else 0
                
                if consumption is not None:
                    total_consumption += consumption
                    processed_data["hourly_consumption"].append({
                        "hour": hour,
                        "value": consumption
                    })
                    
                    if consumption > processed_data["peak_consumption_value"]:
                        processed_data["peak_consumption_value"] = consumption
                        processed_data["peak_consumption_hour"] = hour
                
                if production is not None:
                    total_production += production
                    processed_data["hourly_production"].append({
                        "hour": hour,
                        "value": production
                    })
                    
                    if production > processed_data["peak_production_value"]:
                        processed_data["peak_production_value"] = production
                        processed_data["peak_production_hour"] = hour
            
            processed_data["total_consumption"] = total_consumption
            processed_data["total_production"] = total_production
            
            # Obliczenia dla prosumenta
            energy_returned = total_production * self.prosument_ratio  # Energia możliwa do odebrania
            processed_data["energy_returned"] = energy_returned
            processed_data["energy_stored"] = total_production - energy_returned  # Energia "stracona"
            processed_data["energy_balance"] = energy_returned - total_consumption  # Bilans energii
            
            if len(consumption_values) > 0:
                processed_data["average_consumption"] = total_consumption / len(consumption_values)
            if len(production_values) > 0:
                processed_data["average_production"] = total_production / len(production_values)
                
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Błąd przetwarzania danych: {str(e)}")
            return None

    def get_sensors_data(self):
        """Przygotowuje dane dla sensorów Home Assistant."""
        energy_data = self.get_energy_data()
        if not energy_data:
            return None
            
        return {
            "total_daily_consumption": {
                "state": round(energy_data["total_consumption"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Dzienne zużycie energii"
            },
            "total_daily_production": {
                "state": round(energy_data["total_production"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Dzienna produkcja energii"
            },
            "energy_balance": {
                "state": round(energy_data["energy_balance"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Bilans energii"
            },
            "energy_returned": {
                "state": round(energy_data["energy_returned"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Energia możliwa do odebrania"
            },
            "energy_stored": {
                "state": round(energy_data["energy_stored"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Energia magazynowana"
            },
            "average_hourly_consumption": {
                "state": round(energy_data["average_consumption"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Średnie godzinowe zużycie energii"
            },
            "average_hourly_production": {
                "state": round(energy_data["average_production"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Średnia godzinowa produkcja energii"
            },
            "peak_consumption": {
                "state": round(energy_data["peak_consumption_value"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Szczytowe zużycie energii"
            },
            "peak_production": {
                "state": round(energy_data["peak_production_value"], 2),
                "unit_of_measurement": "kWh",
                "friendly_name": "Szczytowa produkcja energii"
            },
            "peak_consumption_hour": {
                "state": energy_data["peak_consumption_hour"],
                "friendly_name": "Godzina szczytowego zużycia"
            },
            "peak_production_hour": {
                "state": energy_data["peak_production_hour"],
                "friendly_name": "Godzina szczytowej produkcji"
            }
        }

def main():
    # Przykład użycia
    username = "twoj_login"
    password = "twoje_haslo"
    
    tauron = TauronAPI(username, password)
    sensors_data = tauron.get_sensors_data()
    
    if sensors_data:
        print("\nDane dla Home Assistant:")
        print(json.dumps(sensors_data, indent=2, ensure_ascii=False))
    else:
        print("Nie udało się pobrać danych")

if __name__ == "__main__":
    main()