from vsmntrobot import coin, flag, go, left, right, set_flag, wall, wall_right


while True:
    if wall():
        left()
    else:
        if not wall_right():
            right()
        go()
