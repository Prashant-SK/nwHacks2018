"""
dataPlotGUI: Class to plot and visualize patient data
"""

import Tkinter
import tkMessageBox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime
import os

class App:
    
    def save(self):
        datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        subdirectory = 'saved_plots/'
        # Creating new subdirectory if it doesn't already exist
        try:
            os.stat(subdirectory)
        except:
            os.mkdir(subdirectory) 
            
        saveName = self.fieldVal.get() + "_plot.jpg"
        self.fig.savefig(subdirectory + saveName)
        tkMessageBox.showinfo("Save", "Figure saved as " + saveName)
        
    def plotQuit(self):
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL state
                        
    # Function to clear and make plot
    def make_plot(self, field):
             
        self.p.cla()
        name = self.pData['Patient Surname'][0] + ', ' + self.pData['Patient Firstname'][0]
        self.p.cla()
        self.p.plot(self.pData['Date'], self.pData[field])
        self.p.set_xlabel('Date', **self.figFont)
        self.p.set_ylabel('Score', **self.figFont)
        self.p.set_title(field + ' Scores for ' + name, **self.figFont)
        self.p.grid(True)
        
    def change_field(self, event):
        field = self.fieldVal.get()
        self.make_plot(field)
        self.canvas.draw()
        
    def __init__(self, master):
        # Create a container
        frame = Tkinter.Frame(master)
        
        # Initial values for fonts and figure size
        self.figWidth = 12
        self.figHeight = 5
        self.figFont = {'fontname':'Helvetica'}
    
        # Importing data
        self.fileName = 'selfReportData.csv'
        self.pData = pd.read_csv(self.fileName)
        
        for x in range (0, len(self.pData.index)):
            tempVal = pd.to_datetime(str(self.pData['Date'][x]), format = '%Y%m%d')
            self.pData['Date'][x] = tempVal
                         
        # Creating User Controls
    
        # Field selection
        self.fieldVal = Tkinter.StringVar(frame)
        self.fieldVal.set("Mood")
        self.field_select = Tkinter.OptionMenu(frame, self.fieldVal, "Mood", "Energy", "Concentration", "Interest In Activities", "Agitation", "Guilt", "Suicidality", "Weight", "Hours of Sleep" , command=self.change_field)
        self.field_select.pack(side="left")
        

        # Save Button   
        self.saveButton = Tkinter.Button(frame, text='Save Figure', command=self.save)
        self.saveButton.pack(side="left") 
        
        # Quit button
        self.quitButton = Tkinter.Button(frame, text='Quit', command=self.plotQuit)
        self.quitButton.pack(side="left")
        
        # Initial dummy data
        field = 'Mood'
        name = self.pData['Patient Surname'][0] + ', ' + self.pData['Patient Firstname'][0]

        self.fig = Figure(figsize = (self.figWidth,self.figHeight))
        self.p = self.fig.add_subplot(111)
        
        # Populating with initial data
        self.p.plot(self.pData['Date'], self.pData[field])
        self.p.set_xlabel('Date', **self.figFont)
        self.p.set_ylabel('Score', **self.figFont)
        self.p.set_title(field + ' Scores for ' + name, **self.figFont)
        self.p.grid(True)

        # Showing figure on the tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

root = Tkinter.Tk()
app = App(root)
root.mainloop()