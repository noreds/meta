import unittest
import add_syntaxnet as sn


class TestSyntaxnet(unittest.TestCase):
    def testGenerateNetwork(self):
        self.assertEqual(sn.generate_network("Hallo Welt."), "Test")
