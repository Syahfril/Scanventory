import time

def function1():
    while True:
        # some code here
        function2()  # calling function2
        time.sleep(5)  # wait for 5 seconds

def function2():
    print("Hello from function2!")
    # any other code you want to execute goes here

function1()  # start the loop in function1
