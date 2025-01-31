"""Komponent Tauron dla Home Assistant."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    Platform,
)

DOMAIN = "tauron_sensor"
PLATFORMS = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(minutes=15)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Skonfiguruj integrację Tauron na podstawie wpisu konfiguracyjnego."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_USERNAME: entry.data[CONF_USERNAME],
        CONF_PASSWORD: entry.data[CONF_PASSWORD],
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Wyładuj wpis konfiguracyjny."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok