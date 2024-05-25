import win32api,  win32con, win32gui, winsound, os
from PIL import Image, ImageSequence

def display_gif_with_sound(gif_path, sound_path):
    try:
        win32api.ShowCursor(False)
        gif = Image.open(gif_path)
        frames = [frame.copy().convert('RGB') for frame in ImageSequence.Iterator(gif)]
        width, height = frames[0].size
        
        # make window
        hwnd = win32gui.FindWindow(None, "GIF Window")
        if not hwnd:
            win32gui.InitCommonControls()
            hwnd = win32gui.CreateWindow("STATIC", "Mario.exe", win32con.WS_VISIBLE | win32con.WS_OVERLAPPEDWINDOW,
                                         100, 100, width, height, None, None, None, None)
        
        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        
        for frame in frames:
            frame.save('temp.bmp')
            dib = Image.open('temp.bmp')
            dib.save('temp.bmp', quality=95)
            
            hdc = win32gui.GetDC(hwnd)
            memdc = win32gui.CreateCompatibleDC(hdc)
            bmp = win32gui.LoadImage(0, 'temp.bmp', win32con.IMAGE_BITMAP, 0, 0, win32con.LR_LOADFROMFILE)
            win32gui.SelectObject(memdc, bmp)
            win32gui.StretchBlt(hdc, 0, 0, width, height, memdc, 0, 0, width, height, win32con.SRCCOPY)

            win32gui.DeleteObject(bmp)
            win32gui.DeleteDC(memdc)
            win32gui.ReleaseDC(hwnd, hdc)

            win32api.Sleep(7)
    except Exception as e:
        print(e)

display_gif_with_sound("https://github.com/nfwebapi/mario-virus-python/blob/main/example.gif", "https://github.com/nfwebapi/mario-virus-python/blob/main/example.wav")
