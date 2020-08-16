# Questions

<img src="resources/images/questions_output.jpg" width="1000">

Write an AI to answer questions
Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions.
we’ll design a very simple question answering system based on inverse document frequency.

Our question answering system will perform two tasks: document retrieval and passage retrieval. Our system will have access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. Once the top documents are found, the top document(s) will be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

How do we find the most relevant documents and passages? To find the most relevant documents, we’ll use tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. Once we’ve found the most relevant documents, there many possible metrics for scoring passages, but we’ll use a combination of inverse document frequency and a query term density measure (described in the Specification).

## Highlights

* The goal of this project was to write an AI to parse sentences, print their syntax tree, and extract noun phrases.

* A common task in natural language processing is parsing, the process of determining the structure of a sentence. 

* Knowing the structure of a sentence can help a computer to extract information out of it, like the noun phrases, which is useful to get an understanding for what the sentence is about.

* The context-free grammar formalism allow us to parse English sentences via a technique called Rewriting Rules, which means replacing one symbol with other symbol or symbols.

## Rewriting Rules Guide

|Non-Terminal Symbol|Word or Phrase Class|
|----|-----------|
|`S`|Sentence|
|`N`|Noun|
|`V`|Verb|
|`Det`|Determiner|
|`Adj`|Adjective|
|`Adv`|Adverb|
|`P`|Preposition|
|`Conj`|Conjugation|
|`NP`|Noun Phrase|
|`VP`|Verb Phrase|
|`AdjP`|Adjective Phrase|
|`AdvP`|Adverb Phrase|
|`PP`|Preposition Phrase|
|`ConjP`|Conjugation Phrase|

* By defining a set of rules, the CYK algorithm, used by the `parse` method from the nltk library, is able to take a sentence (terminal symbols) and figure out the syntax tree (the structure of the non-terminal symbols).

* According to how well the rules are established, this algorithm can prevent the generation of non-well formed sentences, but it can't detect some sentences that may not be semantically well-formed (non-sense sentences).

* The more rules are implemented, the more complex sentences it can parse.

* Since English grammar is inherently ambiguous, the same sentences can produce more than one syntax structure.

## Implementation

### preprocess 

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
* [CS50 AI Language Lecture][cs50 lecture]
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
