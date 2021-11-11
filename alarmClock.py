import tkinter as tk
from tkinter import StringVar, ttk
import time
from threading import Thread
from datetime import datetime
import os
import simpleaudio as sa

class AlarmClock(tk.Tk):

    def __init__(self):
        super().__init__()

        self.aMode = False

        # Creating window
        self.title('Alarm Clock')
        self.resizable(0, 0)
        self.geometry('250x150')
        self['bg'] = 'black'

        # Styling time label
        self.styleTimeLabel = ttk.Style(self)
        self.styleTimeLabel.configure(
            'TLabel',
            background = 'black',
            foreground = 'lightblue')

        # Styling [Set alarm] button
        self.styleAlarmButton = ttk.Style(self)
        self.styleAlarmButton.configure(
            'TButton',
            font=('Helvetica', 10),
            foreground = 'black')

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
            text='Set alarm', 
            command=lambda:Thread(target=self.alarmMode).start())

        # Placing button for starting timer
        self.button1.place(relx=0.09, rely=0.72)

        self.soundMenuOptions = ['Sound1', 'Sound2', 'Sound3']

        # Creating a drop down menu
        self.selectedAlarmSound = StringVar(self)
        self.alarmSoundMenu = ttk.OptionMenu(
            self, 
            self.selectedAlarmSound,
            self.soundMenuOptions[0],
            *self.soundMenuOptions,
            command=lambda x=None:self.getAlarmSound(self.selectedAlarmSound, self.soundMenuOptions)).place(relx=0.69, rely=0.72)

        # Calling an update every second
        self.label.after(1000, self.update)

        # Creating a thread for updating label and getting time
        self.newThread1 = Thread(target=self.update).start()
        self.newThread2 = Thread(target=self.getTime).start()
        self.newThread3 = lambda:Thread(target=self.getAlarmSound).start()

    def getTime(self):
        return time.strftime('%H:%M:%S')

    def update(self):
        self.label.configure(text=self.getTime())

        self.label.after(1000, self.update)

    def alarmMode(self):
        try:
            self.aMode = True

            hours = int(self.entryH.get())
            minutes = int(self.entryM.get())
            seconds = int(self.entryS.get())

            print('Entering alarm mode...')
            print('Alarm set at:', self.getTime())

            print(f'Alarm set for: {hours:02d}:{minutes:02d}:{seconds:02d}')

            while self.aMode == True:
                now = datetime.now().time()
                if now.hour == hours and now.minute == minutes and now.second == seconds:
                    print('Alarm noises')
                    self.getAlarmSound(self.selectedAlarmSound, self.soundMenuOptions)
                    self.aMode = False
        except ValueError:
            print('Unable to set alarm: No time entered.')

    def getAlarmSound(self, selectedAlarmSound, soundMenuOptions):
        # Paths for sound files
        alarmSound1Path = os.path.abspath('soundEffects\\alarmClockBeep.wav')
        alarmSound2Path = os.path.abspath('soundEffects\\alarmClockBeep2.wav')
        alarmSound3Path = os.path.abspath('soundEffects\\alarmClockBeep3.wav')

        alarmSound1 = sa.WaveObject.from_wave_file(alarmSound1Path)
        alarmSound2 = sa.WaveObject.from_wave_file(alarmSound2Path)
        alarmSound3 = sa.WaveObject.from_wave_file(alarmSound3Path)

        if selectedAlarmSound.get() == soundMenuOptions[0] and self.aMode == True:
            alarmSound1.play() # Playing alarm sound 1
        if selectedAlarmSound.get() == soundMenuOptions[1] and self.aMode == True:
            alarmSound2.play()
        if selectedAlarmSound.get() == soundMenuOptions[2] and self.aMode == True:
            alarmSound3.play()
        if self.aMode == False:
            if selectedAlarmSound.get() == soundMenuOptions[0]:
                print('Playing alarmSound1')
                alarmSound1.play()
            if selectedAlarmSound.get() == soundMenuOptions[1]:
                print('Playing alarmSound2')
                alarmSound2.play()
            if selectedAlarmSound.get() == soundMenuOptions[2]:
                print('Playing alarmSound3')
                alarmSound3.play()


if __name__ == "__main__":
    clock = AlarmClock()
    clock.mainloop()
