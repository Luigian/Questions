import nltk
import sys
import os
import string
from nltk.corpus import stopwords
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")
    
    # Calculate IDF values across files
    print("Loading data...")
    files = load_files(sys.argv[1])
    print("Extracting words from corpus...")
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    print("Calculating inverse document frequencies...")
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    print("Finding top files matches...")
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    print("Finding top sentences matches...")
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            files[filename] = f.read()
            
    return files
    

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order. Process document by coverting all words 
    to lowercase, and removing any punctuation or English stopwords.
    """
    punctuations = """"!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~–—"""
    for c in document:
        if c in punctuations:
            document = document.replace(c, " ")
    
    tokens = []
    for word in nltk.word_tokenize(document.lower()):
        if word not in stopwords.words('english'):
            tokens.extend([word])
    tokens.sort()
    
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values. Any word
    that appears in at least one of the documents should be in the resulting dictionary.
    """
    words = set()
    for filename in documents:
        words.update(documents[filename])
    
    idfs = dict()
    for word in words:
        f = sum(word in documents[filename] for filename in documents)
        idf = math.log(len(documents) / f)
        idfs[word] = idf
    
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranks = dict()
    for filename in files:
        ranks[filename] = sum(files[filename].count(word) * idfs[word] 
            for word in query if word in idfs)

    sorted_ranks = sorted(ranks, key=lambda f: ranks[f], reverse=True)[:n]

    return sorted_ranks


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranks = dict()
    for sentence in sentences:
        # Matching word measure
        mwm = sum(idfs[word] for word in query if word in sentences[sentence])
        # Query term density
        qtd = sum(word in query for word in sentences[sentence]) / len(sentences[sentence])
        ranks[sentence] = {"mwm": mwm, "qtd": qtd} 
    
    sorted_ranks = sorted(ranks, key=lambda s: (ranks[s]["mwm"], ranks[s]["qtd"]), reverse=True)[:n]
    
    return sorted_ranks


if __name__ == "__main__":
    main()
