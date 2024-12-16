import tkinter as tk
from tkinter.constants import *


def make_credits():
    class CreditList:
        def __init__(self, lines):
            self.location = HEIGHT
            self.text = canvas.create_text(0, 0, text='\n'.join(lines), justify=CENTER,
                                           anchor=NW, fill='black', font='Time 40')
            xl, yt, xr, yb = canvas.bbox(self.text)
            txtwidth = max(xr - xl, WIDTH)
            xpos = (WIDTH - txtwidth) // 2  # To center text horizontally.
            canvas.move(self.text, xpos, self.location)

        def roll_credits(self):
            xl, yt, xr, yb = canvas.bbox(self.text)
            if yb <= 0:  # Completely off top of screen?
                canvas.pack_forget()
                tk.Button(text='Done', font=('Courier New', 20), relief=GROOVE, bg='orange',
                          command=window.quit).place(x=WIDTH / 2, y=HEIGHT / 2)
                return  # Stop.
            canvas.move(self.text, 0, -3)
            window.after(DELAY, self.roll_credits)  # Keep going.

    DELAY = 40  # Millisecs.
    HEIGHT, WIDTH = 900, 900
    window = tk.Tk()
    window.resizable(False, False)
    window.update_idletasks()
    window.geometry("800x700")
    window.title('Credits')

    canvas = tk.Canvas(window, width=WIDTH, height=WIDTH, bg='green', bd=0,
                        highlightthickness=0, relief='ridge')
    canvas.pack()

    credits = open('../credits.txt').read().splitlines()
    cl = CreditList(credits)
    window.after(DELAY, cl.roll_credits)  # Start rolling credits "loop".
    window.mainloop()

if __name__ == '__main__':
    try:
        make_credits()
    except:
        pass