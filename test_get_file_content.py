
from calculator.functions.get_file_content import get_file_content

def main():
    print("Result for current directory:")
    print(get_file_content("calculator", "lorem.txt"))
    print()

    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Result for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Result for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print("Result for pkg/does_not_exist.py:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print()


if __name__ == "__main__":
    main()