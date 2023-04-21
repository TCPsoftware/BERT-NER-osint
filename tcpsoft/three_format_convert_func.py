import re
import json
from tcpsoft import common_func as func


def token_json_2_txt(input_filename, output_filename, return_obj=False):
    list_json_obj = func.get_json(input_filename)
    txt_str = ""
    for sentence_tuple in list_json_obj:
        words = sentence_tuple[0].split(" ")
        tokens = sentence_tuple[1].split(" ")
        if len(sentence_tuple) >= 3:
            source = sentence_tuple[2]  # 此句子的，来源文件
        else:
            source = "none."
        if len(words) != len(tokens):
            print("len(words) != len(tokens)")
            print("source: " + source)
        for index in range(len(words)):
            txt_str += (words[index]+" "+tokens[index]+"\n")
            # out_f.write(words[index]+" "+tokens[index]+"\n")
        txt_str += "\n"
        # out_f.write("\n")
    if return_obj:
        return txt_str
    with open(output_filename, "w", encoding="utf8") as out_f:
        out_f.write(txt_str)


def txt_2_token_json(input_filename, output_filename, return_obj=False):
    with open(input_filename, 'r', encoding='utf8') as in_f:
        txt_lines = in_f.readlines()
    queue_word = []
    queue_token = []
    json_obj = []
    for line in txt_lines:
        line = line.strip()
        if line == "" and len(queue_token) != 0:
            json_obj.append([" ".join(queue_word), " ".join(queue_token)])
            queue_word = []
            queue_token = []
        elif line == "" and len(queue_token) == 0:
            pass
        else:
            line = re.sub(' +', ' ', line).strip()
            splits = line.split(' ')
            # splits = line.split('\t')
            # if len(splits_1) > 1:
            #     splits = splits_1
            # splits_2 = line.split('\t')
            # if len(splits_2) > 1:
            #     splits = splits_2
            word = splits[0]
            token = splits[1]
            # word = splits[0]
            # token = splits[2]
            queue_word.append(word)
            queue_token.append(token)
    if queue_word != [] or queue_token != []:
        json_obj.append([" ".join(queue_word), " ".join(queue_token)])
        queue_word = []
        queue_token = []
    if return_obj:
        return json_obj
    func.write_obj_to_json(json_obj, output_filename)

def check_two(label_dict):
    for i in label_dict["label"]:
        for j in label_dict["label"][i]:
            if len(label_dict["label"][i][j]) >= 2:
                return True
            else:
                return False

def token_json_2_span_json(input_filename, output_filename, return_obj=False):
    token_json_obj = func.get_json(input_filename)
    json_arr = []
    for sentence_tuple in token_json_obj:
        words = sentence_tuple[0].split(" ")
        tokens = sentence_tuple[1].split(" ")
        if len(sentence_tuple) >= 3:
            source = sentence_tuple[2]  # 此句子的，来源文件
        else:
            source = "none."
        if len(words) != len(tokens):
            print("len(words) != len(tokens)")
            print("source: " + source)
        full_sentence = ""
        label_dict = {"text": "", "label": {}}
        token_queue = []  # {"word", "label", len_before, len_after}
        def process_queue(token_queue=token_queue):
            index_begin = 0  #####
            index_end = 0  #####
            index_array = []
            label = ""
            text = ""
            for i in token_queue:
                i_word = 0
                i_label = 1
                i_begin = 2
                i_end = 3
                text += i[i_word]
                if label == "":  # 设置label
                    label = i[i_label][2:]
                elif label != i[i_label][2:]:
                    print("label not match...")
                    input(str(token_queue))
                    return 
                if index_begin == 0 and index_end == 0:  # 设置起止
                    index_begin = i[i_begin]
                    index_end = i[i_end]
                elif index_end == i[i_begin]:
                    index_end = i[i_end]
                else:
                    print("index not match...")
                    input(str(token_queue))
                    return 
                # index_array.append([i[i_begin], i[i_end]])
            index_array.append([index_begin, index_end])
            if label != "":
                if label not in label_dict["label"].keys():
                    label_dict["label"][label] = {}
                if text not in label_dict["label"][label].keys():
                    label_dict["label"][label][text] = []
                label_dict["label"][label][text] += index_array
            token_queue.clear()
        for index in range(len(words)):
            len_before = len(full_sentence)
            full_sentence += words[index]
            len_after = len(full_sentence)
            if tokens[index][0] == 'B':
                process_queue()  # process
                token_queue.append([words[index], tokens[index], len_before, len_after])
            elif tokens[index][0] == "I":
                token_queue.append([words[index], tokens[index], len_before, len_after])
            elif tokens[index] == "O":
                process_queue()  # process
                token_queue.append([words[index], tokens[index], len_before, len_after])
            elif tokens[index][0] == "E":
                token_queue.append([words[index], tokens[index], len_before, len_after])
            elif tokens[index][0] == "S":
                process_queue()  # process
                token_queue.append([words[index], tokens[index], len_before, len_after])
            else:
                raise ValueError("Invalid tag:", str([words[index], tokens[index], len_before, len_after]))
        label_dict["text"] = full_sentence
        # if check_two(label_dict)==True:
        #     input('''手工断点：label_dict["text"] = full_sentence''')
        json_arr.append(label_dict)
    if return_obj:
        return json_arr
    else:
        for i in range(len(json_arr)):
            if i == 0:
                func.write_obj_to_json(json_arr[i], output_filename, indent=None, end="\n")
            else:
                func.append_obj_to_json(json_arr[i], output_filename, indent=None, end="\n")


def span_json_2_token_json(input_filename, output_filename, return_obj=False):
    with open(input_filename, "r", encoding="utf8") as sj_f:
        span_json_lines = sj_f.readlines()
    token_json_obj = []
    for json_line in span_json_lines:  # 一个json
        json_obj = json.loads(json_line)
        full_text = json_obj["text"]
        full_labels = json_obj["label"]
        import re
        word_arr = re.findall(".", full_text)
        label_arr = ["O"]*len(full_text)
        for a_label in full_labels.keys():  # 一类label
            entities_dict = full_labels[a_label]
            for a_entity in entities_dict.keys():  # 一个text
                index_list_list = entities_dict[a_entity]
                index_begin = 0
                index_end = 0
                for index_tuple in index_list_list:  # 检查index二维数组的连续性
                    if index_begin == 0 and index_end == 0:  # 设置起止
                        index_begin = index_tuple[0]
                        index_end = index_tuple[1]
                    elif index_end == index_tuple[0]:
                        index_end = index_tuple[1]
                    else:
                        print("index not match...")
                        input(str(a_entity))
                        return
                if full_text[index_begin: index_end] != a_entity:  # index出现偏差
                    print("index not match entity:")
                    input(str(json_line))
                    return 
                if index_end-index_begin == 1:
                    prefix = "S-"
                    postfix = "S-"
                else:
                    prefix = "B-"
                    postfix = "E-"
                for i in range(index_begin, index_end):
                    label_arr[i] = "I-" + a_label
                label_arr[index_begin] = prefix + a_label
                label_arr[index_end-1] = postfix + a_label
        token_json_obj.append([" ".join(word_arr), " ".join(label_arr)])
    if return_obj:
        return token_json_obj
    func.write_obj_to_json(token_json_obj, output_filename)

