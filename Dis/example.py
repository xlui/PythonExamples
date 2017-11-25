import dis


def fn_expressive(upper=1000000):
    return sum(range(upper))


def fn_terse(func=sum, upper=1000000):
    return func(range(upper))


def fn_while_1():
    while 1:
        pass


def fn_while_true():
    while True:
        pass


if __name__ == '__main__':
    print("functions return the same result: ", fn_expressive() == fn_terse())

    print(fn_expressive.__name__)
    dis.dis(fn_expressive)

    print(fn_terse.__name__)
    dis.dis(fn_terse)

    print(fn_while_1.__name__)
    dis.dis(fn_while_1)

    print(fn_while_true.__name__)
    dis.dis(fn_while_true)
