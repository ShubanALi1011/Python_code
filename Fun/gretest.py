def greatest():
    a = int(input("Enter first no : "))
    b = int(input("Enter first no : "))
    c = int(input("Enter first no : "))

    if a > b and a > c:
        print("Greatest : ",a)
    elif b > a and b > c:
        print("Greatest : ",b)
    else:
        print("Greatest : ",c)

greatest()