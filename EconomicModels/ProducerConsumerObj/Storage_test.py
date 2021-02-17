import unittest
import EconomicModels.ProducerConsumerObj.Storage as stor

CAP = 100


class MyTestCase(unittest.TestCase):
    def test_initInventory(self):
        storage = stor.Storage(CAP)
        self.assertEqual(storage.inventory, 0)

    def test_addStorage(self):
        # make sure that upon adding to storage inventory is increased
        storage = stor.Storage(CAP)
        init_inventory = storage.inventory
        storage.add_inventory(5)

        self.assertGreater(storage.inventory, init_inventory)

    def test_removeStorage(self):
        # make sure that inventory decreases when items are removed from storage by the requested amount
        storage = stor.Storage(CAP)
        storage.inventory = 50
        init_inventory = storage.inventory
        storage.remove_inventory(20)
        self.assertLess(storage.inventory, init_inventory)

    def test_loseStorage(self):
        # if items in storage are perishable make sure that some fraction of items are lost and losses increase
        storage = stor.Storage(CAP)
        init_loss = storage.storage_loss
        storage.add_inventory(10)
        init_inventory = storage.inventory
        storage.lose_inventory(loss_rate=0.05)

        self.assertGreater(storage.storage_loss, init_loss, msg="Loss fails to increase as inventory expires")
        self.assertLess(storage.inventory, init_inventory, msg="Inventory fails to decrease with loss")

    def test_maxInventory(self):
        # ensure max capacity is never exceeded
        storage = stor.Storage(1)
        storage.add_inventory(2)

        self.assertEqual(storage.inventory, storage.capacity)

    def test_minInventory(self):
        storage = stor.Storage(5)
        storage.remove_inventory(10)
        self.assertGreaterEqual(storage.inventory, 0)

    # def test_minCapacity(self):  # not sure how to use assertRaises
    #     # makes sure capacity can never go below 0
    #     self.assertRaises(stor.StorageError, stor.Storage(-1))



if __name__ == '__main__':
    unittest.main()
