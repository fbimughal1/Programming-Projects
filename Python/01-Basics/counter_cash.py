price = [12.05, 15.00, 25.00, 22.35, 17.50]
discounted_price = 0
count = 0
while(count>20):
    if price >=20:
        discounted_price = price * 0.90
    else:
        discounted_price = 0
print(f"The prices are ${price:.2f}")