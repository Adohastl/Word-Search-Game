import os

def preparation(file_path): 

    with open(file_path, 'r', encoding='utf-8') as file:
        words = sorted((list(set(file.read().splitlines()))), key= len) #remove duplicate elements and sort by lenght
        
        min_len = len(words[0])
        max_len = len(words[-1])
        word_dict = {length: [] for length in range(min_len, max_len + 1)}
        
        for word in words:
            word_dict[len(word)].append(word)
        
        return list(word_dict.values())
    
print(preparation("data\\categories\\test.txt"))