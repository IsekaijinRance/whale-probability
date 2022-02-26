import random

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

def main():
    number_of_iterations = 1000

    ### Print the problem statement
    print(
    '''
    Suppose you have two whales
    You know that at least one of them is a male whales

    What is the probability that both whales are male?
    '''
    )

    ### Activating single threaded mode.
    print(f"Using a single thread to run a simulation to calculate {number_of_iterations} pairs of whales.")    
    result = calculateWhaleCombinations(number_of_iterations, 0)

    ###Finished computing so print the result of the data.
    print(f'Finished computing {number_of_iterations} pair of whales and these are the results:')
    for p in result:
        print(f"{p} pair: \t {result[p]} \t ({round(result[p]/number_of_iterations*100, 2)}%)")
    print('')

##! END OF def main():

if __name__ == "__main__":
    main()
    