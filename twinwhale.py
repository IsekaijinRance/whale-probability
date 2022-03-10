import math
import random
import time

import argparse
from multiprocessing import cpu_count, Pool

SINGLE_THREAD_THRESHOLD = 75000

def rollWhale():
    return "male" if (random.randint(1,100) % 2 == 0) else "female" 

def calculateWhaleCombinations(number_of_times, mode = 0):

    if number_of_times <= 0:
        return None

    results = {
        "male-male" : 0,
        "male-female": 0,
        "female-male": 0
    }
    order_roll = mode
    
    for i in range(number_of_times):
        if mode == 0:
            order_roll = (random.randint(1,100)% 2) + 1

        if order_roll == 1:
            results["male-" + rollWhale()] += 1

        if order_roll == 2:
            results[rollWhale() + "-male"] += 1

    return results

##! END OF calculateWhaleCombinations(number_of_times, mode = 0):

def main(iterations, single_thread, mode):

    ### Print the problem statement
    print(
    '''
    Suppose you have two whales
    You know that at least one of them is a male whales

    What is the probability that both whales are male?
    '''
    )

    result = {}

    ### Activating singlethreaded mode.
    if single_thread:
        print(f"Using a single thread to run the simulation with a sample size of {iterations} pairs of whales.") 
        timer_start = time.time_ns()
        result = calculateWhaleCombinations(iterations, mode)
    
    ### Activating multithreaded mode.
    else:
        print(f"Found {cpu_count()} cpu units to run the simulation with a sample size of {iterations} pairs of whales.")
        timer_start = time.time_ns()
        ### Determine how to spread the number of iterations between cores taking into account when the user inputs an uneven ammount to the number of cpu units available.
        pn = math.floor(iterations / cpu_count())
        pool_args=[]

        pool_args.append(
            (pn + (iterations % cpu_count()), mode,)
            )
        
        pool_args.extend(
            [(pn,mode,)] * (cpu_count()-1)
            )

        with Pool() as pool:
            mp_result = pool.starmap(calculateWhaleCombinations, pool_args)

            for pool_result in mp_result:
                for key in pool_result:
                    if key in result:
                        result[key] += pool_result[key]
                    else:
                        result[key] = pool_result[key]

    ###Finished computing 
    timer_end=time.time_ns()
    run_time = (timer_end - timer_start) / 1000000000

    ### print the result of the data.
    print(f'Finished computing {iterations} pair of whales in {run_time} seconds.')
    print('These are the results:')
    for p in result:
        print(f"{p} pair: \t {result[p]} \t ({round(result[p]/iterations*100, 2)}%)")
    print('')

##! END OF def main():

if __name__ == "__main__":
    ### Setup command line arguments
    cmdparser = argparse.ArgumentParser(description='Run a simulation of a probability problem involving pairs of whales.')

    cmdparser.add_argument('-s', '--sample-size', type=int, help='Determine the ammount of pairs to be calculated for the simulation.', default=SINGLE_THREAD_THRESHOLD)

    cmdparser.add_argument('-d', '--draw-order', type=int, choices=[0,1,2], default=0, help=
    '''
    Determine the order by which the pair are drawn. 
    Setting it to 1 will make the confirmed male is always the first draw. 
    Setting it to 2 will make it the second draw.
    Default is 0 which will randomly alternate between 1st and 2nd draw.
    ''')

    cmdparser.add_argument('--single-thread', action='store_true', help='Force this simulation to run on a single thread.')

    args = cmdparser.parse_args()
    main(args.sample_size, args.single_thread, args.draw_order)
    