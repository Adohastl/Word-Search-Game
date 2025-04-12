import os

def preparation(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
        cleanwords = []
        for word in words:            
            cleanwords.append(word.replace("آ", "ا"))
    return(set(cleanwords))
print(preparation("data\\categories\\test.txt"))


# def normalize_word(word):
#     """Normalize words."""
#     return word.replace('آ', 'ا')

# def load_words_from_file(file_path):
#     """Load words from a given file and normalize them."""
#     with open(file_path, 'r', encoding='utf-8') as file:
#         words = [normalize_word(line.strip()) for line in file if len(line.strip()) > 2]
#     return words

# print(load_words_from_file("data\\categories\\animals.txt"))