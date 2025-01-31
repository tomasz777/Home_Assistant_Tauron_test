"""Config flow dla integracji Tauron."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .tauron_api import TauronAPI

class TauronConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Obsługa config flow dla Tauron."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Obsługa kroku wprowadzania danych przez użytkownika."""
        errors = {}

        if user_input is not None:
            # Sprawdź poprawność danych logowania
            api = TauronAPI(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if await self.hass.async_add_executor_job(api.login):
                return self.async_create_entry(
                    title=f"Tauron ({user_input[CONF_USERNAME]})",
                    data=user_input,
                )
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )