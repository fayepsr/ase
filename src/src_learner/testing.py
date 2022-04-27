import SHModelUtils as bl
import jpype
import jpype.imports
from jpype.types import *
import unittest
import highlight


class Test(unittest.TestCase):
    
    def runTest(self):
        #Test for empty content
        self.assertEqual(highlight.predict('', 'python'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test with content
        #self.assertEqual(highlight.predict('', 'python'), {'ok': 1, 'prediction': [8, 6, 7, 6, 11, [401 chars]41}]}, "Unuccessful run of function")


#run the rest
unittest.main()