import ui
from objc_util import *

class Updater(ui.View):
	def __init__(self):
		self.update_interval = 1.0

	def update(self):
		v = self.superview
		set_brightness_value(
			lambda x:x,v)

def set_brightness(x,v):
	
	b = v['brightness']
	b.text = str(
		round(x * 100, 1))
	
	s = v['slider']
	s.value = x
	

def set_brightness_value(f,v):
	
	scr = ObjCClass('UIScreen').mainScreen()
	
	b = scr.brightness()
	b = f(b)
	
	scr.setBrightness(b)
	set_brightness(b,v)
	

def slider(sender):
	b = float(sender.value)
	f = lambda x: b
	set_brightness_value(f,sender.superview)
	
	
def max(sender):
	b = float(sender.title)/100.0
	f = lambda x: b
	set_brightness_value(f,sender.superview)
	

def plus(sender):
	f = lambda x: x + 0.003
	set_brightness_value(f,sender.superview)
	
	
def minus(sender):
	f = lambda x: x - 0.003
	set_brightness_value(f,sender.superview)
	
def close(sender):
	sender.superview.close()
	sender.superview.socket.close()
	
def is_running():
	
	import socket 
	s = socket.socket(socket.AF_INET,
		socket.SOCK_STREAM)
	
	try:
		
		s.bind(('localhost', 8888))
		return False, s
		
	except Exception as ex:
		return True, None
	
def main():
	
	r, s = is_running()
	if r:
		return

	v = ui.load_view('brightness')
	v.socket = s
	
	import math
	
	s = v['slider']
	
	s.transform = ui.Transform().rotation(math.radians(-90))
	
	v.present('full_screen',
		hide_close_button=True,
		hide_title_bar=True,
		orientations=['portrait'])
		
	set_brightness_value(lambda x: x,v)
	
main()