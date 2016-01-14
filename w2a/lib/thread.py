import threading
import inspect
import ctypes


def _async_raise(tid, exctype, name):
	"""raises the exception, performs cleanup if needed"""
	if not inspect.isclass(exctype):
		raise TypeError("Only types can be raised (not instances)")
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble, 
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
		raise SystemError("PyThreadState_SetAsyncExc failed")
	if name != None:
		print('Killed thread name : ' + name)
	else:
		print('Killed thread Id: ' + tid)
class Thread(threading.Thread):
	def __init__(self, *args, **kwargs):
		threading.Thread.__init__(self, *args, **kwargs)
		self.daemon		= True
		self._return	= None
		self.name		= 'Unknown'
	def run(self):
		try:
			if self._target:
				self._return = self._target(*self._args, **self._kwargs)
		finally:
			# Avoid a refcycle if the thread is running a function with
			# an argument that has a member that points to the thread.
			del self._target, self._args, self._kwargs

	def _get_my_tid(self):
		"""determines this (self's) thread id"""
		if not self.isAlive():
			raise threading.ThreadError("the thread is not active")
		
		# do we have it cached?
		if hasattr(self, "_thread_id"):
			return self._thread_id
		
		# no, look for it in the _active dict
		for tid, tobj in threading._active.items():
			if tobj is self:
				self._thread_id = tid
				return tid
		
		raise AssertionError("could not determine the thread's id")
	
	def raise_exc(self, exctype):
		"""raises the given exception type in the context of this thread"""
		_async_raise(self._get_my_tid(), exctype, self.name)
	
	def terminate(self):
		"""raises SystemExit in the context of the given thread, which should 
		cause the thread to exit silently (unless caught)"""
		self.raise_exc(SystemExit)
	def join(self, *argc, **argv):
		try:
			threading.Thread.join(self, *argc, **argv)
			return self._return
		except KeyboardInterrupt:
			self.terminate()
			