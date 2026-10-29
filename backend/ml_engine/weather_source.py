"""Public historical weather lookup for image-aligned environmental inputs."""

from datetime import date
import json
import math
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class WeatherSourceError(RuntimeError):
    pass


def fetch_weather_for_observation(
    latitude: float, longitude: float, observation_date: str | date
) -> dict:
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        observed_on = (
            observation_date
            if isinstance(observation_date, date)
            else date.fromisoformat(observation_date)
        )
    except (TypeError, ValueError) as exc:
        raise WeatherSourceError("A valid latitude, longitude, and YYYY-MM-DD date are required.") from exc

    if not math.isfinite(latitude) or not -90 <= latitude <= 90:
        raise WeatherSourceError("Latitude must be between -90 and 90 degrees.")
    if not math.isfinite(longitude) or not -180 <= longitude <= 180:
        raise WeatherSourceError("Longitude must be between -180 and 180 degrees.")
    if observed_on > date.today():
        raise WeatherSourceError("The observation date cannot be in the future.")

    endpoint = "https://archive-api.open-meteo.com/v1/archive"
    params = urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "start_date": observed_on.isoformat(),
        "end_date": observed_on.isoformat(),
        "daily": (
            "temperature_2m_mean,relative_humidity_2m_mean,"
            "precipitation_sum,wind_speed_10m_max"
        ),
        "timezone": "UTC",
    })
    request = Request(f"{endpoint}?{params}", headers={"User-Agent": "AI-Crop-Disease-Prediction/1.0"})

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise WeatherSourceError(f"Open-Meteo historical weather lookup failed: {exc}") from exc

    daily = payload.get("daily", {})
    try:
        weather = {
            "temperature": float(daily["temperature_2m_mean"][0]),
            "relative_humidity": float(daily["relative_humidity_2m_mean"][0]),
            "rainfall_mm": float(daily["precipitation_sum"][0]),
            "wind_speed_kmh": float(daily["wind_speed_10m_max"][0]),
        }
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise WeatherSourceError(
            "Open-Meteo returned no complete daily weather observation for that location and date."
        ) from exc

    if not all(math.isfinite(value) for value in weather.values()):
        raise WeatherSourceError("Open-Meteo returned non-finite weather values.")

    humidity = weather["relative_humidity"]
    rainfall = weather["rainfall_mm"]
    wetness_proxy = 0.0
    if humidity >= 80:
        wetness_proxy = min(24.0, 2.0 + (humidity - 80.0) * 0.5)
    if rainfall > 0:
        wetness_proxy = min(24.0, max(wetness_proxy, min(12.0, 2.0 + rainfall * 0.4)))

    return {
        **weather,
        "leaf_wetness_hours": round(wetness_proxy, 1),
        "source": {
            "name": "Open-Meteo Historical Weather API",
            "url": endpoint,
            "latitude": latitude,
            "longitude": longitude,
            "observation_date": observed_on.isoformat(),
            "timezone": "UTC",
            "variables": [
                "temperature_2m_mean",
                "relative_humidity_2m_mean",
                "precipitation_sum",
                "wind_speed_10m_max",
            ],
            "leaf_wetness": "estimated proxy from daily humidity and precipitation; not directly observed",
            "spatially_aligned": True,
            "temporally_aligned": True,
        },
    }
