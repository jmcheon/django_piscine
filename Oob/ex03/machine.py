import random


class CoffeeMachine:
    def __init__(self):
        self.count = 0

    class EmptyCup(HotBeverage):
        docs="An empty cup?! Gimme my money back!"
        def __init__(self, price=0.90, name="empty cup"):
            super().__init__(price, name)

    class BrokenMachineException(Exception):
        def __init__(self, message="This coffee machine has to be repaired.")
            super().__init__(message)

    def repair(self):

    def serve(self):

