import SHModelUtils as bl
import unittest
import highlight

#testing return for each possible return statement

class Test(unittest.TestCase):
    
    def test_predict(self):
        #For Predict
        #Test for empty content for python
        response = highlight.predict('', 'python')
        self.assertEqual(response.get('ok'), 1)
        #Test for empty content for kotlin
        response = highlight.predict('', 'kotlin')
        self.assertEqual(response.get('ok'), 1)
        #Test for empty content for java
        response = highlight.predict('', 'java')
        self.assertEqual(response.get('ok'), 1)
        #Test with language not in use
        self.assertEqual(highlight.predict('', 'R'), {'ok': -1, 'msg': 'not yet accepting this language'}, "Language error")

    def test_accuracy_empty_file(self):
        model = highlight.model_loader('python', 'base_model')
        txt_test_current = []
        result = highlight.check_accuracy(model, txt_test_current)
        self.assertEquals(result.get('ok'), -1)

    def test_accuracy(self):
        model = highlight.model_loader('kotlin', 'base_model')

        path = '/src/tests/accuracy/kotlin/test_current.txt'
        with open(path, 'rt', encoding='utf-8') as f_test_current:
            txt_test_current = f_test_current.read().splitlines()

        result = highlight.check_accuracy(model, txt_test_current)
        self.assertEquals(result.get('ok'), 1)
        self.assertGreater(result.get('accuracy'), 0.01)

    def test_check_overlap_not_overlapping(self):
        path_train = '/src/tests/training/python/training_current.txt'
        with open(path_train, 'rt', encoding='utf-8') as f_test_current:
            txt_train_current = f_test_current.read().splitlines()

        path_test = '/src/tests/accuracy/python/test_current.txt'
        with open(path_test, 'rt', encoding='utf-8') as f_test_current:
            txt_test_current = f_test_current.read().splitlines()

        result = highlight.check_overlap(txt_train_current, txt_test_current, 'python', training_directory='/src/tests/training/python', training_current_path=path_train,
                      test_directory='/src/tests/accuracy/python', test_current_path=path_test)
        self.assertEquals(result.get('training_current'), txt_train_current)
        self.assertEquals(result.get('test_current'), txt_test_current)

    def test_check_overlap_partially_overlapping(self):
        path_train = '/src/tests/training/java/training_current.txt'
        with open(path_train, 'rt', encoding='utf-8') as f_test_current:
            txt_train_current = f_test_current.read().splitlines()

        path_test = '/src/tests/accuracy/java/test_current.txt'
        with open(path_test, 'rt', encoding='utf-8') as f_test_current:
            txt_test_current = f_test_current.read().splitlines()

        len_before = len(txt_train_current)
        result = highlight.check_overlap(txt_train_current, txt_test_current, 'java', training_directory='/src/tests/training/java', training_current_path=path_train,
                      test_directory='/src/tests/accuracy/java', test_current_path=path_test)
        len_after = len(result.get('training_current'))
        self.assertGreater(len_before, len_after)
        # write file to textfile again so that tests can be rerun
        with open(path_train, 'w', encoding="utf-8") as f_train_current:
            f_train_current.write("\n".join(txt_train_current))

    def test_check_overlap_completely_overlapping(self):
        path_train = '/src/tests/training/kotlin/training_current.txt'
        with open(path_train, 'rt', encoding='utf-8') as f_test_current:
            txt_train_current = f_test_current.read().splitlines()

        path_test = '/src/tests/accuracy/kotlin/test_current.txt'
        with open(path_test, 'rt', encoding='utf-8') as f_test_current:
            txt_test_current = f_test_current.read().splitlines()

        result = highlight.check_overlap(txt_train_current, txt_test_current, 'kotlin', training_directory='/src/tests/training/kotlin', training_current_path=path_train,
                      test_directory='/src/tests/accuracy/kotlin', test_current_path=path_test)

        # write file to textfile again so that tests can be rerun
        with open(path_train, 'w', encoding="utf-8") as f_train_current:
            f_train_current.write("\n".join(txt_train_current))

        self.assertEquals(result.get('training_current'), [])

    def test_finetune_python(self):
        response = highlight.finetune('python')
        self.assertEquals(response.get('ok'), 1)

    def test_finetune_kotlin(self):
        response = highlight.finetune('kotlin')
        self.assertEquals(response.get('ok'), 1)

    def test_finetune_java(self):
        response = highlight.finetune('java')
        self.assertEquals(response.get('ok'), 1)



if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main(exit=True)
