from abc import ABC, abstractmethod


# --- Observer Interface ---

class Observer(ABC):
    """All observers must implement update()."""

    @abstractmethod
    def update(self, event, data):
        pass


# --- Subject ---

class Subject:
    """
    Maintains a list of observers and notifies them on state changes.
    Observers can be attached or detached at any time.
    """

    def __init__(self, name):
        self.name = name
        self._observers = []
        self._state = None

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"  [{self.name}] Observer '{observer.name}' attached.")

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"  [{self.name}] Observer '{observer.name}' detached.")

    def notify(self, event):
        """Notify all currently attached observers."""
        for observer in self._observers:
            observer.update(event, self._state)

    def set_state(self, new_state):
        """Update state and automatically notify all observers."""
        print(f"\n[{self.name}] State changed: '{self._state}' → '{new_state}'")
        self._state = new_state
        self.notify(event="state_change")


# --- Concrete Observers ---

class Logger(Observer):
    """Logs every state change to console."""

    def __init__(self):
        self.name = "Logger"
        self.log = []

    def update(self, event, data):
        entry = f"[LOG] Event='{event}' | Data='{data}'"
        self.log.append(entry)
        print(f"  {entry}")


class EmailNotifier(Observer):
    """Simulates sending an email when state changes to 'critical'."""

    def __init__(self, email):
        self.name = "EmailNotifier"
        self.email = email

    def update(self, event, data):
        if data == "critical":
            print(f"  [EMAIL] Alert sent to {self.email}: system is now '{data}'!")
        else:
            print(f"  [EMAIL] No alert needed for state '{data}'.")


class Dashboard(Observer):
    """Simulates a UI dashboard that always refreshes on update."""

    def __init__(self):
        self.name = "Dashboard"

    def update(self, event, data):
        print(f"  [DASHBOARD] Refreshing display → current status: '{data}'")


# --- Demo ---

if __name__ == "__main__":
    # Create subject
    server = Subject("WebServer")

    # Create observers
    logger = Logger()
    emailer = EmailNotifier("admin@example.com")
    dashboard = Dashboard()

    # Attach observers
    server.attach(logger)
    server.attach(emailer)
    server.attach(dashboard)

    # Trigger state changes
    server.set_state("starting")
    server.set_state("running")
    server.set_state("critical")

    # Detach one observer and change state again
    print()
    server.detach(dashboard)
    server.set_state("recovering")

    # Show logger's history
    print("\n--- Full Log History ---")
    for entry in logger.log:
        print(entry)