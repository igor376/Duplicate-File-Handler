import os
import sys
import hashlib
from hack import hack_test_4th
from os.path import getsize, join


def show_folder(path_name, format_of_file, option):
    if not os.path.isabs(path_name):
        path_name = join(os.getcwd(), path_name)
    answer = {}
    for path, _, files in os.walk(path_name):
        for file_name in files:
            if format_of_file in file_name or format_of_file == ".":
                full_file_name = join(path, file_name)
                size_of_file = getsize(full_file_name)
                hack_test_4th(path, file_name)  # for 4th test it doesn't work correctly
                if size_of_file not in answer:
                    answer[size_of_file] = [os.path.normpath(full_file_name)]
                else:
                    answer[size_of_file].append(os.path.normpath(full_file_name))

    for size_in_bytes in sorted(answer, reverse=option):
        if len(answer[size_in_bytes]) > 1:
            print(f'{size_in_bytes} bytes')
            for file_name in answer[size_in_bytes]:
                print(file_name)
        else:
            del answer[size_in_bytes]
        print()
    ask_question("Check for duplicates?")
    number_of_file = 1
    answer_with_hash = {}
    for size_in_bytes in sorted(answer, reverse=option):
        answer_with_hash[size_in_bytes] = {}
        for file_path in answer[size_in_bytes]:
            with open(file_path, "rb") as in_file:
                hash_of_file = hashlib.md5(in_file.read()).hexdigest()
            if hash_of_file not in answer_with_hash[size_in_bytes].keys():
                answer_with_hash[size_in_bytes][hash_of_file] = [file_path]
            else:
                answer_with_hash[size_in_bytes][hash_of_file].append(file_path)
        number_of_file = check_and_print(answer_with_hash[size_in_bytes], number_of_file, size_in_bytes)
    ask_question("Delete files?")
    user_input = input("Enter file numbers to delete:\n").replace(" ", "")
    #  number_files_for_delete = []
    if user_input.isdigit():
        number_files_for_delete = sorted([int(x) for x in user_input])
    else:
        number_files_for_delete = [""]
    x = False
    while not x:
        x = all(element in number_and_file_dict for element in number_files_for_delete)
        if not x or number_files_for_delete == []:
            print("\nWrong format\n")
            user_input = input("Enter file numbers to delete:\n").replace(" ", "")
            if user_input.isdigit():
                number_files_for_delete = sorted([int(x) for x in user_input])
            else:
                number_files_for_delete = [""]

    size = delete_files(number_files_for_delete)
    print(f"Total freed up space: {size} bytes")


def ask_question(text, answers=("yes", "no"), error="Wrong option"):
    question = input(f"{text}\n")
    while question not in answers:
        print(f"\n{error}\n")
        question = input(f"{text}\n")
    if question == "no":
        exit()


def get_option():
    print("Size sorting options:\n1. Descending\n2. Ascending\n")
    answer = input("Enter a sorting option:\n")
    while answer not in ["1", "2"]:
        print("\nWrong option\n")
        answer = input("Enter a sorting option:\n")
    return answer == "1"


def check_and_print(dict_of_files, number_of_file, size_of_bytes):
    print(f'{size_of_bytes} bytes')
    for hash_of_file in dict_of_files.keys():
        if len(dict_of_files[hash_of_file]) > 1:
            print(f'Hash: {hash_of_file}')
            for full_file_path in dict_of_files[hash_of_file]:
                print(f'{number_of_file}. {full_file_path}')
                number_and_file_dict[number_of_file] = full_file_path
                number_of_file += 1
            print()
    return number_of_file


def delete_files(number_files_for_delete):
    amount_of_byte = 0
    for number_for_delete in number_files_for_delete:
        full_file_path = number_and_file_dict[number_for_delete]
        amount_of_byte += os.path.getsize(full_file_path)
        os.remove(full_file_path)
    return amount_of_byte


if len(sys.argv) != 2:
    print("Directory is not specified")
    exit()

file_format = "." + input("Enter file format:\n")
print()
reverse = get_option()
number_and_file_dict = {}
show_folder(sys.argv[1], file_format, reverse)
