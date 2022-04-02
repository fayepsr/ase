
import jpype
import jpype.imports
from jpype.types import *
import SHModelUtils as bl

jpype.startJVM(classpath=['../src_java/SHOracle.jar'])
Python3Resolver = jpype.JClass("resolver.Python3Resolver")

model = bl.SHModel(bl.PYTHON3_LANG_NAME, 'base_model')
resolver = Python3Resolver()

'''
from SHModelUtils import *
pythonModel = SHModel(PYTHON3_LANG_NAME, "pythonModel_prediction")
pythonModel.setup_for_prediction()
tt = pythonModel.predict([1, 25, 30, 44, 55])
print(tt)


pythonModel = SHModel(PYTHON3_LANG_NAME, "pythonModel_finetuning")
pythonModel.setup_for_finetuning()
tt = pythonModel.finetune_on([1, 25, 30, 44, 55], [0, 0, 4, 0, 3])
print(tt)'''