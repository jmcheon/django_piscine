from path import Path as path


def ex01():
    try:
        dir_path = path.mkdir("test")
    except FileExistsError as e:
        dir_path = None
        print(e)

    if dir_path:
        path.touch(dir_path + "/test.txt")
        file = path(dir_path + "/test.txt")
        file.write_lines(["hello", "world!!"])
        print(file.read_text())


if __name__ == "__main__":
    ex01()
