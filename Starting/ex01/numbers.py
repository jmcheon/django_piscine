def print_numbers(filename):
    with open(filename, "r") as file:
        content = file.read()
        numbers = content.replace(",", "\n").split()
        for number in numbers:
            print(number)


if __name__ == "__main__":
    print_numbers("numbers.txt")
