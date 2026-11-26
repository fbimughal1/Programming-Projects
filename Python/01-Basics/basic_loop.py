import turtle

t = turtle.Turtle()
t.speed(5)

# location
t.penup()
t.goto(-100,0)
t.pendown()

#rectangle shape
t.color("Red")
for i in range(2):
    t.forward(200)
    t.right(90)
    t.forward(100)
    t.right(90)


turtle.done()


# word = input('Enter the word/sentence you want to repeat: ')
# rep = int(input("Enter the number of repetitions: "))

# for i in range(0 , rep + 1):
#     print(word)
    

