# MyThreadPool Class
This Class has been created as a Pool example for Threading excercice in Python. 
MyThreadPool inherits from ThreaPool class by adding Lock() usage. 

## Python version
Python version 3.10

## How to import it?
```py
	from MyThreadPool import ThreadPool as MyThreadPoolClass
```

## And what next?
Once imported, you are free to use it by simply declaring a 'pool' somewhere else in your main, like follows:
```py
	my_pool = MyThreadPoolClass()
```
Now that it has been declared, it can be passed to any new Thread as a parameter
```py
	t = Thread(target=function_to_execute, name=f"Thread{i}", args=(semaphore, pool))
```
And inside the targeted function, just call the "activate" function when the thread is about to start executing and call the "deactivate" function accordingly once it is over.
```py
def function_to_execute(semaphore, pool):
	pool.activate(current_thread().name)
	# Do your stuff here
	pool.deactivate(current_thread().name)
```