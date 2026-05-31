import json
import urllib.request


class WeatherAgent:
    """Agent that fetches real-time weather data from Open-Meteo (no API key needed)."""

    CITIES: dict[str, tuple[float, float]] = {
        "lisbon": (38.7223, -9.1393),
        "london": (51.5074, -0.1278),
        "new york": (40.7128, -74.0060),
        "paris": (48.8566, 2.3522),
        "berlin": (52.5200, 13.4050),
    }

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def _fetch(self, city: str, lat: float, lon: float) -> str:
        url = (
            f"{self.BASE_URL}?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,wind_speed_10m&temperature_unit=celsius"
        )
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read())
            current = data["current"]
            return (
                f"Current weather in {city.title()}: "
                f"{current['temperature_2m']}°C, "
                f"wind {current['wind_speed_10m']} km/h"
            )
        except Exception as e:
            return f"Could not fetch weather for {city}: {e}"

    def respond(self, query: str) -> str:
        q = query.lower()
        for city, (lat, lon) in self.CITIES.items():
            if city in q:
                return self._fetch(city, lat, lon)
        cities = ", ".join(c.title() for c in self.CITIES)
        return f"Ask about weather in one of: {cities}."


agent = WeatherAgent()

if __name__ == "__main__":
    queries = [
        "What's the weather in Lisbon?",
        "How cold is it in London?",
        "Tell me about New York weather",
        "What about Tokyo?",
    ]
    for q in queries:
        print(f"You:   {q}")
        print(f"Agent: {agent.respond(q)}")
        print()
