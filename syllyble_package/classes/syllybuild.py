import pandas as pd
from syllyble_package.classes.methods import phoneme_lookup

class SyllyBuild():   
    def __init__(self, syllable):
        self.syllable = syllable
        #print(f"Syllable object {self.syllable} initiated Successfully")
        
        #To Be Populated
        self.stress = None
        self.onset = ''
        self.nucleus = ''
        self.coda = ''

        if len(self.nucleus) == 0:
            print(f"Detected empty fields. Auto-populating data.")
            self.populate()
        
        self.rhyme = self.nucleus + self.coda

    def process_character(self, character, symbol_type): 
        lookup = phoneme_lookup
        #print(f"{character} is a {symbol_type}")
        #Suprasegmental Logic
        if symbol_type == 'suprasegmental':
            if len(self.nucleus) != 0:
                self.nucleus += character

            elif len(self.onset) != 0:
                self.onset += character
    
        #Break Specific Logic
        if symbol_type == 'break':
            if len(self.onset) == 0:
                #print(f"{character} begins the syllable.")
                self.stress = lookup(character, 'ARPA1')
                #print(f"Stress : {self.stress}")
            else:
                print(f"Reached a syllable break. You should not be seeing this message.")
                
        if symbol_type == 'vowel':
            if len(self.nucleus) == 0:
                #print(f'{character} is the beginning of the nucleus')
                self.nucleus += character
            
            elif len(self.coda) == 0:
                self.nucleus += character
                #print(f"Added vowel ({character}) to nucleus.")
            else: print(f"Anomaly found. Please log.")
                
        if symbol_type == 'consonant':
            #print(f'{character} is a consonant')
            if len(self.nucleus) == 0:
                #print(f"Adding consonant ({character}) to onset.")
                self.onset += character
            elif len(self.nucleus) != 0:
                #print(f"Adding consonant ({character}) to coda.")
                self.coda += character
        
    def populate(self):
        lookup =  phoneme_lookup
        for character in self.syllable:
            symbol_type = lookup(character)
            self.process_character(character, symbol_type)
        print(f"|| Syllable: {self.syllable} || \n| Stress = {self.stress} |\n| Onset = {self.onset} | Nucleus = {self.nucleus} | Coda = {self.coda} |")
        return