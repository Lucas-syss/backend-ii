class SimpleAgent:
    """A minimal AI agent that returns a predefined message for a specific input."""

    def __init__(self, name: str):
        self.name = name

    def respond(self, query: str) -> str:
        if query.strip().lower() == "hello":
            return f"Hi! I'm {self.name}. How can I help you today?"
        return "I only understand 'hello' right now. Try saying hello!"


agent = SimpleAgent("SimpleAgent")

if __name__ == "__main__":
    test_queries = ["hello", "Hello!", "HELLO", "goodbye", ""]
    for q in test_queries:
        print(f"You:   {q!r}")
        print(f"Agent: {agent.respond(q)}")
        print()
