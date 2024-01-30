import random

from beverages import Cappuccino, Chocolate, Coffee, HotBeverage, Tea


class CoffeeMachine:
    def __init__(self):
        self.count = 0

    class EmptyCup(HotBeverage):
        docs="An empty cup?! Gimme my money back!"
        def __init__(self, price=0.90, name="empty cup"):
            super().__init__(price, name)

    class BrokenMachineException(Exception):
        def __init__(self, message="This coffee machine has to be repaired."):
            super().__init__(message)

    def repair(self):
        self.count = 0
        print("machine has been repaired")


    def serve(self, instance):
        self.count += 1
        if self.count > 9:
            raise self.BrokenMachineException()
        if random.randrange(2) == 0:
            return instance()
        return self.EmptyCup()


if __name__ == "__main__":
    bev_dict = {0: HotBeverage, 1: Coffee, 2: Tea, 3: Chocolate, 4: Cappuccino}
    try:
        machine = CoffeeMachine()
        for _ in range(10):
            print(machine.serve(bev_dict.get(random.randrange(5))))
    except Exception as e:
        print(e)
        machine.repair()
