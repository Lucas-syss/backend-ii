from abc import ABC, abstractmethod
import math

# --- Abstract Base ---

class Shape(ABC):
    """Abstract base class. All shapes must implement area()."""

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def describe(self):
        pass


# --- Concrete Shapes ---

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def describe(self):
        return f"Circle with radius {self.radius}"


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

    def describe(self):
        return f"Square with side {self.side}"


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

    def describe(self):
        return f"Triangle with base {self.base} and height {self.height}"


# --- Factory Function ---

def shape_factory(shape_type, *args):
    """
    Create and return a Shape object based on shape_type string.

    Args:
        shape_type: "circle", "square", or "triangle"
        *args: dimensions passed to the shape constructor
    """
    shapes = {
        "circle": Circle,
        "square": Square,
        "triangle": Triangle,
    }

    shape_type = shape_type.lower()

    if shape_type not in shapes:
        raise ValueError(
            f"Unknown shape '{shape_type}'. Available: {list(shapes.keys())}"
        )

    return shapes[shape_type](*args)


# --- Usage ---

if __name__ == "__main__":
    shapes = [
        shape_factory("circle", 5),
        shape_factory("square", 4),
        shape_factory("triangle", 6, 3),
    ]

    for shape in shapes:
        print(f"{shape.describe()} → Area: {shape.area():.2f}")

    # Error handling
    try:
        shape_factory("hexagon", 5)
    except ValueError as e:
        print(f"\nError caught: {e}")