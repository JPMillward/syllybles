"""
Input Processing Needs
1. Read in input
2. Find every unique word
3. Check each against database to see if we have it or don't
    3a. If it exists, cache data, do nothing else
4. Search the Webster API for anything new
5. Store the data in datatable

"""
import re
import pandas as pd

class SyllySummon():
    
    def __init__(self, file_path):
        self.raw_text = open(file_path, 'r').read()
        self.lines = open(file_path, 'r').readlines()
        #print(self.lines)
        self.unique_words = []
        self.bars = []
        self.structure = []
        self.get_lines()
        self.find_all_words()
    
    def find_all_words(self):
        pattern = re.compile(r"\w+'*\w", re.ASCII)
        word_list = re.findall(pattern, self.raw_text)
        #print(word_list)
        self.word_list = word_list
        return word_list
    
    def get_unique_words(self)  :
        self.get_unique_count()
        for row in range(len(self.unique_word_count)):
            word = self.unique_word_count.iloc()[row]['words']
            self.unique_words.append(word)             
        return self.unique_words
    
    def get_unique_count(self):
        word_series = pd.Series(self.word_list, dtype='string')
        self.unique_word_count = word_series.str.lower().value_counts().rename_axis('words').reset_index()
        return self.unique_word_count

    def get_lines(self):
        new_line = re.compile(r"\n")
        for line in range(len(self.lines)):
            #print(self.lines[line])
            clean = re.sub(new_line, "", self.lines[line])
            if len(self.lines[line]) > 1: self.bars.append(clean.lower())
            self.get_structure(self.lines[line])
        return self.bars
    
    def get_structure(self, line):
        section = {}
        starting_bar = len(self.bars)
        if starting_bar - 1 > 1:
            self.structure[len(self.structure)-1].update({"end" : starting_bar - 2})
        if line[0] != "[" : return
        
        feature = line.find(":")
        shared = line.find("&")
        if feature > 0:
            stanza = line[1:feature]
            artist = [line[feature+2:-2]] if shared < 0 else [line[feature+2:shared-1], line[shared+1:-2]]
            section.update({"stanza" : stanza, "artist" : artist, "start" : starting_bar})
        else: section.update({"stanza" : line[1:-2]})
        self.structure.append(section)
        return
    
    def get_stanza(self, stanza_number, header = False):
        struct = self.structure[stanza_number]
        start = struct['start']
        end = struct['end']
        return self.bars[start:end] if header == False else self.bars[start-1:end]
        