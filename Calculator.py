class Calculator:
    @staticmethod
    def add(num1: float, num2: float) -> float:
        """Returns the sum of two numbers."""
        return num1 + num2

    @staticmethod
    def divide(numerator: float, denominator: float) -> float:
        """
        Returns the quotient of a division.
        Raises a ZeroDivisionError if attempting to divide by zero.
        """
        if denominator == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return numerator / denominator
