import asyncio
import tkinter as tk
from _tkinter import TclError

class AsyncTk(tk.Tk):
	def __init__(self, *args, **kwds):
		self.loop = asyncio.get_running_loop()
		self.__running = False
		super().__init__(*args, **kwds)
	@property
	def running(self):
		return self.__running
	async def async_mainloop(self):
		try:
			self.__running = True
			while True:
				self.update()
				await asyncio.sleep(0)
		except TclError:
			pass
		except asyncio.CancelledError:
			pass
		finally:
			self.__running = False