import unittest
from EconomicModels.ProducerConsumer import Consumer as Con

cname = "C"

class MyTestCase(unittest.TestCase):
    def test_Ppurchase(self):
        consumer = Con.Consumer(cname)
        self.assertGreater(consumer.prob_purchase, 0)

    def test_makePurchase(self):
        consumer = Con.Consumer(cname, prob_purchase=0.5)
        inventory = 5  # must be 1 or greater
        time_steps = 100
        for i in range(time_steps):
            consumer.purchase(inventory)
        self.assertGreater(consumer.owned, 0)

    def test_prioritizeProducer(self):
        consumer = Con.Consumer(cname)
        p_list = ["P1", "P2", "P3"]
        self.assertIsNone(consumer.preferred_producer)

        consumer.prioritize_producers(p_list)
        self.assertEqual(len(consumer.preferred_producer), len(p_list))
        for index in range(len(p_list)):
            self.assertTrue(index in consumer.preferred_producer)

    def test_choosePriorityProducer(self):
        consumer = Con.Consumer(cname)
        p_list = ["P1", "P2", "P3"]

        consumer.prioritize_producers(p_list)
        choices = []
        for i in range(300):
            choice = consumer.choose_priority_producer()
            self.assertLessEqual(choice, len(p_list) - 1)
            choices.append(choice)

        for j in range(len(p_list)):
            self.assertTrue(j in choices)


if __name__ == '__main__':
    unittest.main()
