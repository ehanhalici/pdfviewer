#!/usr/bin/env python
from time import sleep
import pyperclip
from pynput.mouse import Listener
import pyautogui

pano = ""
temp = ""
dosya = open('./sözcükler',"a+")
dosya.seek(0)
sözcükler = dosya.read().splitlines()
#print(sözcükler)
click = 0 

print("program calisiyor")
pyperclip.copy("")  

def main():
	global pano, temp
	pyautogui.hotkey('ctrl', 'c')
	temp = pyperclip.paste()
	işle()
	if temp == "" or temp == " ":
		return
	if temp != pano:
		pano = temp
		#rewrite
		pyperclip.copy(pano)

		if pano not in sözcükler:
			dosyaYaz()

def işle():
	global temp
	temp = temp.lower()
	for i in [".",",",":",";"]:
		if temp.find(i) == len(temp) - 1:
			temp = temp[:len(temp)-1]

def dosyaYaz():
	global dosya, pano

	dosya.write(pano)
	dosya.write('\n')
	dosya.flush()



def on_click(x, y, button, pressed):
	global click, pano, temp
	try:
		click = click + 1
		if click == 2:
			click = 0
			main()
	except:
	   pass

with Listener(on_click=on_click) as listener:
	listener.join()