import os
import shutil
import accuracy_check

"""
Updates the base model with a more accurate fine-tuned model

Args:
    language: langauge for which the model needs to be updated

"""

def update_m(language = "python"):
    
    # text file storing number of input requests used for fine-tuning, accuracy
    # of the base model, and accuracy of the fine-tuning model
    model_status = "./model_status_" + language + ".txt"
    
    # Threshold of difference in accuracy for updating the base model/fine-tuning model
    IMPROVEMENT_THRESHOLD = 0.005
    
    # Frequency of updating the model in terms of input requests for fine-tuning
    REQUEST_FREQUENCY = 100
    
    # Text file with current details of the models
    with open(model_status, "a+", encoding="utf-8") as f:
        f.seek(0)
        status_list = f.read().splitlines()
    
    num_requests = 0
    accuracy_base_model = 0
    accuracy_finetune_model = 0
    
    if status_list:
        num_requests = int(status_list[0].split("=")[1])
        accuracy_base_model = float(status_list[1].split("=")[1])
        accuracy_finetune_model = float(status_list[2].split("=")[1])
        
    num_requests += 1
    
    # No need to update, store the updated model-status    
    if num_requests < REQUEST_FREQUENCY:
        lines = ['num_requests=' + str(num_requests)]
        lines.append('accuracy_base_model=' + str(accuracy_base_model))
        lines.append('accuracy_finetune_model=' + str(accuracy_finetune_model))
        with open(model_status, "w+", encoding="utf-8") as f:
            f.write('\n'.join(lines))
        return {'ok': 1, 'msg': 'No update required yet'}
        
    
    try:
        # Check accuracies of base and fine-tuning models
        model_types = ["finetuning", "base"]
        res_finetuning = accuracy_check.check_accuracy(model_types[0], language)
        res_base = accuracy_check.check_accuracy(model_types[1], language)
        if res_finetuning['ok'] != 1:
            raise ValueError('In Finetuning model: ' + res_finetuning['msg'])
        elif res_base['ok'] != 1:
            raise ValueError('In Base model: ' + res_base['msg'])
    
    except ValueError as e:
        return {'ok': -1, 'msg': e}
        
    else:
        accuracy_finetune_model = res_finetuning['accuracy']
        accuracy_base_model = res_base['accuracy']
        
        # Difference in accuracy between base and fine-tuning models
        accuracy_improvement = accuracy_finetune_model - accuracy_base_model
    
    # Model names for Python language have the prefix 'python3'
    if language == "python":
        language = language + "3"
    
    # Condition for replacing base model with the improved fine-tuning model
    if accuracy_improvement > IMPROVEMENT_THRESHOLD:
        cwd = os.getcwd()
        path_base_model = language + "_base_model.pt"
        path_finetune_model = language + "_finetuning_model.pt"
        
        try:
            os.remove(path_base_model)
            shutil.copyfile(path_finetune_model, path_base_model)
        except Exception as e:
            return {'ok' : -1, 'Exception' : e}
        
        else:
            lines = ['num_requests=' + str(num_requests)]
            lines.append('accuracy_base_model=' + str(accuracy_finetune_model))
            lines.append('accuracy_finetune_model=' + str(accuracy_finetune_model))
            with open(model_status, "w+", encoding="utf-8") as f:
                f.write('\n'.join(lines))
            return "Base model updated"
    
    # Condition for rolling back the fine-tuning model with the original base model
    elif accuracy_improvement < (-1*IMPROVEMENT_THRESHOLD):
        cwd = os.getcwd()
        path_base_model = language + "_base_model.pt"
        path_finetune_model = language + "_finetuning_model.pt"
        
        try:
            os.remove(path_finetune_model)
            shutil.copyfile(path_base_model, path_finetune_model)
        except Exception as e:
            return {'ok' : -1, 'Exception' : e}
        
        else:
            lines = ['num_requests=' + str(num_requests)]
            lines.append('accuracy_base_model=' + str(accuracy_base_model))
            lines.append('accuracy_finetune_model=' + str(accuracy_base_model))
            with open(model_status, "w+", encoding="utf-8") as f:
                f.write('\n'.join(lines))
            return "Base model rolled back"
        
    # No significant difference in accuracy, no update needed
    else:
        lines = ['num_requests=' + str(num_requests)]
        lines.append('accuracy_base_model=' + str(accuracy_base_model))
