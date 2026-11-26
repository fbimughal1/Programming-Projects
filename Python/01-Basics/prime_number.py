n = int(input("Enter number: "))


if n < 2:
    print(n, "is not a Prime number.")
else:
    count = 0
    
    for i in range(2, n):   # 2 se n-1 tak chalega
        if n % i == 0:
            count = 1       # agar divide ho gaya to count badha do
    
    if count == 0:
        print(n, "is a Prime number.")
    else:
        print(n, "is not a Prime number.")