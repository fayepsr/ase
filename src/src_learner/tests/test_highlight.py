import SHModelUtils as bl
import unittest
import highlight

#testing return for each possible return statement

class Test(unittest.TestCase):

    
    def test_predict(self):
        #For Predict
        highlighter = highlight.Highlighter()
        #Test for empty content for python
        self.assertEqual(highlighter.predict('', 'python'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test for empty content for kotlin
        self.assertEqual(highlighter.predict('', 'kotlin'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test for empty content for java
        self.assertEqual(highlighter.predict('', 'java'), {'ok': 1, 'prediction': [], 'result': []}, "Unsuccessful run of function")
        #Test with content (without testing what prediction returns)
        self.assertDictContainsSubset( {'ok': 1}, highlighter.predict('ZGVmIHR5cGluZyh3b3JkKToK', 'python'), "Unuccessful run of function")
        #Test with language not in use
        self.assertEqual(highlighter.predict('', 'R'),{'ok': -1, 'msg': 'Not yet accepting this language'}, "Language error")

    # load_training_set
    def test_load_training_set_correct_set_python(self):
        highlighter = highlight.Highlighter()
        highlighter.load_training_set('python')
        # check that txt is not empty
        self.assertTrue(highlighter.txt_training_current)

    def test_load_training_set_correct_set_java(self):
        highlighter = highlight.Highlighter()
        highlighter.load_training_set('java')
        # check that txt is not empty
        self.assertTrue(highlighter.txt_training_current)

    def test_load_training_set_correct_set_kotlin(self):
        highlighter = highlight.Highlighter()
        highlighter.load_training_set('kotlin')
        # check that txt is not empty
        self.assertTrue(highlighter.txt_training_current)

    def test_load_training_set_wrong_path(self):
        highlighter = highlight.Highlighter()
        highlighter.training_directory_root = '/wrong/path'
        # check that txt is not empty
        self.assertRaises(FileNotFoundError, highlighter.load_training_set('kotlin'))
    # load_test_set
    def test_load_test_set_correct_set_python(self):
        highlighter = highlight.Highlighter()
        highlighter.load_test_set('python')
        # check that txt is not empty
        self.assertTrue(highlighter.txt_test_current)

    def test_load_test_set_correct_set_java(self):
        highlighter = highlight.Highlighter()
        highlighter.load_test_set('java')
        # check that txt is not empty
        self.assertTrue(highlighter.txt_test_current)

    def test_load_test_set_correct_set_kotlin(self):
        highlighter = highlight.Highlighter()
        highlighter.load_test_set('kotlin')
        # check that txt is not empty
        self.assertTrue(highlighter.txt_test_current)

    def test_load_test_set_wrong_path(self):
        highlighter = highlight.Highlighter()
        highlighter.test_directory_root = '/wrong/path'
        # check that txt is not empty
        self.assertRaises(FileNotFoundError, highlighter.load_test_set('kotlin'))
    """
    # check_overlap

    def helper_load_txt_from_folder(self, directory):
        path = directory + "/training_current.txt"
        with open(path, 'rt', encoding='utf-8') as f_training_current:
            txt_file = f_training_current.read().splitlines()
        return txt_file

    # should not raise an exception
    def test_check_overlap_both_files_empty(self, txt_training_current, txt_test_current, language):
        highlighter = highlight.Highlighter()
        train_directory = '/src/tests/trainingData/empty'
        test_directory = '/src/tests/accuracyTestData/empty'
        txt_train = self.helper_load_txt_from_folder(train_directory)
        txt_test = self.helper_load_txt_from_folder(test_directory)
        output = highlighter.check_overlap(txt_train,txt_test, 'python')
    """
    def test_finetune_python(self):
        highlighter = highlight.Highlighter()
        message = highlighter.finetune('python')
        self.assertIn('ok', message)
        self.assertIn('msg', message)

    def test_finetune_java(self):
        highlighter = highlight.Highlighter()
        message = highlighter.finetune('java')
        self.assertIn('ok', message)
        self.assertIn('msg', message)

    def test_finetune_kotlin(self):
        highlighter = highlight.Highlighter()
        message = highlighter.finetune('kotlin')
        self.assertIn('ok', message)
        self.assertIn('msg', message)




if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main(exit=True)
