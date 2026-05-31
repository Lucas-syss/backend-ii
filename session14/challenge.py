class KeywordAgent:
    """AI agent that handles multiple queries with keyword-based response mapping."""

    RESPONSES: dict[str, str] = {
        "hello": "Hi there! How can I assist you today?",
        "help": "I can respond to: hello, help, time, weather, joke, status, bye.",
        "time": "I don't have access to a clock, but your system can tell you the time!",
        "weather": "I can't check live weather, but try a weather service like open-meteo.com.",
        "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
        "status": "All systems operational. Running normally.",
        "bye": "Goodbye! Have a great day!",
    }

    def __init__(self, name: str):
        self.name = name

    def respond(self, query: str) -> str:
        q = query.lower().strip()
        for keyword, response in self.RESPONSES.items():
            if keyword in q:
                return response
        return f"Sorry, I didn't understand '{query}'. Type 'help' to see what I can do."


agent = KeywordAgent("SmartAgent")

if __name__ == "__main__":
    queries = [
        "Hello!",
        "Tell me a joke",
        "What's the weather like?",
        "help",
        "What is the current time?",
        "Something completely unknown",
        "bye",
    ]
    for q in queries:
        print(f"You:   {q}")
        print(f"{agent.name}: {agent.respond(q)}")
        print()
