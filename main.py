from tkinter import Tk
import sensor

class LightingControlSystem:
    def __init__(self, frame):
        self.frame = frame
        self.frame.title("Система управления освещением")
        self.frame.geometry("1100x700+450+100")
        self.frame.resizable(False, False)

if __name__ == "__main__":
    MainFrame = Tk()
    app = LightingControlSystem(MainFrame)
    MainFrame.mainloop()