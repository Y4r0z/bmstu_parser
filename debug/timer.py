
import time
import logging as log

class Timer:
    def __init__(self, name = None) -> None:
        self.name = name
        self.start = time.time()
        self.current = self.start
        self.marks = []
    
    def clear(self):
        self.start = time.time()
        self.current = self.start
    
    def mark(self):
        dif = time.time() - self.current
        self.current = time.time()
        self.marks.append(dif)
    
    def print(self):
        self.mark()
        print(f"------ Timer {self.name}------\n" +
        f"Marks count: {len(self.marks)};\n" +
        "--- Marks:")
        for i in self.marks:
            print(i)
        print(f"--- Total:\n{self.current - self.start}")
    
    def log(self):
        self.mark()
        log.debug(f"------ Timer {self.name}------\n" +
        f"Marks count: {len(self.marks)};\n" +
        "--- Marks:")
        for i in self.marks:
            log.debug(str(i))
        log.debug(f"--- Total:\n{self.current - self.start}")