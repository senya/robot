from vsmntrobot import go, left, right, wall

while not wall():
    go()

left()

if wall():
    left()
    left()
    go()
    left()
else:
    go()
    right()

while not wall():
    go()
