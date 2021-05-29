import numpy as np
import pandas as pd

#Pathing -- Fix later
file_name = "phoneme_table.xlsx"
directory = "/Users/johnm/Documents/Projects/Syllables/"
full_path = directory + file_name
symbol_table = pd.read_excel(full_path, "Sheet1", index_col = None)
#syllable_table = pd.read_excel(full_path, "Syllables", index_col = None)

class Syllable():   
    def __init__(self, syllable):
        self.syllable = syllable
        #print(f"Syllable object {self.syllable} initiated Successfully")
        
        #To Be Populated
        self.stress = None
        self.onset = ''
        self.nucleus = ''
        self.coda = ''

        if len(self.nucleus) == 0:
            #vprint(f"Detected empty fields. Auto-populating data.")
            Syllable.populate(self)
        
        self.rhyme = self.nucleus + self.coda

    def phoneme_lookup(character, return_request = 'Type', symbol_table = symbol_table):
        #print(f'Searching for match to {character}')
        from_ipa = symbol_table['IPA'] == character
        from_arpa1 = symbol_table['ARPA1'] == character
        from_arpa2 =  symbol_table['ARPA2'] == character
        lookup = symbol_table.loc[from_ipa|from_arpa1|from_arpa2]
        
        if len(lookup) > 0:
            #print(f"{character} is a {return_type}")
            return_type = lookup[return_request].iloc[0] 
            return return_type

        else: 
            print(f'Problem! No match to {character} found.')
            return None

    def process_character(self, character, symbol_type): 
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
                self.stress = Syllable.phoneme_lookup(character, 'ARPA1')
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
        for character in self.syllable:
            symbol_type = Syllable.phoneme_lookup(character)
            Syllable.process_character(self, character, symbol_type)
        print(f"|| Syllable: {self.syllable} || \n| Stress = {self.stress} |\n| Onset = {self.onset} | Nucleus = {self.nucleus} | Coda = {self.coda} |")
        return

x = ['ˈʤuːl','ˈriː','ˌlæps', 'ˈɛ', 'lə', 'fənt', 'moʊ', 'ˈmɛn', 'təm']
for syllable in x:
    test = Syllable(syllable)