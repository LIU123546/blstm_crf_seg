# coding=utf-8

'''
Some simple utility functions used for Chinese word segmentation
for python 3.x
'''
import torch
import pdb

def label2len(label):
    out = [0] * len(label)
    l = 0
    for i in range(len(label)-1, -1, -1):
        l += 1
        if label[i] == 0 or label[i] == 1:
            out[i] = l
            l = 0
    return out


#calculate the precission, recall, F1_measure
def calculatePRF(pred_y, y, beta = 1.0):
    true_word_count = 0
    test_word_count = 0
    right = wrong = 0
    for y1, y2 in zip(pred_y, y):
        #y1 = y1[1:-1]
        y1 = label2len(y1)
        y2 = label2len(y2)
        assert len(y1) == len(y2)
        for i in range(len(y1)):
            if y1[i]: test_word_count += 1
            if y2[i]: true_word_count += 1
            if y2[i] > 0 and y1[i] == y2[i]: right += 1
    if right == 0:
        p = r = f = 0.0
    else:
        p = 1.0 * right / test_word_count
        r = 1.0 * right / true_word_count
        f = (1+beta)*p*r / (beta*p+r)
    return p, r, f

def visualize(packed_sent_seq, packed_tag_seq, ix_to_word, ix_to_tag, idx_unsort, words):
    '''
    将每个batch中句子的分词结果按照在原语料中的顺序(利用idx_unsort)
    以一行一句的方式打印出来
    '''
    padded_tag_seq, seq_lengths = torch.nn.utils.rnn.pad_packed_sequence(
        packed_tag_seq, batch_first=True, padding_value=0)
    padded_sent_seq, seq_lengths = torch.nn.utils.rnn.pad_packed_sequence(
        packed_sent_seq, batch_first=True, padding_value=0)
    for i, idx in enumerate(idx_unsort):
        sent_seq = padded_sent_seq[idx][:seq_lengths[idx]]
        tag_seq = padded_tag_seq[idx][:seq_lengths[idx]]
        for j, (word, tag) in enumerate(list(zip(sent_seq, tag_seq))):
            if ix_to_tag[tag.item()] in ['S', 'E'] and j < seq_lengths[idx] - 1:
                print(ix_to_word.get(word.item()) if ix_to_word.get(word.item())!="[UNK]" else words[i][j], end="  ")
            elif ix_to_tag[tag.item()] in ['B', 'M'] or j == seq_lengths[idx] - 1:
                print(ix_to_word.get(word.item()) if ix_to_word.get(word.item())!="[UNK]" else words[i][j], end="")
            else:
                print(words[i][j]+"(\\unk_tag)",end="")
        print()

def is_Chinese_char(uchar):
    '''
    判断一个Unicode字符是否为中文字符（可能不完全）
    '''
    if len(uchar) != 1:
        raise TypeError('expected a character, but a string found!')
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5' or uchar in '，。、；‘’“”：？！【】《》（）＜＞￥':
        return True  
    else:  
        return False 

def is_digit(uchar):
    '''
    判断一个Unicode字符是否为数字
    '''
    if len(uchar) != 1:
        raise TypeError('expected a character, but a string found!')
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

def is_alpha(uchar):
    '''
    判断一个Unicode字符是否为字母
    '''
    if len(uchar) != 1:
        raise TypeError('expected a character, but a string found!')
    if (uchar >= u'\u0041' and uchar <= u'\u005a' 
    or uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False  

if __name__ == "__main__":
    teststr = "这是1个中文字符串的测试，看一看Python3中对于Unicode字符串的处理"
    for uchar in teststr :
        print(uchar, end=" ")
    print()
    for uchar in teststr:
        if is_Chinese_char(uchar):
            print("C ", end=" ")
        elif is_digit(uchar):
            print("D", end=" ")
        elif is_alpha(uchar):
            print("A", end=" ")
    
