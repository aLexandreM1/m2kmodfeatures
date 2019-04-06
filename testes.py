import time, sched,timeit

# a = tuple('Monster;Hue;Game;Haha')
def callTimeCheck():
    start = (timeit.default_timer()*1000)
    return start

# b = str(a).split(';')

# #b = b.split(';')

# print(a,'Break1')

# for letter in b:
#     print(letter)
# start = int(round(time.time()*1000))
# print(start)
# time.sleep(1)
# end = int(round(time.time()*1000))
# result = end-start
# print(result)

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff...")
    # do your stuff

    s.enter(1, 1, do_something, (sc,))

s.enter(1, 1, do_something, (s,))
s.run()