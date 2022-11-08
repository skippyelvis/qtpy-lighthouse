import time
from neopixel import NeoPixel
import board
from digitalio import DigitalInOut as DIN, Direction, Pull
from adafruit_led_animation import color as C

class Timer:

	def __init__(self, chime):
		self.chime = chime
		self.last = time.monotonic()

	def check(self):
		now = time.monotonic()
		res = False
		if (now - self.last) <= self.chime:
			res = True
		self.last = time.monotonic()
		return res


class Display:

	def __init__(self, phase):
		self.pix = NeoPixel(board.A0, 8, brightness=0.75, auto_write=False)
		self.cmap = phase[0]
		self.pos = 0
		self.n = 0
		self.delta = phase[1]

	def step(self):
		self.pos += 1
		if isinstance(self.cmap, list):
			self.pos = self.pos % len(self.cmap)
			return self.cmap[self.pos]
		elif callable(self.cmap):
			return self.cmap(self.pos)

	def change_display(self, phase):
		self.cmap = phase[0]
		self.delta = phase[1]

	def step_display(self):
		self.n = (self.n + 1) % self.delta
		if self.n != 0:
			return
		cmap = self.step()
		for i, c in enumerate(cmap):
			self.pix[i] = c
		self.pix.show()

p0_display = ([
	[C.RED, C.YELLOW, C.RED, C.YELLOW, C.RED, C.YELLOW, C.RED, C.YELLOW],
	[C.YELLOW, C.RED, C.YELLOW, C.RED, C.YELLOW, C.RED, C.YELLOW, C.RED],
], 5)

p1_display = ([
	[C.BLUE, C.PURPLE, C.BLUE, C.PURPLE, C.BLUE, C.PURPLE, C.BLUE, C.PURPLE],
	[C.PURPLE, C.BLUE, C.PURPLE, C.BLUE, C.PURPLE, C.BLUE, C.PURPLE, C.BLUE],
], 10)

p2_display = ([
	[C.YELLOW, C.YELLOW, C.YELLOW, C.BLUE, C.BLUE, C.YELLOW, C.YELLOW, C.YELLOW],
	[C.BLUE, C.BLUE, C.BLUE, C.YELLOW, C.YELLOW, C.BLUE, C.BLUE, C.BLUE], 
], 20)

p3_display = ([
	[C.OLD_LACE] * 8,
	[C.MAGENTA] * 8,
], 50)

blank_display = ([
	[(0,0,0)] * 8,
], 1)

displays = [p0_display, p1_display, p2_display, p3_display]

phase = 0
nphase = len(displays)

if __name__ == "__main__":
	sw = DIN(board.A1)
	disp = Display(displays[0]) 
	timer = Timer(.3)
	sw.switch_to_input(pull=Pull.UP)
	prev = True
	on = True
	while True:
		time.sleep(0.025)
		if not sw.value and prev != sw.value:
			if timer.check():
				on = not on
			if not on:
				disp.change_display(blank_display)
			else:
				phase = (phase + 1) % nphase
				disp.change_display(displays[phase])
		prev = sw.value
		disp.step_display()
	
