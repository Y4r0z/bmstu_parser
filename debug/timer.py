
import time
import logging as log

class Timer:
    def __init__(self) -> None:
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
        print("------ Timer ------\n" +
        f"Marks count: {len(self.marks)};\n" +
        "--- Marks:")
        for i in self.marks:
            print(i)
        print(f"--- Total:\n{self.current - self.start}")