num = int(input("Enter number : "))

def factorial(num):
    if num == 0 or num == 1:
        return 1
    return num * factorial(num-1)
print("Factorial : ",factorial(num))