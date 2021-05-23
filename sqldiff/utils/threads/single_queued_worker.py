from abc import ABC, abstractmethod
from typing import Type

from PyQt5.QtCore import QThreadPool, QRunnable, QObject, pyqtSignal, pyqtSlot
import time

"""
Single Queued worker is a worker with predefined behaviour, 
which runs only one instance of worker at the same time.
It allows to set time delay between current and queued worker start.

If new request for the same worker is sent, and worker is in progress 
- new (only one) worker will be queued, and started after current worker finishes its job

If new request for the same worker is sent, and worker is not in progress 
- new worker will be started immediately. 

Main purpose of this type of worker is handling GUI highlighting in background,
for example when user scrolls through text editor fast,
and a lot of signals are sent. 
This will prevent GUI actions to be called too many times in classical queued approach.
"""


class SingleQueuedWorkerSignals(QObject):
    finished = pyqtSignal()


class SingleQueuedWorkerBase(QRunnable):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker_signals = SingleQueuedWorkerSignals()
        self.delay = 0

    @pyqtSlot()
    def run(self):
        time.sleep(self.delay)
        self.worker_action()
        self.worker_signals.finished.emit()

    @abstractmethod
    def worker_action(self):
        pass


class SingleQueuedWorkerGeneratorBase(ABC):
    @abstractmethod
    def generate_worker(self) -> SingleQueuedWorkerBase:
        pass


class SingleQueuedWorkerManager:

    def __init__(self, worker_generator: SingleQueuedWorkerGeneratorBase, queued_delay: float = 0):
        self.in_progress = False
        self.queued = False
        self.worker_generator = worker_generator
        self.queued_delay = queued_delay
        self.thread_pool = QThreadPool()
        self.worker = None

    def start(self):
        if self.in_progress:
            self.queued = True
            return
        delay = 0
        if self.queued:
            delay = self.queued_delay
            self.queued = False
        self.in_progress = True
        self.worker = self.worker_generator.generate_worker()
        self.worker.delay = delay
        self.worker.worker_signals.finished.connect(self.worker_finished)
        self.thread_pool.start(self.worker)

    def worker_finished(self):
        self.in_progress = False
        if self.queued:
            self.start()
