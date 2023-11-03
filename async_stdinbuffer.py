import asyncio
import sys

async def async_stdinbuffer():
	loop = asyncio.get_event_loop()
	reader = asyncio.StreamReader()
	protocol = asyncio.StreamReaderProtocol(reader)
	await loop.connect_read_pipe(lambda: protocol, sys.stdin.buffer)
	return reader
