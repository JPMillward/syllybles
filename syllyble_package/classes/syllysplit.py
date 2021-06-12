from syllyble_package.classes.methods import phoneme_lookup
#print('***LOADED SyllySplit***')


class SyllySplit():

    def __init__(self, ipa_word):
        self.root = ipa_word
        self.stems = []
        self.split()
    
    def get_list(self):
        syllable_list = []
        for item in self.stems: syllable_list.append(item)
        return syllable_list

    def split(self):
        syllable = ''
        lookup = phoneme_lookup
        
        for i in range(len(self.root)):
            current = self.root[i]
            phoneme_type = lookup(current)
            #print(f'{current} is {i+1} of {len(self.root)}')
            
            ###Process Breaks###            
            if phoneme_type == 'break':
                if i != 0:
                    #print(f'{current} is a break')
                    self.stems.append(syllable)
                    syllable = self.root[i]
                else:
                   #print(f'{current} is the First Character')
                   syllable = self.root[i]
            
            ###Proceess Suprasegmentals###
            elif phoneme_type == 'suprasegmental':
                if len(self.root) - i > 2:
                    next = lookup(self.root[i+1])
                    third = lookup(self.root[i+2])
                    if third == 'vowel':
                        #print('Reached a syllable break')
                        if next == 'consonant':
                            syllable += self.root[i]
                            self.stems.append(syllable)
                            syllable = ''
                        else: syllable += current
                    else: syllable += current
                else: syllable += current
                
                #print(f'{current} is a suprasegmental')
            elif phoneme_type == 'consonant':
                #print(f"{current} is a consonant")
                
                if len(self.root) != i + 1 and i != 0:
                    next_char = lookup(self.root[i+1])
                    prev_char = lookup(self.root[i-1])
                    if next_char == 'vowel' and prev_char == "consonant":
                        if i - 2 >= 0:
                            back_char = lookup(self.root[i-2])
                            if back_char == 'break':
                                #print(f'{self.root[i]} is part of the current syllable.')
                                None
                            else:
                                #print(f'{current} begins the next syllable.')
                                self.stems.append(syllable)
                                syllable = ''
        
                syllable += self.root[i]
                #print(syllable)

            ###Process Vowels###
            elif phoneme_type == 'vowel':
                #print(f"{self.root[i]} is a vowel")
                if len(self.root) - i > 2:
                    next = lookup(self.root[i+1])
                    third = lookup(self.root[i+2])
                    if 'vowel' == phoneme_type == third:
                        if next == 'consonant' :
                            #print("This is the end of the syllable")
                            syllable += self.root[i]
                            self.stems.append(syllable)
                            #print(f"current stems: {self.stems}")

                            syllable = ''
                        else:
                            #print(f"Adding {current} to syllable {syllable}")
                            syllable += current
                    else: syllable += current
                else: syllable += current
            
            ###Process Liquids###
            elif phoneme_type == 'liquid' or current == '̩':
                
                print("{current} is a liquid! Wowwww")
                print(f"Splitting syllable and appending {syllable[:-2]}")
                print(f"Test {syllable[-2:]}")
                self.stems.append(syllable[:-2])
                syllable = syllable[-2:] + current
                            
        self.stems.append(syllable)
        return self.stems