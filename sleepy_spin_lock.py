#!/usr/bin/env	python3
import time

"""
Sleepy Spin lock

contains one semaphore that is used
to determine condition for the sleep

wait_interruptible method:
	will wait for particular condition
	is not equal to semaphore + 1

wakeup_interruptible method:
	increment semaphore to wakeup_next thread
	that is calling wait_interruptibly

get_semaphore_state method:
	returns semaphore but not for
	our use.

"""
class sleepy_spin_lock:
	def __init__(self):

		# semaphore with initialize state
		self.semaphore = 0

	def wait_interruptible(self, condition):
		while self.semaphore+1 != condition:
			time.sleep(0.001)


	def wakeup_interruptible(self):
		self.semaphore += 1

	def get_semaphore_state(self):
		return self.semaphore
