import time

# now = time.localtime()
# print(time.strftime(["%f",now]))

now = time.time_ns()

print(now)

time.sleep(1)

print(time.time_ns() - now)
