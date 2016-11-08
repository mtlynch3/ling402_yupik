#!/usr/bin/python3
import sys
import string
import nltk

#create dict
d = {}
with open("ipa.tsv") as ipa:
    for line in ipa:
        line_split = line.split('\t')
        grapheme = line_split[0]
        ipa_char = line_split[1].rstrip()
        if not grapheme.startswith('#') and grapheme != '':
            d[grapheme] = ipa_char

#get graphemes            
graphemes = []
for key in d:
    graphemes.append(key)

#sort graphemes by length
graphemes.sort(key=len, reverse=True)

#input text file
f = sys.stdin.read()
f_words = []
for line in f.splitlines():
    f_words.append(nltk.word_tokenize(line))

#remove punctuation
new_words = []
for line in f_words:
    temp  = []
    for word in line:
        new_str = ""
        for ltr in word:
            if ltr == "’" or ltr.isalpha() == True or ltr == '\'':
                new_str = new_str + ltr
        if len(new_str) > 0:
            temp.append(new_str)
    new_words.append(temp)
f_words = new_words

#do the things
ret = []
for line in f_words:
    temp  = []
    for word in line:
        ret_word = []
        word = word.lower()
        curr_idx = 0
        while curr_idx < len(word):
            if word[curr_idx] == "'" or word[curr_idx] == "’":
                curr_idx = curr_idx + 1
                continue
            didFind = False
            for g in graphemes:
                if word.find(g, curr_idx) == curr_idx:
                    ret_word.append(g)
                    curr_idx = curr_idx + len(g)
                    didFind = True
                    break
            if didFind == False:
                ret_word.append(word[curr_idx])
                curr_idx = curr_idx + 1
        temp.append(ret_word)
    ret.append(temp)

#output
for line in ret:
    for word in line:
        print(word, end=" ")
    print()
