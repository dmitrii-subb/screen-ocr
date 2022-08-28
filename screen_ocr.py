import pyautogui
import pyscreenshot
import pytesseract
import pyperclip as clipboard
from pystray import MenuItem as item
import pystray
from tkinter import *
from PIL import Image


class App(Frame):
    def __init__(self,window):

        self.tesseract_path = r'D:\Apps\Tesseract-OCR\tesseract.exe'

        Frame.__init__(self,window)
        self.window = window
        self.canvas_x = self.canvas_y = 0

        self.canvas = Canvas(self, width=1920, bd = 0, height=1080, cursor="cross")
        self.canvas.grid()
        self.canvas.bind("<ButtonPress-1>", self.on_left_mouse_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_mouse_button_release)
        self.window.bind("<Escape>", lambda x: self.window.destroy())

        self.rect = None

        self.canvas_start_x = 0
        self.canvas_start_y = 0

        self.screen_start_x = 0
        self.screen_start_y = 0

    def exit_window(self, icon, item):
        '''When exit button in taskbar pressed'''
        icon.stop()
        self.window.destroy()

    def run_window(self, icon, item):
        '''When run button in taskbar pressed'''
        icon.stop()
        self.window.after(0, self.window.deiconify())

    def on_left_mouse_button_press(self, event):
        self.canvas_start_x = self.canvas.canvasx(event.x)
        self.canvas_start_y = self.canvas.canvasy(event.y)
        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.canvas_x,
                self.canvas_y,
                1,
                1,
                outline='blue',
                width=2
            )

        self.screen_start_x, self.screen_start_y = pyautogui.position()

    def on_mouse_move(self, event):
        '''When mouse button is pressed and moving - draw rectangle'''
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        # expand rectangle as you drag the mouse
        self.canvas.coords(
            self.rect,
            self.canvas_start_x,
            self.canvas_start_y,
            curX,
            curY
        )

    def on_left_mouse_button_release(self, event):
        screen_stop_x, screen_stop_y = pyautogui.position()

        self.window.withdraw()

        if (self.screen_start_x >= screen_stop_x):
            self.screen_start_x, screen_stop_x = screen_stop_x, self.screen_start_x
        if (self.screen_start_y >= screen_stop_y):
            self.screen_start_y, screen_stop_y = screen_stop_y, self.screen_start_y

        img = pyscreenshot.grab(
            bbox = (
                self.screen_start_x,
                self.screen_start_y,
                screen_stop_x,
                screen_stop_y
            )
        )

        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
        text = pytesseract.image_to_string(img)

        clipboard.copy(text)
        self.hide_window_in_taskbar()

    def hide_window_in_taskbar(self):
        '''Hide the window and show on the system taskbar'''
        favicon=Image.open("favicon.ico")
        menu = ( item('Exit', self.exit_window), item('Run', self.run_window) )
        icon = pystray.Icon("name", favicon, "My System Tray Icon", menu)
        icon.run()


if __name__ == "__main__":

    window=Tk()
    window.attributes('-alpha',0.6)
    window.attributes('-fullscreen', True)

    app = App(window)
    app.pack()
    window.mainloop()
