import pyautogui
import mouse
import pyscreenshot
import time
import datetime
from tkinter import *
from PIL import Image
from io import BytesIO
import win32clipboard

import cv2
import pytesseract


# автоопределение расширения

 
def send_msg_to_clip(type_data, msg):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type_data, msg)
    win32clipboard.CloseClipboard()
 
 
def paste_img(file_img):
    image = Image.open(file_img)
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    send_msg_to_clip(win32clipboard.CF_DIB, data)
    

class App(Frame):
    
    def __init__(self,window):
        
        Frame.__init__(self,window=None)
        self.window = window

        self.rec_text = 'None'
        self.path = StringVar() 

        self.canvas_x = self.canvas_y = 0 
        self.canvas = Canvas(self, width=1920, bd = 0, height=1080, cursor="cross")

        settings_btn = Button(window, text='Settings', bg='#54FA9B', relief='flat', command=self.settings)
        settings_btn.place(x = 0, y = 0, width=150)

        recognized_text_btn = Button(window, text='Recognized text', bg='#54FA9B',relief='flat', command=self.recognized_text)
        recognized_text_btn.place(x = 200, y = 0, width=150)
        
        
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

    def save_path(self):
        self.path = self.path.get()
        print(self.path)

    def settings(self):
        settings_window = Toplevel(window)
        settings_window.geometry("400x600")
        settings_window.title('Settings')

        save_path_field = Entry(settings_window, text='save', textvariable=self.path)
        save_path_field.place(x=10, y=10)

        save_path_btn = Button(settings_window, text='save', command=self.save_path)
        save_path_btn.place(x=10, y=50)
        
        #save_path_field.pack()
        

    def recognized_text(self):
        recognized_text_window = Toplevel(window)
        recognized_text_window.geometry("400x600")
        recognized_text_window.title('Recognized text')
        text_field = Text(recognized_text_window, width=400, height=600, fg='black', wrap=WORD)
        text_field.insert(1.0, self.rec_text)
        text_field.pack()
        

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
        
        img.save(self.path+'\\lala.jpg')
        #paste_img('lala.jpg')
        
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        now = datetime.datetime.now()
        now = now.strftime("%d-%m-%y:%H-%M")

        img = cv2.imread(now)
        self.rec_text = pytesseract.image_to_string(img)
        print('recognized text:\n=====\n\n' + self.rec_text + '\n======')
        print('done')
        

if __name__ == "__main__":

    #import ctypes, sys
 
    #def is_admin():
    #    try:
    #        return ctypes.windll.shell32.IsUserAnAdmin()
    #    except:
    #        return False
 
    #if is_admin():
        window=Tk()
        window.geometry("1920x1080")
        window.attributes('-alpha',0.6)
        window.attributes('-fullscreen', True)

        app = App(window)
        app.pack()
        window.mainloop()
    #else:
        # Re-run the program with admin rights
    #    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    #    window=Tk()
    #    window.geometry("1920x1080")
    #    window.attributes('-alpha',0.6)
    #    window.attributes('-fullscreen', True)

    #    app = App(window)
    #    app.pack()
    #    window.mainloop()
    


    
