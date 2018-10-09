from objc_util import *
scr = ObjCClass('UIScreen').mainScreen()

import appex, ui
import socket
import time

class Info(ui.View):
	
	def update_b(self):
		
		b = round(scr.brightness()*100)
		self.label.text = f'{b}%'		
	
	def __init__(self):
		
		self.frame = (0,0,350,110)
		
		self.label = ui.Label(
			font=('Menlo', 24), alignment=ui.ALIGN_CENTER,
			frame=self.frame)
		
		self.update_b()		
		
		self.add_subview(self.label)
		self.update_interval = 1.0
		
	def update(self):
		self.update_b()
	
def main():
		
	v = Info()
	appex.set_widget_view(v)
	
if __name__ == '__main__':
	main()
	
