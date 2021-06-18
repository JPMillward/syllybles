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


directory = "/Users/johnm/Documents/Projects/tenrapsongs/Rebirth/"
text_file = "Look Over Your Shoulder (feat. Kendrick Lamar) by Busta Rhymes.txt"
path = directory + text_file

class SyllySummon():
    
    def __init__(self, file_path):    
        self.raw_text = open(file_path, 'r')
        self.unique_words = []
        self.bars = []
        self.structure = []
    
    def find_all_words(self):
        pattern = re.compile("\\w+'*\w", re.ASCII)
        word_list = re.findall(pattern, self.raw_text.read())
        self.word_list = word_list
        return word_list
    
    def find_unique_words(self):
        self.find_all_words()
        word_series = pd.Series(self.word_list, dtype='string')
        print(word_series)
        unique_words = word_series.str.lower().value_counts().rename_axis('words').reset_index()
        print(unique_words)
        for row in range(len(unique_words)):
            word = unique_words.iloc()[row]['words']
            self.unique_words.append(word)             
        return self.unique_words

    def get_lines(self):
        new_line = re.compile(r"\n")
        for line in self.raw_text:
            clean = re.sub(new_line, "", line)
            if len(line) > 1: self.bars.append(clean)
        return self.bars
    
    def get_breaks(self):
        #Determine how the text is structured.
        #Reliant on a metadata line
        #[Verse/Chorus # - Artist]
        for line in self.bars:
            if line[0] == "[":
                print("Pause for gitpush")
                
        
#print(SyllySummon(path).find_unique_words())

sm = SyllySummon(path)
for line in sm.get_lines():
    print(line)