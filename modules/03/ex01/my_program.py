from path import Path as path


def ex01():
    path = path.mkdir("test")
    file = path.touch(path/"test.txt")
    file.write_lines(["test", "lines"])


if __name__ == "__main__":
    ex01()
    
