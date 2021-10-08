import time
import threading
import random

def philosopher_create(name=0):
   p = {
           'left_chopstick': threading.Event(),
           'right_chopstick': threading.Event(),
           'left_philosopher': None,
           'right_philosopher': None,
           'name': name,
           'num_eats': 0,
   }
   return p


def philosophize(philosopher, max_num_eats=5):
    while philosopher['num_eats'] < max_num_eats:
        print(f'Philosopher {philosopher["name"]} is thinking...')
        time.sleep(random.randint(1, 3))
        
        # See if left philosopher holds chopstick.
        if philosopher['left_philosopher']['right_chopstick'].is_set():
            continue
        
        # Pick up chopstick and see if other chopstick is available.
        philosopher['left_chopstick'].set()
        print(f'Philosopher {philosopher["name"]} picked up left chopstick...')

        if philosopher['right_philosopher']['left_chopstick'].is_set():
            
            print(f'Philosopher {philosopher["name"]} put down left chopstick...')
            philosopher['left_chopstick'].clear()
            continue
        
        philosopher['right_chopstick'].set()
        print(f'Philosopher {philosopher["name"]} picked up left chopstick...')
        
        philosopher['num_eats'] += 1
        print(f'Philosopher {philosopher["name"]} is eating: {philosopher["num_eats"]}...')
        time.sleep(random.randint(1,3))
            
        print(f'Philosopher {philosopher["name"]} put down left chopstick...')
        philosopher['left_chopstick'].clear()

        print(f'Philosopher {philosopher["name"]} put down right chopstick...')
        philosopher['right_chopstick'].clear()

philosophers = [philosopher_create(i) for i in range(1, 6)]

for p1, p2 in zip(philosophers, philosophers[1:]):
    p1['right_philosopher'] = p2
    p2['left_philosopher'] = p1

philosophers[0]['left_philosopher'] = philosophers[-1]
philosophers[-1]['right_philosopher'] = philosophers[0]

threads = [threading.Thread(target=philosophize, args=(p,)) for p in philosophers]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print('All philosophers finished eating!')
