import multiprocessing
import threading


class Server:
    def __init__(self, name):
        self._name = name
        self._stop_flag = multiprocessing.Event()
        self._start_log_routine()

    def _start_log_routine(self):
        self._log_timer = threading.Timer(5, self._log_routine)
        self._log_timer.start()

    def _log_routine(self):
        pass

    def name(self):
        return self._name

    def stop(self):
        self._stop_flag.set()

    def release(self):
        self._log_timer.cancel()
