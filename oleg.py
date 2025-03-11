from vsmntrobot import go, left, right, wall

while True:
    while not wall():
        go()

    left()

    while not wall():
        go()

    left()

    while not wall():
        left()
        go()
        right()
        go()
