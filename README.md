# Questions

## An AI to answer questions

<img src="resources/images/questions_output.jpg" width="1000">

Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions. 

This is a question answering system based on **inverse document frequency** that will perform two tasks: document retrieval and passage retrieval.

First, the system will have access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. To find the most relevant documents, we’ll use tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. 

Then, once the top documents are found, passage retrieval will subdivide the top document(s) into passages (in this case, sentences) and score them using a combination of inverse document frequency and a query term density measure, so that the most relevant passage to the question can be determined.

## Implementation

In the main function, we first load the files from the corpus directory into memory (via the `load_files` function). Each of the files is then tokenized (via `tokenize`) into a list of words, which then allows us to compute inverse document frequency values for each of the words (via `compute_idfs`). The user is then prompted to enter a query. The `top_files` function identifies the files that are the best match for the query. From those files, sentences are extracted, and the `top_sentences` function identifies the sentences that are the best match for the query.

### load_files

* The load_files function accepts the name of a directory and return a dictionary mapping the filename of each .txt file inside that directory to the file’s contents as a string.

* On macOS, the `/` character is used to separate path components, while the `\` character is used on Windows. By using `os.path.join`, this function is platform-independent, it works regardless of operating system.

* In the returned dictionary, there's one key named for each .txt file in the directory. The value associated with that key is a string (the result of reading the corresponding file).

### tokenize



### compute_idfs
### top_files
### top_sentences
The preprocess function accept a string as input and return a lower cased list of its words. 
The following methods are implemented inside this function: 
* nltk’s `word_tokenize()` - Perform tokenization (split the string into words).
* `lower()` - Convert all characters to lowercase.
* `isalpha()` - Remove any word that does not contain at least one alphabetic character.

### non-terminals global variable

This is a set of context-free grammar rules that, when combined with the rules in the `TERMINALS` global variable, allow the parsing of all sentences in the `sentences` directory.

Constraints: 
* Avoid over-generation of sentences, sentences like "Armchair on the sat Holmes" aren't meant to be accepted by the parser.
* Avoid  under-generation of sentences. A very long and specific rule like `(S -> N V Det Adj Adj Adj N P Det N P Det N)` would technically successfully generate sentence 10, but isn't useful or generalizable.
* Try to be as general as possible without over-generating. The parser should accept the sentences: “Holmes sat in the armchair”, “Holmes sat in the red armchair” and “Holmes sat in the little red armchair”, but not the sentence: “Holmes sat in the the armchair”.

### np_chunk

The np_chunk function accept a tree representing the syntax of a sentence (nltk.tree object) and return a list of all the noun phrase chunks in the sentence tree.
A noun phrase chunk is defined as any subtree of the sentence whose label is "NP" that does not itself contain any other noun phrases as subtrees.
The following methods are implemented inside this function in order to manipulate the nltk.tree object:
* nltk’s `subtrees()` - Generate all the subtrees of a tree, optionally restricted to trees matching the filter function.
* nltk’s `label()` - Return the node label of the tree.

## Resources
* [Language - Lecture 6 - CS50's Introduction to Artificial Intelligence with Python 2020][cs50 lecture]
* [How to Clean Text for Machine Learning with Python][clean text]
* [Python | Nested Dictionary][nested dictionary]
* [Breaking Ties: Second Sorting][second sorting]

## Installation
Inside of the `questions` directory:

* `pip3 install -r requirements.txt` | Install this project’s dependency: nltk for natural language processing.

## Usage
Inside of the `questions` directory:

* `python3 questions.py corpus` | Accepts the corpus of documents via a directory, and the query via user input.

## Credits
[*Luis Sanchez*][linkedin] 2020.

A project from the course [CS50's Introduction to Artificial Intelligence with Python 2020][cs50 ai] from HarvardX.

[cs50 lecture]: https://youtu.be/_hAVVULrZ0Q?t=4158
[clean text]: https://machinelearningmastery.com/clean-text-machine-learning-python/
[nested dictionary]: https://www.geeksforgeeks.org/python-nested-dictionary/
[second sorting]: https://runestone.academy/runestone/books/published/fopp/Sorting/SecondarySortOrder.html
[linkedin]: https://www.linkedin.com/in/luis-sanchez-13bb3b189/
[cs50 ai]: https://cs50.harvard.edu/ai/2020/
