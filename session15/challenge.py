import json
import re
import urllib.request
from datetime import datetime

CITY_COORDS: dict[str, tuple[float, float]] = {
    "lisbon":   (38.7223, -9.1393),
    "london":   (51.5074, -0.1278),
    "new york": (40.7128, -74.0060),
    "paris":    (48.8566, 2.3522),
    "berlin":   (52.5200, 13.4050),
    "tokyo":    (35.6762, 139.6503),
    "sydney":   (-33.8688, 151.2093),
}


class StatefulWeatherAgent:
    """Advanced agent with conversation history and multi-city weather support."""

    def __init__(self, name: str):
        self.name = name
        self.history: list[dict[str, str]] = []

    def _fetch_weather(self, city: str) -> str:
        lat, lon = CITY_COORDS[city]
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,wind_speed_10m,weathercode"
            "&temperature_unit=celsius"
        )
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read())
            c = data["current"]
            return (
                f"Weather in {city.title()}: "
                f"{c['temperature_2m']}°C, "
                f"wind {c['wind_speed_10m']} km/h"
            )
        except Exception as e:
            return f"Failed to fetch weather for {city.title()}: {e}"

    def _record(self, query: str, response: str) -> None:
        self.history.append({
            "time": datetime.now().isoformat(timespec="seconds"),
            "query": query,
            "response": response,
        })

    def respond(self, query: str) -> str:
        q = query.lower().strip()

        if q in ("history", "show history"):
            if not self.history:
                return "No conversation history yet."
            lines = [
                f"[{h['time']}] You: {h['query']} → {h['response']}"
                for h in self.history
            ]
            return "Conversation history:\n" + "\n".join(lines)

        is_weather_query = bool(
            re.search(r"\b(weather|temperature|temp|hot|cold|warm|wind)\b", q)
        )

        if is_weather_query:
            matched = next((c for c in CITY_COORDS if c in q), None)
            if matched:
                response = self._fetch_weather(matched)
            else:
                cities = ", ".join(c.title() for c in CITY_COORDS)
                response = f"I can check weather for: {cities}. Which city?"
        else:
            response = (
                "I specialise in weather queries. "
                "Try: 'What's the temperature in Paris?' or type 'history'."
            )

        self._record(query, response)
        return response


if __name__ == "__main__":
    agent = StatefulWeatherAgent("WeatherBot")
    queries = [
        "What's the weather in Lisbon?",
        "How cold is it in Tokyo?",
        "Tell me about Paris",
        "What about Sydney temperature?",
        "Something unrelated",
        "history",
    ]
    for q in queries:
        print(f"You:   {q}")
        print(f"{agent.name}: {agent.respond(q)}")
        print()
