import threading
import time
import random


class Tram:
    def __init__(self, capacity, num_stops):
        self.capacity = capacity
        self.num_stops = num_stops
        self.current_stop = 0
        self.passengers = []
        self.mutex = threading.Lock()
        self.all_aboard = threading.Condition(self.mutex)

    def load(self):
        with self.mutex:
            while len(self.passengers) < self.capacity:
                passenger = Passenger()
                self.passengers.append(passenger)
                passenger.start()
                print(f"Пасажир {passenger.id} сідає в трамвай на зупинці {self.current_stop}")
            self.all_aboard.notify_all()
            
    def unload(self):
        with self.mutex:
            while self.passengers:
                passenger = self.passengers.pop()
                print(f"Пасажир {passenger.id} виходить з трамвая на зупинці {self.current_stop}")
            
    def move(self):
        while True:
            time.sleep(1)
            print(f"Трамвай від’їжджає від зупинки {self.current_stop}")
            self.current_stop = (self.current_stop + 1) % self.num_stops
            if self.current_stop == 0:
                print("Трамвай повертається на першу зупинку")
            self.unload()
            self.load()
            time.sleep(1)


class Passenger(threading.Thread):
    _id = 1
    def __init__(self):
        super().__init__()
        self.id = Passenger._id
        Passenger._id += 1
        
    def run(self):
        with tram.all_aboard:
            while self not in tram.passengers:
                tram.all_aboard.wait()


if __name__ == "__main__":
    capacity = 5
    num_stops = 3

    tram = Tram(capacity, num_stops)

    move_thread = threading.Thread(target=tram.move)
    move_thread.start()

    move_thread.join()