import ui
from objc_util import *
import threading

class T(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		self.stop = threading.Event()
		
	def run(self):
		self.stop.wait()
		

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
	sender.superview.t.stop.set()
	
def is_running():

	if threading.active_count() > 1:
		return True, None
	
	t = T()
	t.start()
	
	return False, t
	
	
def main():
	
	r,t = is_running()
	if r:
		return

	v = ui.load_view('brightness')
	v.t = t
	
	import math
	
	s = v['slider']
	
	s.transform = ui.Transform().rotation(math.radians(-90))
	
	v.present('full_screen',
		hide_close_button=True,
		hide_title_bar=True,
		orientations=['portrait'])
		
	set_brightness_value(lambda x: x,v)
	
main()
