import unittest
import src.ayla as ayla

class TestAyla(unittest.TestCase):

    def testHash(self):
        self.assertEqual("e508b08f17747e6aca989eb75dd68f033e4376f6533c2d82d7cbd1cba7ef9b89", ayla.calculateHash("1","asd","1501316741", "hello world"))

    def test_generataNextBlock(self):
        gb = ayla.getLatestBlock()
        next_block = ayla.generataNextBlock(gb,"hello world")
        self.assertEqual(next_block.index, 1)
        self.assertEqual(next_block.data, "hello world")
        self.assertIsNotNone(next_block.hash)
        self.assertIsNotNone(next_block.timestamp)
        self.assertEqual(next_block.previus_hash,ayla.getLatestBlock().hash)

    def test_validateblock(self):
        gb = ayla.getLatestBlock()
        n = ayla.generataNextBlock(gb,"hello world")

        self.assertTrue(ayla.isValidBlock(n,gb))
        n_not_valid_hash = n
        n_not_valid_hash.hash = "not valid hash"
        self.assertFalse(ayla.isValidBlock(n_not_valid_hash,gb))
        n_not_valid_prev_hash = n
        n_not_valid_prev_hash.previus_hash = "not valid hash"
        self.assertFalse(ayla.isValidBlock(n_not_valid_prev_hash,gb))
        n_not_valid_index = n
        n_not_valid_index.index =4444
        self.assertFalse(ayla.isValidBlock(n_not_valid_index,gb))

    def test_isvalidblock(self):

        gb = ayla.getLatestBlock()
        chain = [gb]

        for i in range(1,100):
            n = ayla.generataNextBlock(chain[i-1]," block pop")
            chain.append(n)

        self.assertTrue(ayla.isValidChain(chain))

        chain[72] = gb

        self.assertFalse(ayla.isValidChain(chain))






if __name__ == '__main__':
    unittest.main()
