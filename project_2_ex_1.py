import itertools
from numpy import random
from datetime import datetime

import simpy


RANDOM_SEED = 42
NEW_PATIENTS = 5  # Total number of customers
SIM_TIME = 120



def source(env, number, process_1, cleaner_1):
    """Source generates customers randomly"""
    while True:
        p = patient(env, process_1, cleaner_1)
        env.process(p)
        t = random.exponential(scale=1)
        yield env.timeout(t)


def patient(env, process_1, cleaner_1):

	arrive = env.now

	print('patient admitted at ', env.now)

	with process_1.request() as req:
		
		process_1_timeout = random.triangular(.5, 1, 1.5)
		print(process_1_timeout)
		result = yield env.timeout(process_1_timeout)

	with cleaner_1.request() as req:
		print('Cleaner started at ', env.now)
		cleaning_person_timeout = random.triangular(.5,1,1.5)
		print(cleaning_person_timeout)
		yield env.timeout(cleaning_person_timeout)

		print('Cleaner done at ', env.now)



if __name__ == "__main__":
	env = simpy.Environment()
	process_1 = simpy.Resource(env, capacity=1)
	cleaner_1 = simpy.Resource(env, capacity=1)
	env.process(source(env, NEW_PATIENTS, process_1, cleaner_1))	
	env.run(until=SIM_TIME)
	
	
	