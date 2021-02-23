from . import Consumer as cons
from . import Producer as prod
from . import Storage as stor

import matplotlib.pyplot as plt
import random as rand
import numpy as np


# def shuffle_list(list_object):  # works as a shuffle, could likely be improved
#     copy = list_object
#     new_list = []
#     iterations = len(list_object)
#     for i in range(iterations):
#         old_index = rand.randint(0, len(copy) - 1)
#         new_list.append(copy[old_index])
#         copy.pop(old_index)
#     assert len(copy) == 0
#     return new_list

# The below simulations are done without considering any options for producers to use a storage object
def simulation_basic(time=100000):
    """
    A single producer and consumer engage in an economy in which the producer makes some number of items every time
    step and the consumer decides simply whether they buy or don't buy.
    :param time: Duration of Simulation
    :return: Plots of the producers sold objects and the consumers purchased objects
    """
    consumer = cons.Consumer("C1")
    producer = prod.Producer("P1")

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Objects Sold")
    sales_at_time = []
    for t in range(time):
        producer.produce_object()  # producer makes a product
        # Consumer decides whether or not to purchase the item provided the consumer has it
        producer.track_sales(sold=consumer.purchase(producer.inventory))
        # The producer clears their inventory at the end of each time step
        producer.clear_inventory()
        sales_at_time.append(producer.sales)
    ax1.plot(sales_at_time)
    plt.show()


def simulation_competingConsumers(time=100000):  # CC
    """
    As the basic simulation but now two consumers compete for the object which is being sold by a single consumer.
    The consumer which arrives at the producer's shop first gets priority. The priority is determined simply by a
    random shuffle of the two consumers for now.
    :param time: Duration of Simulation
    :return: plots
    """
    consumer1 = cons.Consumer("C1")
    consumer2 = cons.Consumer("C2")
    producer = prod.Producer("P1")

    consumers = [consumer1, consumer2]

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Objects Sold")
    sales_at_time = []

    fig2, ax2 = plt.subplots()
    fig2.suptitle("Consumer 1 Purchase Attempts")
    c1_purchases = []
    c1_failed_purchases = []

    fig3, ax3 = plt.subplots()
    fig3.suptitle("Consumer 2 Purchase Attempts")
    c2_purchases = []
    c2_failed_purchases = []
    for t in range(time):
        # randomly determine consumer priority
        c1 = rand.randint(0, 1)
        c2 = int(np.abs(c1 - 1))

        producer.produce_object()  # producer makes a product
        # Consumer decides whether or not to purchase the item provided the consumer has it
        producer.track_sales(sold=consumers[c1].purchase(producer.inventory))
        producer.track_sales(sold=consumers[c2].purchase(producer.inventory))
        # The producer clears their inventory at the end of each time step
        producer.clear_inventory()

        # Track Data
        sales_at_time.append(producer.sales)
        c1_purchases.append(consumer1.owned)
        c1_failed_purchases.append(consumer1.failed_purchases)

        c2_purchases.append(consumer2.owned)
        c2_failed_purchases.append(consumer2.failed_purchases)

    ax1.plot(sales_at_time)
    ax2.plot(c1_purchases)
    ax2.plot(c1_failed_purchases)

    ax3.plot(c2_purchases)
    ax3.plot(c2_failed_purchases)
    plt.show()


def simulation_competingProducers(time=100000):  # CP
    """
    As the basic simulation but now producers compete for the consumers attention. The consumer decides each time step
    which producer they prefer to purchase from randomly with equiprobability.
    :param time: Duration of Simulation
    :return: plots
    """
    consumer = cons.Consumer("C1")
    producer1 = prod.Producer("P1")
    producer2 = prod.Producer("P2")

    producers = [producer1, producer2]

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Producer 1 Objects Sold")
    p1_sales = []

    fig2, ax2 = plt.subplots()
    fig2.suptitle("Producer 2 Objects Sold")
    p2_sales = []

    fig3, ax3 = plt.subplots()
    fig3.suptitle("Consumer Objects Owned")
    c_purchases = []
    c_failed_purchases = []
    for t in range(time):
        p = rand.randint(0, 1)
        producer1.produce_object()  # producer makes a product
        producer2.produce_object()
        # Consumer decides whether or not to purchase the item provided the consumer has it
        producers[p].track_sales(sold=consumer.purchase(producers[p].inventory))
        # The producer clears their inventory at the end of each time step
        producer1.clear_inventory()
        producer2.clear_inventory()

        # update data
        p1_sales.append(producer1.sales)
        p2_sales.append(producer2.sales)

        c_purchases.append(consumer.owned)
        c_failed_purchases.append(consumer.failed_purchases)
    ax1.plot(p1_sales)
    ax2.plot(p2_sales)
    ax3.plot(c_purchases)
    ax3.plot(c_failed_purchases)
    plt.show()


def simulation_competition(time=100000):
    consumer1 = cons.Consumer("C1")
    consumer2 = cons.Consumer("C2")
    producer1 = prod.Producer("P1")
    producer2 = prod.Producer("P2")

    consumers = [consumer1, consumer2]
    producers = [producer1, producer2]

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Producer 1 Objects Sold and Lost")
    p1_sales = []
    p1_losses = []

    fig2, ax2 = plt.subplots()
    fig2.suptitle("Consumer 1 Purchase Attempts")
    c1_purchases = []
    c1_failed_purchases = []

    fig3, ax3 = plt.subplots()
    fig3.suptitle("Consumer 2 Purchase Attempts")
    c2_purchases = []
    c2_failed_purchases = []

    fig4, ax4 = plt.subplots()
    fig4.suptitle("Producer 2 Objects Sold and Lost")
    p2_sales = []
    p2_losses = []
    for t in range(time):
        # randomly determine consumer priority
        c1 = rand.randint(0, 1)
        c2 = int(np.abs(c1 - 1))

        consumer1.choose_producer(producers)
        consumer2.choose_producer(producers)

        producer1.produce_object()  # producer makes a product
        producer2.produce_object()
        # Consumer decides whether or not to purchase the item provided the consumer has it
        producers[consumer1.preferred_producer].track_sales(
            sold=consumers[c1].purchase(producers[consumer1.preferred_producer].inventory))
        producers[consumer2.preferred_producer].track_sales(
            sold=consumers[c2].purchase(producers[consumer2.preferred_producer].inventory))
        # The producer clears their inventory at the end of each time step
        producer1.clear_inventory()
        producer2.clear_inventory()

        # Track Data
        p1_sales.append(producer1.sales)
        p2_sales.append(producer2.sales)

        p1_losses.append(producer1.lost_inventory)
        p2_losses.append(producer2.lost_inventory)

        c1_purchases.append(consumer1.owned)
        c1_failed_purchases.append(consumer1.failed_purchases)

        c2_purchases.append(consumer2.owned)
        c2_failed_purchases.append(consumer2.failed_purchases)

    ax1.plot(p1_sales, label="Sales")
    ax1.plot(p1_losses, label="Losses")
    ax1.legend()

    ax4.plot(p2_sales, label="Sales")
    ax4.plot(p2_losses, label="Losses")
    ax4.legend()

    ax2.plot(c1_purchases, label="Success")
    ax2.plot(c1_failed_purchases, label="Failure")
    ax2.legend()

    ax3.plot(c2_purchases, label="Success")
    ax3.plot(c2_failed_purchases, label="Failure")
    ax3.legend()
    plt.show()


def simulation_multiConsumer(consumer_n=2, time=100000):
    producer1 = prod.Producer("P1")
    producer2 = prod.Producer("P1")

    consumers = []
    for i in range(consumer_n):
        new_consumer = cons.Consumer("C" + str(i))
        consumers.append(new_consumer)

    producers = [producer1, producer2]

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Producer 1 Objects Sold and Lost")
    p1_sales = []
    p1_losses = []

    fig2, ax2 = plt.subplots()
    fig2.suptitle("Producer 2 Objects Sold and Lost")
    p2_sales = []
    p2_losses = []

    fig3, ax3 = plt.subplots()
    fig3.suptitle("Consumer Assets Acquired")
    c_assets = {}
    for consumer in consumers:
        c_assets[consumer] = []

    fig4, ax4 = plt.subplots()
    fig4.suptitle("Consumer Failed Purchases")
    c_losses = {}
    for consumer in consumers:
        c_losses[consumer] = []
    for t in range(time):
        # randomly determine consumer priority
        rand.shuffle(consumers)

        for consumer in consumers:
            consumer.choose_producer(producers)

        producer1.produce_object()  # producer makes a product
        producer2.produce_object()
        # Consumer decides whether or not to purchase the item provided the consumer has it
        for consumer in consumers:
            producers[consumer.preferred_producer].track_sales(
                sold=consumer.purchase(producers[consumer.preferred_producer].inventory))
        # The producer clears their inventory at the end of each time step
        producer1.clear_inventory()
        producer2.clear_inventory()

        # Track Data
        p1_sales.append(producer1.sales)
        p2_sales.append(producer2.sales)

        p1_losses.append(producer1.lost_inventory)
        p2_losses.append(producer2.lost_inventory)

        for consumer in consumers:
            c_assets[consumer].append(consumer.owned)
            c_losses[consumer].append(consumer.failed_purchases)

    ax1.plot(p1_sales, label="Sales")
    ax1.plot(p1_losses, label="Losses")
    ax1.legend()

    ax2.plot(p2_sales, label="Sales")
    ax2.plot(p2_losses, label="Losses")
    ax2.legend()

    for consumer in consumers:
        ax3.plot(c_assets[consumer], label=consumer.name)
        ax4.plot(c_losses[consumer], label=consumer.name)
    ax3.legend()
    ax4.legend()
    plt.show()


def simulation_multi(consumer_n=3, producer_n=3, time=100000):
    producers = []
    for i in range(producer_n):
        new_producer = prod.Producer("P" + str(i))
        producers.append(new_producer)

    consumers = []
    for i in range(consumer_n):
        new_consumer = cons.Consumer("C" + str(i))
        consumers.append(new_consumer)

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Producer Sales")
    p_sales = {}

    fig2, ax2 = plt.subplots()
    fig2.suptitle("Producer Losses")
    p_losses = {}

    fig3, ax3 = plt.subplots()
    fig3.suptitle("Consumer Assets Acquired")
    c_assets = {}

    fig4, ax4 = plt.subplots()
    fig4.suptitle("Consumer Failed Purchases")
    c_losses = {}

    for consumer in consumers:
        c_losses[consumer] = []
        c_assets[consumer] = []

    for producer in producers:
        p_losses[producer] = []
        p_sales[producer] = []
    for t in range(time):
        # randomly determine consumer priority
        rand.shuffle(consumers)

        for consumer in consumers:
            consumer.choose_producer(producers)

        for producer in producers:  # producer makes a product
            producer.produce_object()
        # Consumer decides whether or not to purchase the item provided the consumer has it
        for consumer in consumers:
            producers[consumer.preferred_producer].track_sales(
                sold=consumer.purchase(producers[consumer.preferred_producer].inventory))
        # The producer clears their inventory at the end of each time step
        for producer in producers:
            producer.clear_inventory()

        # Track Data
        for producer in producers:
            p_sales[producer].append(producer.sales)
            p_losses[producer].append(producer.lost_inventory)

        for consumer in consumers:
            c_assets[consumer].append(consumer.owned)
            c_losses[consumer].append(consumer.failed_purchases)

    for producer in producers:
        ax1.plot(p_sales[producer], label=producer.name)
        ax2.plot(p_losses[producer], label=producer.name)
    ax1.legend()
    ax2.legend()

    for consumer in consumers:
        ax3.plot(c_assets[consumer], label=consumer.name)
        ax4.plot(c_losses[consumer], label=consumer.name)
    ax3.legend()
    ax4.legend()

    plt.show()


# From here on simulations use storage type objects
def simulation_prodStorage(consumer_n=3, producer_n=3, time=100000):
    producers = []
    for i in range(producer_n):
        new_producer = prod.Producer("P" + str(i))
        new_storage = stor.Storage(50)
        new_producer.add_storage(new_storage)
        producers.append(new_producer)

    consumers = []
    for i in range(consumer_n):
        new_consumer = cons.Consumer("C" + str(i))
        consumers.append(new_consumer)

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Producer Sales")
    p_sales = {}

    fig2, ax2 = plt.subplots()
    fig2.suptitle("Producer Losses")
    p_losses = {}

    fig3, ax3 = plt.subplots()
    fig3.suptitle("Consumer Assets Acquired")
    c_assets = {}

    fig4, ax4 = plt.subplots()
    fig4.suptitle("Consumer Failed Purchases")
    c_losses = {}

    fig5, ax5 = plt.subplots()
    fig5.suptitle("Storage Inventory")
    s_inventory = {}

    for consumer in consumers:
        c_losses[consumer] = []
        c_assets[consumer] = []

    for producer in producers:
        p_losses[producer] = []
        p_sales[producer] = []
        s_inventory[producer] = []

    for t in range(time):
        # randomly determine consumer priority
        rand.shuffle(consumers)

        for consumer in consumers:
            consumer.choose_producer(producers)

        for producer in producers:  # producer makes a product
            producer.produce_object()
            # producers always attempt to carry as much product as customers can possibly purchase
            producer.request_inventory(len(consumers) - producer.inventory)
        # Consumer decides whether or not to purchase the item provided the consumer has it
        for consumer in consumers:
            producers[consumer.preferred_producer].track_sales(
                sold=consumer.purchase(producers[consumer.preferred_producer].inventory))
        # The producer clears their inventory at the end of each time step
        for producer in producers:
            producer.clear_inventory()

        # Track Data
        for producer in producers:
            p_sales[producer].append(producer.sales)
            p_losses[producer].append(producer.lost_inventory)
            s_inventory[producer].append(producer.storage.inventory)

        for consumer in consumers:
            c_assets[consumer].append(consumer.owned)
            c_losses[consumer].append(consumer.failed_purchases)

    for producer in producers:
        ax1.plot(p_sales[producer], label=producer.name)
        ax2.plot(p_losses[producer], label=producer.name)
        ax5.plot(s_inventory[producer], label=producer.name)
    ax1.legend()
    ax2.legend()
    ax5.legend()

    for consumer in consumers:
        ax3.plot(c_assets[consumer], label=consumer.name)
        ax4.plot(c_losses[consumer], label=consumer.name)
    ax3.legend()
    ax4.legend()

    plt.show()

def simulation_consumerPriorities(consumer_n=3, producer_n=3, time=100000):
    producers = []
    for i in range(producer_n):
        new_producer = prod.Producer("P" + str(i))
        new_storage = stor.Storage(50)
        new_producer.add_storage(new_storage)
        producers.append(new_producer)

    consumers = []
    for i in range(consumer_n):
        new_consumer = cons.Consumer("C" + str(i))
        new_consumer.prioritize_producers(producers)  # randomly generate a prioritized list of producer indices
        consumers.append(new_consumer)

    fig1, ax1 = plt.subplots()
    fig1.suptitle("Producer Sales")
    p_sales = {}

    fig2, ax2 = plt.subplots()
    fig2.suptitle("Producer Losses")
    p_losses = {}

    fig3, ax3 = plt.subplots()
    fig3.suptitle("Consumer Assets Acquired")
    c_assets = {}

    fig4, ax4 = plt.subplots()
    fig4.suptitle("Consumer Failed Purchases")
    c_losses = {}

    fig5, ax5 = plt.subplots()
    fig5.suptitle("Storage Inventory")
    s_inventory = {}

    for consumer in consumers:
        c_losses[consumer] = []
        c_assets[consumer] = []

    for producer in producers:
        p_losses[producer] = []
        p_sales[producer] = []
        s_inventory[producer] = []

    for t in range(time):
        # randomly determine consumer priority
        rand.shuffle(consumers)

        for producer in producers:  # producer makes a product
            producer.produce_object()
            # producers always attempt to carry as much product as customers can possibly purchase
            producer.request_inventory(len(consumers) - producer.inventory)
        # Consumer decides whether or not to purchase the item provided the consumer has it
        for consumer in consumers:
            choice = consumer.choose_priority_producer()  # consumer selects a producer based upon prioritized list
            producers[consumer.preferred_producer[choice]].track_sales(
                sold=consumer.purchase(producers[consumer.preferred_producer[choice]].inventory))
        # The producer clears their inventory at the end of each time step
        for producer in producers:
            producer.clear_inventory()

        # Track Data
        for producer in producers:
            p_sales[producer].append(producer.sales)
            p_losses[producer].append(producer.lost_inventory)
            s_inventory[producer].append(producer.storage.inventory)

        for consumer in consumers:
            c_assets[consumer].append(consumer.owned)
            c_losses[consumer].append(consumer.failed_purchases)

    for producer in producers:
        ax1.plot(p_sales[producer], label=producer.name)
        ax2.plot(p_losses[producer], label=producer.name)
        ax5.plot(s_inventory[producer], label=producer.name)
    ax1.legend()
    ax2.legend()
    ax5.legend()

    for consumer in consumers:
        ax3.plot(c_assets[consumer], label=consumer.name)
        ax4.plot(c_losses[consumer], label=consumer.name)
    ax3.legend()
    ax4.legend()

    plt.show()


simulation_consumerPriorities(consumer_n=5, producer_n=7)
