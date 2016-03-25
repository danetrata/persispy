import tkinter
import tkinter.ttk as ttk

from test_connected_components import stratified, double_stratified, monte_carlo


class Textbox:
    def __init__(self, parent, label):
        name = ttk.Label(parent, text = label)
        self.textbox = ttk.Entry(parent)

        name.grid(sticky = tkinter.W)
        self.textbox.grid()


    def get(self):
        return self.textbox.get()

class Interface:

    def __init__(self):
        self.currentTest = ""

        root = tkinter.Tk()

        buttonFrame = ttk.Frame()
        window = ttk.Frame()

        buttonBar = []

        stratified = ttk.Button(buttonFrame, \
                text = 'stratified', 
                command = lambda: self.create_stratified_window(window))
        buttonBar.append(stratified)

        doubleStratified = ttk.Button(buttonFrame, \
                text = 'double stratified', 
                command = lambda: self.create_double_stratified_window(window))
        buttonBar.append(doubleStratified)

        monteCarlo = ttk.Button(buttonFrame, \
                text = 'monte carlo', 
                command = lambda: self.create_monte_carlo_window(window))
        buttonBar.append(monteCarlo)

        for i, button in enumerate(buttonBar):
            button.grid(row = 0, column = i)
        
        buttonFrame.grid()
        window.grid()



        run = ttk.Button(text = 'run',
                command = lambda: self.run_test(window))
        run.grid()

        root.mainloop()

    def create_stratified_window(self, parent):

        self.currentTest = "stratified_window"

        for child in parent.winfo_children():
            child.destroy()

        settingsWindow = ttk.Frame(parent)

        Textbox(settingsWindow, "e(n)")
        Textbox(settingsWindow, "Starting number of points")
        Textbox(settingsWindow, "Ending number of points")
        Textbox(settingsWindow, "Number of points increment")

        settingsWindow.grid()

    def create_double_stratified_window(self, parent):

        self.currentTest = "double_stratified"

        for child in parent.winfo_children():
            child.destroy()

        settingsWindow = ttk.Frame(parent)

        Textbox(settingsWindow, "Starting distance")
        Textbox(settingsWindow, "Ending distance")
        Textbox(settingsWindow, "Distance increment")
        Textbox(settingsWindow, "Starting number of points")
        Textbox(settingsWindow, "Ending number of points")
        Textbox(settingsWindow, "Number of points increment")

        settingsWindow.grid()

    def create_monte_carlo_window(self, parent):

        self.currentTest = "monte_carlo"

        for child in parent.winfo_children():
            child.destroy()

        settingsWindow = ttk.Frame(parent)

        Textbox(settingsWindow, "Lower distance")
        Textbox(settingsWindow, "Upper distance")
        Textbox(settingsWindow, "Lower number of points")
        Textbox(settingsWindow, "Upper number of points")
        Textbox(settingsWindow, "Number of trials")

        settingsWindow.grid()

    def get_children_values(self, parent):
        [children] = self.get_children_values_recursive(parent)
        for child in children:
            if child.winfo_class() == "TEntry":
                print(child.get())

    def get_children_values_recursive(self, parent):
        if not parent.winfo_children():
            return parent
        else:
            children = []
            for child in parent.winfo_children():
                children.append(self.get_children_values_recursive(child))
            return children

    def run_test(self, parent):

        pass
        exec(self.currentTest+"()")


def test():

    root = tkinter.Tk()

    ft = ttk.Frame()
    fb = ttk.Frame()

    ft.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
    fb.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)

    pb_hd = ttk.Progressbar(ft, orient='horizontal', mode='determinate')
    pb_hD = ttk.Progressbar(ft, orient='horizontal', mode='indeterminate')
    pb_vd = ttk.Progressbar(fb, orient='vertical', mode='determinate')
    pb_vD = ttk.Progressbar(fb, orient='vertical', mode='indeterminate')

    pb_hd.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
    pb_hD.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
    pb_vd.pack(expand=True, fill=tkinter.BOTH, side=tkinter.LEFT)
    pb_vD.pack(expand=True, fill=tkinter.BOTH, side=tkinter.LEFT)

    def increment():
        pb_hd.step()

    import time



    button = ttk.Button(ft, text = "Click", command = increment)

    button.pack(expand=True, fill=tkinter.BOTH, side=tkinter.LEFT)

    pb_hd.start(50)
    pb_hD.start(50)
    pb_vd.start(50)
    pb_vD.start(50)

    for _ in range(99):
        increment()
        time.sleep(0.1)
        root.update()

    root.mainloop()


if __name__ == '__main__':
    Interface()
