# from tkinter import *
#
# if __name__ == '__main__':
#     root = Tk() # blank window
#
#     top_frame = Frame(root)
#     top_frame.pack()
#     bottom_frame = Frame(root)
#     bottom_frame.pack(side=BOTTOM)
#
#     button_one = Button(top_frame, text='button_one', fg='red')
#     button_two = Button(top_frame, text='button_two', fg='green')
#     button_three = Button(top_frame, text='button_three', fg='blue')
#
#     button_four = Button(bottom_frame, text='button_four', fg='yellow', bg='black')
#
#     button_one.pack(side=LEFT)
#     button_two.pack(side=LEFT)
#     button_three.pack(side=LEFT)
#     button_four.pack(side=LEFT)
#
#     root.mainloop()


from database import MariaDB

test = MariaDB()
test.create_player('alan', 'teste')
