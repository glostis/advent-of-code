def main():
    card_pub_key = 10441485
    door_pub_key = 1004920

    key = 0
    loop_size = 0
    card_loop_size = None
    door_loop_size = None
    for loop_size, key in loop_public_key():
        if key == card_pub_key:
            card_loop_size = loop_size
        if key == door_pub_key:
            door_loop_size = loop_size
        if card_loop_size is not None and door_loop_size is not None:
            break
    encryption_key = public_key(card_loop_size, door_pub_key)
    print(encryption_key)


def loop_public_key(loop_size=None, subject_number=7):
    value = 1
    loop_size = 1
    while True:
        value *= subject_number
        value = value % 20201227
        yield loop_size, value
        loop_size += 1


def public_key(loop_size, subject_number=7):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


if __name__ == "__main__":
    main()
