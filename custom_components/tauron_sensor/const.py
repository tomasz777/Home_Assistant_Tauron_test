"""Stałe dla integracji Tauron."""
DOMAIN = "tauron_sensor"

# Identyfikatory sensorów
SENSOR_TYPES = {
    "total_daily_consumption": {
        "name": "Dzienne zużycie energii",
        "unit": "kWh",
        "icon": "mdi:flash",
    },
    "total_daily_production": {
        "name": "Dzienna produkcja energii",
        "unit": "kWh",
        "icon": "mdi:solar-power",
    },
    "energy_balance": {
        "name": "Bilans energii",
        "unit": "kWh",
        "icon": "mdi:scale-balance",
    },
    "energy_returned": {
        "name": "Energia możliwa do odebrania",
        "unit": "kWh",
        "icon": "mdi:battery-positive",
    },
    "energy_stored": {
        "name": "Energia magazynowana",
        "unit": "kWh",
        "icon": "mdi:battery",
    },
    "average_hourly_consumption": {
        "name": "Średnie godzinowe zużycie energii",
        "unit": "kWh",
        "icon": "mdi:chart-line",
    },
    "average_hourly_production": {
        "name": "Średnia godzinowa produkcja energii",
        "unit": "kWh",
        "icon": "mdi:chart-line",
    },
    "peak_consumption": {
        "name": "Szczytowe zużycie energii",
        "unit": "kWh",
        "icon": "mdi:flash-alert",
    },
    "peak_production": {
        "name": "Szczytowa produkcja energii",
        "unit": "kWh",
        "icon": "mdi:solar-power-variant",
    },
    "peak_consumption_hour": {
        "name": "Godzina szczytowego zużycia",
        "unit": None,
        "icon": "mdi:clock",
    },
    "peak_production_hour": {
        "name": "Godzina szczytowej produkcji",
        "unit": None,
        "icon": "mdi:clock",
    },
}