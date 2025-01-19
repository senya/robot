from vsmntrobot import robot

x = 0

while True:
    if robot.wall_right():
        if robot.wall():
            robot.left()
        else:
            robot.go()
    else:
        robot.right()
        robot.go()
