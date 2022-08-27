import pyautogui
import pyscreenshot
import pytesseract
import pyperclip as clipboard
from tkinter import *
from PIL import Image


class App(Frame):
    def __init__(self,window):

        Frame.__init__(self,window=None)
        self.window = window

        self.rec_text = 'None'
        self.path = StringVar()

        self.canvas_x = self.canvas_y = 0
        self.canvas = Canvas(self, width=1920, bd = 0, height=1080, cursor="cross")


        self.canvas.grid()
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.window.bind("<Escape>", lambda x: self.window.destroy())

        self.rect = None

        self.canvas_start_x = 0
        self.canvas_start_y = 0

        self.screen_start_x = 0
        self.screen_start_y = 0


    def on_button_press(self, event):
        # save mouse drag start position
        self.canvas_start_x = self.canvas.canvasx(event.x)
        self.canvas_start_y = self.canvas.canvasy(event.y)

        print('press: ', pyautogui.position())
        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.canvas_x, self.canvas_y, 1, 1, outline='red')

        self.screen_start_x, self.screen_start_y = pyautogui.position()


    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.canvas_start_x, self.canvas_start_y, curX, curY)


    def on_button_release(self, event):
        screen_stop_x, screen_stop_y = pyautogui.position()
        print('release: ', screen_stop_x, screen_stop_y)

        window.wm_state("iconic")

        if (self.screen_start_x >= screen_stop_x):
            self.screen_start_x, screen_stop_x = screen_stop_x, self.screen_start_x
        if (self.screen_start_y >= screen_stop_y):
            self.screen_start_y, screen_stop_y = screen_stop_y, self.screen_start_y

        img = pyscreenshot.grab(bbox = (self.screen_start_x, self.screen_start_y, screen_stop_x, screen_stop_y))
        window.wm_state("zoomed")

        img.save('screenshot.jpg')

        pytesseract.pytesseract.tesseract_cmd = r'D:\Apps\Tesseract-OCR\tesseract.exe'

        img = Image.open('screenshot.jpg')
        self.rec_text = pytesseract.image_to_string(img)
        print('recognized text:\n=====\n\n' + self.rec_text + '\n======')
        print('done')
        clipboard.copy(self.rec_text)
        self.window.destroy()


if __name__ == "__main__":

    window=Tk()
    window.geometry("1920x1080")
    window.attributes('-alpha',0.6)
    window.attributes('-fullscreen', True)

    app = App(window)
    app.pack()
    window.mainloop()
