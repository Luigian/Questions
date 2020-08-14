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
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    # print(file_words)

    file_idfs = compute_idfs(file_words)
    # print(file_idfs)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))
    # print(query)

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
    print(filenames)
    sys.exit()

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
    tfidfs = dict()
    for filename in files:
        tfidfs[filename] = sum(files[filename].count(word) * idfs[word] 
            for word in query if word in idfs)

    tfidfs_sort = sorted(tfidfs.items(), key=lambda x: x[1], reverse=True)
    filenames = [i[0] for i in tfidfs_sort][:n]

    return filenames


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
