import matplotlib, sys
matplotlib.use('TkAgg')
import matplotlib.animation as animation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk


class PersispyWindow:
    """
    creates the window to hold all important information about the
    graph
    """
    def __init__(self, root):
        self._frame = tk.Frame(root)
        root.wm_title("Persispy")

        self._root = root

        self._config_control()
        self._hasFig = False
        self._hasPointCloud = False
        self._cv = tk.Canvas(self._root, 
                width = 400,
                height = 400,
                bg='white')



    def _config_control(self):
        """Create the control panel on the right hand side
        
        This method is WAY too long, but GUI layout code is typically
        like this. Plus, Tkinter makes this even worse than it should be."""
        panel = tk.Frame(master=self._root)

        self.numPoints = tk.Scale(self._root, 
                from_ = 1000, 
                to = 5000, 
                resolution = 10, 
                orient = tk.VERTICAL)
        self.numPoints.pack(side = tk.RIGHT)

        self.distance = tk.Scale(self._root, 
                from_ = 0.1, 
                to = 0.2, 
                resolution = 0.01, 
                orient = tk.VERTICAL)
        self.distance.pack(side = tk.RIGHT)

        panel.columnconfigure(0,pad=3)
        panel.columnconfigure(1,pad=3)
        panel.rowconfigure(1,pad=0)
        panel.rowconfigure(2,pad=23)
        panel.rowconfigure(3,pad=3)
        panel.rowconfigure(4,pad=3)
        panel.rowconfigure(5,pad=3)
        panel.rowconfigure(6,pad=13)
        
        divider = tk.Frame(master=panel,height=2, bd=1, relief=tk.SUNKEN)
        divider.grid(row=1,columnspan=2, sticky='we')
        
        self._colorOptions = {"Dark2": 0,
                "Accent": 1,
                "Paired": 2,
                "rainbow": 3}
        self._color = tk.StringVar(self._root)
        self._color.set("Dark2")
        colorSelection = apply(tk.OptionMenu, (panel, self._color) + tuple(self._colorOptions.keys()))
        colorSelection.grid(row=3,column=1,sticky='w')
        
        
        # Control buttons
        button = tk.Button(master=panel, text='Show Plot', width=8, command=self._show_plot)
        button.grid(row=6,column=0,padx=(10,0))
        button = tk.Button(master=panel, text='Quit', width=8, command = self._quit) # command
        button.grid(row=6,column=1)
        
        panel.pack(side=tk.RIGHT, fill=tk.Y)




    from persispy.samples import plane
    from persispy.plot import plot2d
    def _show_plot(self):
        """
        updates the canvas when graph is pressed
        """
        pc = plane(100)
        fig = pc.plot2d(gui = True)

        self.canvas = FigureCanvasTkAgg(fig, self._root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect('key_press_event', self._on_key_event)
        self._hasFig = True
        self.canvas.draw()


    def _on_key_event(self, event):
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas, toolbar)



    def _quit(self):
        self._root.quit()     # stops mainloop
        self._root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate





def main():
    root = tk.Tk()


    window = PersispyWindow(root)


    window._root.mainloop()

if __name__ == "__main__": main()
