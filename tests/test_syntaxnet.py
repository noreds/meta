import unittest
import add_syntaxnet as sn


class TestSyntaxnet(unittest.TestCase):
    def testGenerateNetwork(self):
        print(sn.generate_network('Sie sprach von einem " herben Rückschlags " , will Trump in Hamburg aber nicht isolieren .'))
        self.assertEqual(sn.generate_network("Hallo Welt ."), {'sentences': [{'words': [{'type2': '_', 'type1': 'PROPN', 'name': 'Hallo'}, {'type2': '_', 'type1': 'PROPN', 'name': 'Welt'}, {'type2': '_', 'type1': 'PUNCT', 'name': '.'}]}]})
