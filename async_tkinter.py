import asyncio
import tkinter as tk

class AsyncTk(tk.Tk):
	def __init__(self, *args, **kwds):
		self.loop = asyncio.get_running_loop()
		self.__running = False
		super().__init__(*args, **kwds)
	@property
	def running(self):
		return self.__running
	def destroy(self):
		self.__running = False
		return super().destroy()
	async def async_mainloop(self):
		self.__running = True
		try:
			while self.running:
				self.update()
				await asyncio.sleep(0)
		except asyncio.CancelledError:
			self.destroy()
