import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import json
import argparse
import numpy as np


exp_result = {
    "avg_latency_lookup_cache_p00": 0.07244290709495544,
    "avg_latency_lookup_cache_p02": 0.07903057670593262,
    "avg_latency_lookup_cache_p04": 0.08399424242973328,
    "avg_latency_lookup_cache_p06": 0.08761160516738892,
    "avg_latency_lookup_cache_p08": 0.09170633792877198,
    "avg_latency_order_cache_p00": np.nan, 
    "avg_latency_order_cache_p02": 0.0984061967979357, 
    "avg_latency_order_cache_p04": 0.12781917689759055, 
    "avg_latency_order_cache_p06": 0.15927220608492856, 
    "avg_latency_order_cache_p08": 0.20216920611299113, 
    "avg_latency_lookup_nocache_p00": 0.07677148365974426,
    "avg_latency_lookup_nocache_p02": 0.08131726312637329,
    "avg_latency_lookup_nocache_p04": 0.08510809111595153,
    "avg_latency_lookup_nocache_p06": 0.09088663458824158,
    "avg_latency_lookup_nocache_p08": 0.09559101414680481,
    "avg_latency_order_nocache_p00": np.nan, 
    "avg_latency_order_nocache_p02": 0.14739101025664691,
    "avg_latency_order_nocache_p04": 0.15510660704999868,
    "avg_latency_order_nocache_p06": 0.16628563336681887,
    "avg_latency_order_nocache_p08": 0.23437943805882961
}


def list_avg(_list):
    return sum(_list) / len(_list)

def main(args):
    # Maximun number of clients
    x_range = 5

    # Change the probability p from 0 to 80%, both lookup and order
    if args.type == "caching":
        lookup_latency = []
        order_latency = []
        for p in ["00", "02", "04", "06", "08"]:
            lookup_latency.append(exp_result[f"avg_latency_lookup_cache_p{p}"])
            order_latency.append(exp_result[f"avg_latency_order_cache_p{p}"])
        x_label = [0.0, 0.2, 0.4, 0.6, 0.8]
        # Plot the figure
        fig, ax = plt.subplots()
        plt.xlabel('Probability')
        plt.ylabel('Average response time (s) per request')
        plt.xticks(list(range(1, x_range+1)), x_label)
        ax.plot(list(range(1, x_range+1)), lookup_latency, label="Lookup")
        ax.plot(list(range(1, x_range+1)), order_latency, label="Order")
        ax.set_title('Average Latency with Caching')
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.grid(which='minor', linewidth=0.6)
        ax.legend()
        
        plt.show()
    
    elif args.type == "nocaching":
        lookup_latency = []
        order_latency = []
        for p in ["00", "02", "04", "06", "08"]:
            lookup_latency.append(exp_result[f"avg_latency_lookup_nocache_p{p}"])
            order_latency.append(exp_result[f"avg_latency_order_nocache_p{p}"])
        x_label = [0.0, 0.2, 0.4, 0.6, 0.8]
        # Plot the figure
        fig, ax = plt.subplots()
        plt.xlabel('Probability')
        plt.ylabel('Average response time (s) per request')
        plt.xticks(list(range(1, x_range+1)), x_label)
        ax.plot(list(range(1, x_range+1)), lookup_latency, label="Lookup")
        ax.plot(list(range(1, x_range+1)), order_latency, label="Order")
        ax.set_title('Average Latency without Caching')
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.grid(which='minor', linewidth=0.6)
        ax.legend()
        
        plt.show()

    elif args.type == "lookup":
        lookup_latency_cache = []
        lookup_latency_nocache = []
        for p in ["00", "02", "04", "06", "08"]:
            lookup_latency_cache.append(exp_result[f"avg_latency_lookup_cache_p{p}"])
            lookup_latency_nocache.append(exp_result[f"avg_latency_lookup_nocache_p{p}"])
        x_label = [0.0, 0.2, 0.4, 0.6, 0.8]
        # Plot the figure
        fig, ax = plt.subplots()
        plt.xlabel('Probability')
        plt.ylabel('Average response time (s) per request')
        plt.xticks(list(range(1, x_range+1)), x_label)
        ax.plot(list(range(1, x_range+1)), lookup_latency_cache, label="w/ caching")
        ax.plot(list(range(1, x_range+1)), lookup_latency_nocache, label="w/o caching")
        ax.set_title('Effectiveness of Caching')
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.grid(which='minor', linewidth=0.6)
        ax.legend()
        
        plt.show()

    elif args.type == "order":
        order_latency_cache = []
        order_latency_nocache = []
        for p in ["00", "02", "04", "06", "08"]:
            order_latency_cache.append(exp_result[f"avg_latency_order_cache_p{p}"])
            order_latency_nocache.append(exp_result[f"avg_latency_order_nocache_p{p}"])
        x_label = [0.0, 0.2, 0.4, 0.6, 0.8]
        # Plot the figure
        fig, ax = plt.subplots()
        plt.xlabel('Probability')
        plt.ylabel('Average response time (s) per request')
        plt.xticks(list(range(1, x_range+1)), x_label)
        ax.plot(list(range(1, x_range+1)), order_latency_cache, label="w/ caching")
        ax.plot(list(range(1, x_range+1)), order_latency_nocache, label="w/o caching")
        ax.set_title('Effectiveness of Caching')
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.grid(which='minor', linewidth=0.6)
        ax.legend()
        
        plt.show()


    else:
        print(f"Unknown argument: {args.type}")



if __name__ == '__main__':
   # Create an argument parser
    parser = argparse.ArgumentParser(description='Client.')
    # Add arguments 
    parser.add_argument('--type', dest='type', help='Type of experiment', type=str)
    # Parse the arguments and store them in a variable called 'args'
    args = parser.parse_args()

    # Call the main function with the 'args' parameter
    main(args)