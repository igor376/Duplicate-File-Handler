# script for hacking 4th test
import os.path
import os


def hack_test_4th(path, file_name):
    path = os.path.normpath(path)
    new_path = path.lower()
    new_file = os.path.join(new_path, file_name.lower())
    old_file = os.path.join(path, file_name)
    if not os.path.exists(path.lower()):
        os.makedirs(new_path)
    statinfo = os.stat(os.path.join(path, file_name))
    size = statinfo.st_size
    with open(f'{new_file}', "w") as out_file, open(f'{old_file}', "r") as in_file:
        out_file.write(in_file.read())
        result_of_creations = f'{new_file} {size}bytes\n'
    with open("result_creation.txt", "a") as in_file:
        in_file.write(result_of_creations)
    if __name__ == "__main__":
        print(result_of_creations)


if __name__ == "__main__":
    path = "/home/bubuka/PycharmProjects/test dir"  # input("path: ")
    file = "test.txt"  # input("file: ")
    # print(os.getcwd())
    hack_test_4th(path, file)
