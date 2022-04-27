import SHModelUtils as bl
import jpype
import jpype.imports
from jpype.types import *
import unittest
import highlight


class Test(unittest.TestCase):
    
    def runTest(self):
        #For Predict
        #Test for empty content
        self.assertEqual(highlight.predict('', 'python'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test with content (without testing what prediction returns)
        self.assertDictContainsSubset( {'ok': 1}, highlight.predict('ZGVmIHR5cGluZyh3b3JkKToK', 'python'), "Unuccessful run of function")
        #Test with language not in use
        self.assertEqual(highlight.predict('', 'java'), {'ok': -1, 'msg': 'Not yet accepting this language'}, "Language error")

        #For Finetune
        #Test for empty content
        self.assertEqual(highlight.finetune('', 'python'), {'ok': 1}, "Unsuccessful run of function")
        #Test with content (without testing what prediction returns)
        self.assertDictContainsSubset( {'ok': 1}, highlight.finetune('ZGVmIHR5cGluZyh3b3JkKToK', 'python'), "Unuccessful run of function")
        #Test with language not in use
        self.assertEqual(highlight.finetune('', 'java'), {'ok': -1, 'msg': 'Not yet accepting this language'}, "Language error")
        


#run the rest
unittest.main()