import gzip
import re
from collections import defaultdict

def simple_stem(word):
    # Improved stemming function (still basic but tailored for this use case)
    suffixes = ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']
    # Order by length of suffix so that we match the longest suffix first
    suffixes = sorted(suffixes, key=len, reverse=True)
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word

word_freqs = defaultdict(int)
word_docs_counts = defaultdict(set)

# Consider checking the actual file size to see if this should be causing concern.
print('Starting to process the dataset...')
with gzip.open('tiny_wikipedia.txt.gz', 'rt', encoding='utf-8') as file:
    for line in file:
        words = re.findall(r'\b(\w+)\b', line)
        words = [word for word in words if not re.match(r'https?://', word)]
        stemmed_content = set()
        
        for word in words:
            word = word.lower()
            stemmed_word = simple_stem(word)
            word_freqs[stemmed_word] += 1
            stemmed_content.add(stemmed_word)

        # Assumes the URL is the first token in the line
        doc_url = line.split(maxsplit=1)[0]
        for stemmed_word in stemmed_content:
            word_docs_counts[stemmed_word].add(doc_url)

# No need to sort word_freqs.keys() each time - do it once and store it
sorted_word_keys = sorted(word_freqs.keys())
word_to_code = {word: i for i, word in enumerate(sorted_word_keys)}

# Now write the results to dictionary.txt and unigrams.txt
print('Writing files...')
with open('dictionary.txt', 'w') as dict_file:
    for word in sorted_word_keys:
        dict_file.write(f"{word}\n")

with open('unigrams.txt', 'w') as uni_file:
    for word in sorted(sorted_word_keys, key=lambda w: -word_freqs[w]):
        doc_freq = len(word_docs_counts[word])
        global_freq = word_freqs[word]
        word_code = word_to_code[word]
        uni_file.write(f"{word_code} {word} {doc_freq} {global_freq}\n")

print('Finished processing.')