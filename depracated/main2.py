from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

root = Tk()
root.title('TCP/IP Lab Sim')
# root.iconbitmap('')
root.geometry("800x600")


w = 600
h = 400
x = w/2
y = h/2

my_canvas = Canvas(root, width=w, height=h, bg="white")
my_canvas.pack(pady=20)

#Add image to Canvas
# img = PhotoImage(file="training.jpeg")
img = ImageTk.PhotoImage(Image.open("assets/router_switch.png"))
my_image = my_canvas.create_image(260,125, anchor=NW, image=img)

def move(e):
    #e.x
    #e.y
    global img
    img = ImageTk.PhotoImage(Image.open("assets/router_switch.png"))
    my_image = my_canvas.create_image(e.x,e.y, image=img)
    my_label.config(text="Coordinates x:" + str(e.x) + " y:" + str(e.y))

my_label = Label(root, text="")
my_label.pack(pady=20)

root.bind('<B1-Motion>', move)

# Define a function to implement choice function
def choice(option):
   pop.destroy()
   if option == "yes":
      label.config(text="Hello, How are You?")
   else:
      label.config(text="You have selected No")
      root.destroy()
def click_fun():
   global pop
   pop = Toplevel(root)
   pop.title("Confirmation")
   pop.geometry("300x150")
   pop.config(bg="white")
   # Create a Label Text
   label = Label(pop, text="Would You like to Proceed?",
   font=('Aerial', 12))
   label.pack(pady=20)
   # Add a Frame
   frame = Frame(pop, bg="gray71")
   frame.pack(pady=10)
   # Add Button for making selection
   button1 = Button(frame, text="Yes", command=lambda: choice("yes"), bg="blue", fg="white")
   button1.grid(row=0, column=1)
   button2 = Button(frame, text="No", command=lambda: choice("no"), bg="blue", fg="white")
   button2.grid(row=0, column=2)
# Create a Label widget
label = Label(root, text="", font=('Aerial', 14))
label.pack(pady=40)

# Create a Tkinter button
root.Button(root, text="Click Here", command=click_fun).pack()

root.mainloop()