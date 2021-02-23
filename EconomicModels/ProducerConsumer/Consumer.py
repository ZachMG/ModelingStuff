import random as rand  # Should import statements somehow be placed in __init__.py?


class Consumer:
    def __init__(self, name, prob_purchase=0.5):
        self.name = name

        self.prob_purchase = prob_purchase
        self.owned = 0
        self.failed_purchases = 0
        self.preferred_producer = None  # may be a list or single value depending upon the simulation

    def purchase(self, available_items):
        action = rand.uniform(0, 1)
        if action <= self.prob_purchase:
            if available_items >= 1:
                self.owned += 1
                return True
            else:
                self.failed_purchases += 1
                return False
        else:
            return False

    def choose_producer(self, producers):
        self.preferred_producer = rand.randint(0, len(producers) - 1)

    def prioritize_producers(self, producers):
        producer_list = [i for i in range(len(producers))]
        rand.shuffle(producer_list)
        self.preferred_producer = producer_list

    def choose_priority_producer(self, p_choice=0.5):
        decision = False
        index = 0
        while decision is False:
            if index > len(self.preferred_producer) - 1:
                index = 0
            choice = rand.uniform(0, 1)
            if choice <= p_choice:
                decision = True
            elif choice > p_choice:
                index += 1
        return self.preferred_producer[index]


