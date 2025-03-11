from vsmntrobot import go, left, right, flag, set_flag, coin, wall

set_flag()

while not wall():
    go()

left()
left()

while not coin():
    go()
