import math
from collections import Counter

def partial_acc(pred, actual):
    '''
    Calculates partial accuracy.

    Arguments:
    pred -- list containing all the predicted values from the model
    actual -- list containing all the actual values (true labels)

    NOTE: pred[i] must correlate directly with actual[i]

    Return: The partial accuracy score of the model from 0-100.
    '''
    if len(pred) != len(actual):
        print ("Lists are not the same size. Ending")
        return
    pred = [x.upper() for x in pred]
    actual = [x.upper() for x in actual]
    score = 0
    for i, val in enumerate(pred):
        # calc exact match ##
        if pred[i] == actual[i]:
            score += 0.5

        ## calc num words match ##
        if len(pred[i].split(" ")) == len(actual[i].split(" ")):
            score += 0.1

        ## find if there are any word matches ##
        match = False
        for each_word_pred in pred[i].split(" "):
            if match:
                break
            if each_word_pred[-1] == 'S':
                each_word_pred = each_word_pred[:len(each_word_pred)-1]
            for each_word_actual in actual[i].split(" "):
                if each_word_actual[-1] == 'S':
                    each_word_actual = each_word_actual[:len(each_word_actual)-1]
                if each_word_actual == each_word_pred:
                    score += 0.2
                    match = True
                    break
        
        ## find char level score ##
        actual_dict = Counter(actual[i])
        pred_dict = Counter(pred[i])
        
        for each_char in actual_dict.keys():
            if each_char in pred_dict.keys():
                pred_dict[each_char] = int(math.fabs(pred_dict[each_char] - actual_dict[each_char]))
            else:
                pred_dict[each_char] = actual_dict[each_char]
        percent = 1 - (sum(pred_dict.values()) / (len(pred[i]) + len(actual[i])))
        score += percent * 0.2
    return score / len(pred)