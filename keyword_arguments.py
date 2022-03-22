def func(*args, **kwargs):
    # arguments = args = tuple
    # KeyWordArguments = kwargs = dictionary
    print(args)
    print(kwargs)


def main():
    func(1, 2, 3, name='Victor', age=34)


if __name__ == '__main__':
    main()