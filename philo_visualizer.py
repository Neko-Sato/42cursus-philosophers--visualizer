#!/usr/bin/python3
import asyncio
from typing import IO
from functools import wraps
import os, sys
import tkinter as tk
import async_tkinter as atk
import math
from enum import Enum
import struct

PATH = "/tmp/philo_visualizer.pipe"

@wraps(open)
async def async_open(*args, **kwds):
	opener = kwds.pop("opener") if "opener" in kwds else os.open
	kwds["opener"] = lambda path, flags: opener(path, flags | os.O_NONBLOCK)
	while True:
		try:
			fd = open(*args, **kwds)
			break
		except OSError as e:
			if e.errno != 6:
				raise
		await asyncio.sleep(0)
	return fd

async def async_read_bytes(fd:IO, n:int):
	try:
		data = b''
		while n < 0 or len(data) < n:
			chank = fd.read(-1 if n < 0 else n - len(data))
			if chank:
				data += chank
			await asyncio.sleep(0)
	except ValueError:
		if not n < 0:
			return None
	return data

def calc_pos_and_angle(width, height, n, p):
	x = width/2*(1+n*math.sin(2*math.pi*p))
	y = height/2*(1-n*math.cos(2*math.pi*p))
	angle = -360*p
	return x, y, angle

class PhiloState(Enum):
	THINKING = 0
	EATING = 1
	SLEEPING = 2
	DIED = -1

class PhiloVisualizer(atk.AsyncTk):
	font = (None, 18)
	def __init__(self, width=500, height=500):
		super().__init__()
		self.title("PhiloVisualizer")
		self.width, self.height = width, height
		self.geometry(f"{self.width}x{self.height}")
		self.len = 0
		self.philo = []
		self.fork = []
		self.build()
	def build(self):
		self.canvas = tk.Canvas(self, width=self.width, height=self.height)
		self.canvas.pack()
	def init(self, len:int):
		self.canvas.delete("all")
		self.philo.clear()
		self.fork.clear()
		self.len = len
		for i in range(self.len):
			x, y, angle = calc_pos_and_angle(self.width, self.height, 0.95, i/self.len)
			item = self.canvas.create_text(x, y, text="●", angle=angle, font=self.font)
			self.philo.append(item)
		for i in range(self.len):
			x, y, angle = calc_pos_and_angle(self.width, self.height, 0.8, (i+0.5)/self.len)
			item = self.canvas.create_text(x, y, text="|", angle=angle, font=self.font)
			self.fork.append(item)
	def change_philostate(self, philo:int, state:PhiloState):
		color = {
			PhiloState.THINKING: "black",
			PhiloState.EATING: "green", 
			PhiloState.SLEEPING: "blue", 
			PhiloState.DIED: "red"
			}[state]
		self.canvas.itemconfig(self.philo[philo], fill=color)
	def change_forkstate(self, philo:int, istake:bool, lr:int):
		fork = (philo + (-1 if lr < 0 else 0)) % self.len
		fork_pos = fork + 0.5
		if istake:
			fork_pos += 0.4 * (1 if lr < 0 else -1)
		x, y, angle = calc_pos_and_angle(
			self.width, self.height, 0.9 if istake else 0.8, fork_pos/self.len)
		self.canvas.coords(self.fork[fork], x, y)
		self.canvas.itemconfig(self.fork[fork],angle=angle)
	async def start(self, reader:IO):
		while self.running:
			data = await async_read_bytes(reader, 8)
			if not data:
				break
			philo, action = struct.unpack("II", data)
			if action & 0b1000:
				self.init(philo)
				continue
			philo -= 1
			if action == 0b0000:
				self.change_philostate(philo, PhiloState.THINKING)
			elif action == 0b0001:
				self.change_philostate(philo, PhiloState.EATING)
			elif action == 0b0010:
				self.change_philostate(philo, PhiloState.SLEEPING)
			elif action == 0b0011:
				self.change_philostate(philo, PhiloState.DIED)
			elif action == 0b0100:
				self.change_forkstate(philo, True, -1)
			elif action == 0b0101:
				self.change_forkstate(philo, False, -1)
			elif action == 0b0110:
				self.change_forkstate(philo, True, 1)
			elif action == 0b0111:
				self.change_forkstate(philo, False, 1)
			# await asyncio.sleep(0.01)

async def main(path):
	if not os.access(PATH, os.F_OK):
		os.mkfifo(PATH)
	await asyncio.create_subprocess_exec(*sys.argv[1:])
	app = PhiloVisualizer()
	with await async_open(path, "rb", buffering=0) as reader:
		task = asyncio.create_task(app.start(reader))
		await app.async_mainloop()
		task.cancel()

if __name__ == "__main__":
	asyncio.run(main(PATH))
	