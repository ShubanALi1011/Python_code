n = int(input("Enter number : "))
isPrime = True
for i in range(2, n):
    if n%i == 0:
        isPrime = False

if isPrime:
    print("Prime ha.")
else:
    print("Prime nhi ha.")