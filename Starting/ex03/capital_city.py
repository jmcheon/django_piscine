import sys


def print_capital_city(state):
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver",
    }
    if state in states:
        value = states[state]
        print(capital_cities[value])
    else:
        print("Unknown state")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print_capital_city(sys.argv[1])
