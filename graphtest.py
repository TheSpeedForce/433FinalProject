import tkinter as Tk
from random import randint
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window:

    def __init__(self,master):
        frame = Tk.Frame(master)

        self.fig = plt.figure(figsize=(14, 4.5), dpi=100)

        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.set_ylim(0, 100)
        self.line, = self.ax.plot(xar, yar)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

    def animate(self,i):
        xar = []
        yar = []
        for j in range (1,10):
            xar.append (j)
            yar.append (randint (1,100))
        self.ax.clear()
        self.ax.plot (xar, yar)

xar = []
yar = []

root = Tk.Tk()
app = Window(root)
ani = animation.FuncAnimation(app.fig, app.animate, interval=1000, blit=False)
root.mainloop()
