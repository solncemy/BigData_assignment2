#!/usr/bin/env python3
import sys
import re
from collections import defaultdict

def tokenize(text):
    # Convert to lowercase and split into words
    words = re.findall(r'\w+', text.lower())
    return words

def main():
    for line in sys.stdin:
        parts = line.strip().split('\t')
        if len(parts) != 3:
            continue
            
        doc_id, title, text = parts
        
        words = tokenize(text)
        
        term_freq = defaultdict(int)
        for word in words:
            term_freq[word] += 1
            
        for term, freq in term_freq.items():
            print(f"{term}\t{doc_id}\t{freq}\t{len(words)}")

if __name__ == "__main__":
    main()