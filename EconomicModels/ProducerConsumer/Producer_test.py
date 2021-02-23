import unittest
from EconomicModels.ProducerConsumer import Producer as prod
from EconomicModels.ProducerConsumer import Storage as stor

pname = "P"

class MyTestCase(unittest.TestCase):
    def test_production_rate(self):
        producer = prod.Producer(pname)
        self.assertGreater(producer.production_rate, 0)

    def test_emptyInventory(self):
        producer = prod.Producer(pname)
        time_steps = 100
        self.assertEqual(producer.inventory, 0, msg="Inventory Initially 0")
        for i in range(time_steps):
            producer.produce_object()
            self.assertGreater(producer.inventory, 0, msg="Produced Item added to inventory")
            producer.clear_inventory()
            self.assertEqual(producer.inventory, 0, msg="Inventory is Emptied every time step")

    def test_saleTracking(self):
        producer = prod.Producer(pname)
        time_steps = 100
        for i in range(time_steps):
            producer.produce_object()
            producer.track_sales(sold=True)
            producer.clear_inventory()
        self.assertEqual(producer.sales, time_steps)

    def test_productionTracking(self):
        producer = prod.Producer(pname)
        time_steps = 100
        for i in range(time_steps):
            producer.produce_object()
            producer.clear_inventory()
        self.assertEqual(producer.total_production, time_steps * producer.production_rate)

    # Tests regarding the interaction of producer and storage objects
    def test_addStorage(self):
        producer = prod.Producer(pname)
        storage = stor.Storage(100)
        producer.add_storage(storage)

        self.assertIsNot(producer.storage, None)

    def test_upgradeStorage(self):
        producer = prod.Producer(pname)
        storage = stor.Storage(100)

        producer.add_storage(storage)
        init_storagecap = producer.storage.capacity
        producer.upgrade_storage(50)

        self.assertGreater(producer.storage.capacity, init_storagecap)

    def test_storeInventory(self):
        producer = prod.Producer(pname)
        storage = stor.Storage(100)
        producer.add_storage(storage)  # add storage to a producer
        init_s_inventory = producer.storage.inventory
        producer.store_inventory(10)

        self.assertGreater(producer.storage.inventory, init_s_inventory)

    def test_requestInventory(self):
        producer = prod.Producer(pname)
        storage = stor.Storage(100)

        producer.add_storage(storage)
        producer.store_inventory(10)
        init_prodinventory = producer.inventory
        init_storinventory = producer.storage.inventory
        producer.request_inventory(5)

        self.assertGreater(producer.inventory, init_prodinventory)
        self.assertLess(producer.storage.inventory, init_storinventory)



if __name__ == '__main__':
    unittest.main()
