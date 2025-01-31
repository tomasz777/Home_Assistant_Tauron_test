"""Platforma sensorów dla integracji Tauron."""
from datetime import timedelta
import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import Throttle

from .const import DOMAIN, SENSOR_TYPES
from .tauron_api import TauronAPI

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=15)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Skonfiguruj sensory Tauron na podstawie wpisu konfiguracyjnego."""
    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]

    api = TauronAPI(username, password)
    coordinator = TauronDataCoordinator(hass, api)
    await coordinator.async_refresh()

    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(TauronSensor(coordinator, sensor_type))

    async_add_entities(entities, True)

class TauronDataCoordinator:
    """Klasa koordynatora danych z API Tauron."""

    def __init__(self, hass: HomeAssistant, api: TauronAPI) -> None:
        """Zainicjuj koordynatora."""
        self.hass = hass
        self.api = api
        self.data = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_refresh(self) -> None:
        """Odśwież dane z API."""
        try:
            self.data = await self.hass.async_add_executor_job(
                self.api.get_sensors_data
            )
            if not self.data:
                _LOGGER.error("Nie udało się pobrać danych z API Tauron")
        except Exception as error:
            _LOGGER.error("Błąd podczas pobierania danych: %s", error)

class TauronSensor(SensorEntity):
    """Reprezentacja sensora Tauron."""

    def __init__(self, coordinator: TauronDataCoordinator, sensor_type: str) -> None:
        """Zainicjuj sensor."""
        self.coordinator = coordinator
        self.sensor_type = sensor_type
        self._attr_name = SENSOR_TYPES[sensor_type]["name"]
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_unique_id = f"tauron_{sensor_type}"

    @property
    def native_value(self) -> StateType:
        """Zwróć wartość sensora."""
        if self.coordinator.data and self.sensor_type in self.coordinator.data:
            return self.coordinator.data[self.sensor_type]["state"]
        return None

    async def async_update(self) -> None:
        """Zaktualizuj stan sensora."""
        await self.coordinator.async_refresh()