import os

def preparation(file_path): 

    with open(file_path, 'r', encoding='utf-8') as file:
        words = sorted((list(set(file.read().splitlines()))), key= len) #remove duplicate elements and sort by lenght
        
        wordssorted = []
        current_strike = []
        current_length = len(words[0])

        for word in words:
            if len(word) == current_length:
                current_strike.append(word)
            else:
                if current_strike:
                    wordssorted.append(current_strike)
                current_strike = [word]
                current_length = len(word)
        if current_strike:
            wordssorted.append(current_strike)

    return wordssorted

print(preparation("data\\categories\\test.txt"))