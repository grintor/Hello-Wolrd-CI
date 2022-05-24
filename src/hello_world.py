def main():
    print("Hello world!")  # noqa: T001


def foo(num):
    if num > 1:
        print("bar")  # noqa: T001
        if num < 2:
            print("sds")  # noqa: T001


if __name__ == "__main__":
    main()
