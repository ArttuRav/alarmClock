import tkinter as tk
from tkinter import ttk
import time
from threading import Thread
from datetime import datetime
import simpleaudio as sa

class AlarmClock(tk.Tk):

    def __init__(self):
        super().__init__()

        # Path for sound file
        myPath = r'C:/Users/arttu/OneDrive - Turun ammattikorkeakoulu/Python/soundEffects/alarmClockBeep.wav'
        self.alarmSound = sa.WaveObject.from_wave_file(myPath)

        self.aMode = False

        # Creating window
        self.title('Alarm Clock')
        self.resizable(0, 0)
        self.geometry('250x150')
        self['bg'] = 'black'

        # Styling label
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background = 'black',
            foreground = 'lightblue')

        # Creating label
        self.label = ttk.Label(
            self,
            text=self.getTime(),
            font = ('Digital-7', 40))

        self.label.place(x=20, y=10)

        # Creating entries for entering time
        self.entryH = ttk.Entry(
            self,
            width='8')
        self.entryM = ttk.Entry(
            self,
            width='8')
        self.entryS = ttk.Entry(
            self,
            width='8')

        # Placing entries
        self.entryH.place(relx=0.09, rely=0.47)
        self.entryM.place(relx=0.39, rely=0.47)
        self.entryS.place(relx=0.69, rely=0.47)

        # Creating a button to start timer with
        self.button1 = ttk.Button(
            self,
            text='SET ALARM', 
            command=lambda:Thread(target=self.alarmMode).start())

        # Placing button for starting timer
        self.button1.place(relx=0.09, rely=0.72)

        # Calling an update every second
        self.label.after(1000, self.update)

        # Creating a thread for updating label and getting time
        self.newThread1 = Thread(target=self.update).start()
        self.newThread2 = Thread(target=self.getTime).start()

    def getTime(self):
        return time.strftime('%H:%M:%S')

    def update(self):
        self.label.configure(text=self.getTime())

        self.label.after(1000, self.update)

    def alarmMode(self):
        print('Entering alarm mode...')
        print('Alarm set at:', self.getTime())

        self.aMode = True

        hours = int(self.entryH.get())
        minutes = int(self.entryM.get())
        seconds = int(self.entryS.get())

        print(f'Alarm set for {hours:02d}:{minutes:02d}:{seconds:02d}')

        while self.aMode == True:
            now = datetime.now().time()
            if now.hour == hours and now.minute == minutes and now.second == seconds:
                self.aMode = False
                print('Alarm noises')
                self.playSound = self.alarmSound.play()
                self.playSound.wait_done()
                

if __name__ == "__main__":
    clock = AlarmClock()
    clock.mainloop()
