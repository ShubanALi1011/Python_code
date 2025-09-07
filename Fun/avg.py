a = int(input("Enter your 1 number : "))
b = int(input("Enter your 2 number : "))
c = int(input("Enter your 3 number : "))

def avg(a,b,c):
    avg = (a+b+c)/3
    return avg

print("Avg : ",avg(a,b,c))