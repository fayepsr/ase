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

    def test_accuracy_empty_file(self):
        model = highlight.model_loader('python', 'base_model')
        txt_test_current = []
        highlight.check_accuracy(model, txt_test_current)


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main(exit=True)
