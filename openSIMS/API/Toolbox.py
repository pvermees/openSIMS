import datetime
import numpy as np

def get_date(datestring):
    date_patterns = ["%d/%m/%Y","%Y/%m/%d","%m/%d/%Y","%Y/%d/%m"]
    return get_datetime(datestring,date_patterns).date()

def get_time(timestring):
    time_patterns = ["%I:%M %p","%H:%M","%I:%M:%S %p","%H:%M:%S"]
    return get_datetime(timestring,time_patterns).time()

def get_datetime(dtstring,patterns):
    for pattern in patterns:
        try:
            return datetime.datetime.strptime(dtstring,pattern)
        except:
            pass
    raise ValueError('Invalid datetime string.')

def linearfit(x,y,B=None):
    D = np.vstack([x, np.ones(len(x))]).T
    y = y[:, np.newaxis]
    res = np.dot((np.dot(np.linalg.inv(np.dot(D.T,D)),D.T)),y)
    slope = res[0][0]
    intercept = res[1][0]
    return intercept, slope

def show_figure(fig):
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    root = tk.Tk()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()
    root.mainloop()
