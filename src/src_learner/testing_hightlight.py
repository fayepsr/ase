import SHModelUtils as bl
import unittest
import highlight

#testing return for each possible return statement

class Test(unittest.TestCase):
    
    def test_predict(self):
        #For Predict
        #Test for empty content for python
        self.assertEqual(highlight.predict('', 'python'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test for empty content for kotlin
        self.assertEqual(highlight.predict('', 'kotlin'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test for empty content for java
        self.assertEqual(highlight.predict('', 'java'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test with content (without testing what prediction returns)
        self.assertDictContainsSubset( {'ok': 1}, highlight.predict('ZGVmIHR5cGluZyh3b3JkKToK', 'python'), "Unuccessful run of function")
        #Test with language not in use
        self.assertEqual(highlight.predict('', 'R'),{'ok': -1, 'msg': 'Not yet accepting this language'}, "Language error")

    def test_finetune(self):
        #For Finetune
        #Test for empty content for python
        self.assertEqual(highlight.finetune('', 'python'), {'ok': 1}, "Unsuccessful run of function")
        #Test for empty content for kotlin
        self.assertEqual(highlight.finetune('', 'kotlin'), {'ok': 1}, "Unsuccessful run of function")
        #Test for empty content for java
        self.assertEqual(highlight.finetune('', 'java'), {'ok': 1}, "Unsuccessful run of function")
        #Test with content (without testing what prediction returns)
        self.assertDictContainsSubset( {'ok': 1}, highlight.finetune('ZGVmIHR5cGluZyh3b3JkKToK', 'python'), "Unuccessful run of function")
        #Test with language not in use
        self.assertEqual(highlight.finetune('', 'R'), {'ok': '-1', 'msg': 'Not yet accepting this language'}, "Language error")
        


#run the rest
unittest.main()