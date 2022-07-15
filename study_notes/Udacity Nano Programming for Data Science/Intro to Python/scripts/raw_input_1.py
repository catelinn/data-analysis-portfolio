name = input("Enter your name: ")
print("Hello there, {}!".format(name.title()))

# convert input string to integer
num = int(input("Enter an integer: "))
print("hello" * num)

# use `eval` to evaluate the input string, 
# so if user inputs `2*3`, the ouput will be `6`
result = eval(input("Enter an expression: "))
print(result)