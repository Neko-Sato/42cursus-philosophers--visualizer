#!/usr/bin/python3
import argparse
import asyncio
import os, sys
import tkinter as tk
import async_tkinter as atk
import math
from enum import Enum
import struct

PATH = "/tmp/philo_visualizer.pipe"

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
	async def start(self, reader:asyncio.StreamReader):
		while self.running:
			try:
				data = await reader.readexactly(8)
			except asyncio.IncompleteReadError:
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
				self.change_forkstate(philo, True, 1)
			elif action == 0b0101:
				self.change_forkstate(philo, False, 1)
			elif action == 0b0110:
				self.change_forkstate(philo, True, -1)
			elif action == 0b0111:
				self.change_forkstate(philo, False, -1)
			# await asyncio.sleep(0.01)

async def main(args:argparse.Namespace):
	if not os.access(args.pipe, os.F_OK):
		os.mkfifo(args.pipe)
	app = PhiloVisualizer(width=args.width, height=args.height)
	loop = asyncio.get_running_loop()
	philo = await asyncio.create_subprocess_exec(*args.philo_argv)
	sync_reader = open(args.pipe, "rb", buffering=0)
	reader = asyncio.StreamReader()
	transport, _ = await loop.connect_read_pipe(
		lambda: asyncio.StreamReaderProtocol(reader), sync_reader)
	task = asyncio.create_task(app.start(reader))
	await app.async_mainloop()
	task.cancel()
	transport.close()
	sync_reader.close()
	try:
		philo.terminate()
		await philo.wait()
	except ProcessLookupError:
		pass

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("philo_argv", nargs="+", type=str)
	parser.add_argument("--width", type=int, default=500)
	parser.add_argument("--height", type=int, default=500)
	parser.add_argument("--pipe", type=str, default=PATH)
	asyncio.run(main(parser.parse_args()))