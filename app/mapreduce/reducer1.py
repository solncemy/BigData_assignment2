#!/usr/bin/env python3
import sys
from collections import defaultdict

def main():
    current_term = None
    doc_freq = 0
    term_docs = []
    
    for line in sys.stdin:
        term, doc_id, freq, doc_length = line.strip().split('\t')
        
        if current_term != term:
            if current_term is not None:
                # Emit term statistics
                print(f"{current_term}\t{doc_freq}\t{','.join(term_docs)}")
            current_term = term
            doc_freq = 0
            term_docs = []
            
        doc_freq += 1
        term_docs.append(f"{doc_id}:{freq}:{doc_length}")
    
    if current_term is not None:
        print(f"{current_term}\t{doc_freq}\t{','.join(term_docs)}")

if __name__ == "__main__":
    main()