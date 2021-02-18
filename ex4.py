from urllib.request import urlopen

import networkx as nx
import string
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from itertools import combinations
import heapq as hq
import json

stop_words = set(stopwords.words('english'))
punctuation_to_remove = string.punctuation + "``" + "''" + "–" + "‘" + "’" + ":" + ";" + "(" + ")" +"“"+ "”" +"—"
from bs4 import BeautifulSoup

urls = {
    "Health": "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
    "Business": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
    "Technology": "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
    "Science": "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
    "Sports": "https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml",
    "World": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "US":"https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "Arts":"https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml",
    "Travel":"https://rss.nytimes.com/services/xml/rss/nyt/Travel.xml",
    "Style":"https://rss.nytimes.com/services/xml/rss/nyt/FashionandStyle.xml"
}

def simple_graph_ranking_from_file(text,d, n_max_iter, n_top_candidates):
    # Splitting it into sentences
    final_cooccurences_list = []
    sentences = sent_tokenize(text)
    for sentence in sentences:
        # Split sentence into word tokens
        word_tokens = list(word_tokenize(sentence))
        # Remove tokens that are just punctuation
        word_tokens_nopunct = [i.lower() for i in word_tokens if i not in punctuation_to_remove]
        # Restore Contractions
        for n, word in enumerate(word_tokens_nopunct):
            if word in ["'s", "'t", "'d", "'ll", "'m", "'ve", "'re", ]:
                word_tokens_nopunct[n - 1] = word_tokens_nopunct[n - 1] + word
                word_tokens_nopunct.pop(n)
        # Remove stopwords
        word_tokens_cleaned = [i for i in word_tokens_nopunct if i not in stop_words]
        # The tokens list already contains the 1-grams, so we use a copy of it and just append to it the 2- and 3- grams
        sent_cooccurence_pairs = word_tokens_cleaned.copy()
        for n in range(2, 4):
            for ngram in ngrams(word_tokens_cleaned, n):
                sent_cooccurence_pairs.append(' '.join(ngram))
        # Create co-occurence pairs by getting all the tuples corresponding to all possible 2-element combinations
        final_cooccurences_list.extend(list(combinations(sent_cooccurence_pairs, 2)))
    # Create the graph and fill it
    g1 = nx.Graph()
    g1.add_edges_from(final_cooccurences_list)
    # Apply pagerank
    PRresults = nx.pagerank(g1, alpha=1 - d, max_iter=n_max_iter)

    # Get the topx results
    topx = hq.nlargest(n_top_candidates, PRresults, key=PRresults.get)

    results = {};
    for token in topx:
        results[token] = PRresults[token]

    return (results)


def getTextAndTitleFromArticle(category, tag):
    url_article = urls[category];
    response = urlopen(url_article).read()
    soup = BeautifulSoup(response, features="html.parser")
    myList = []
    for node in soup.findAll(tag):
        myList.append(node.findAll(text=True))

    if (tag == 'title'):
        return myList[2:len(myList)]
    else:
        return myList[1:len(myList)]

def readTextsAndTransform(array1, array2):
    array = []
    for arr1 in array1:
        string = arr1[0] + "."
        array.append(string)

    for arr2 in array2:
        string2 = arr2[0]
        array.append(string2)

    return array;

def parseDictToJson(dict):
    arr=[]

    for key in dict:
        data ={}
        data["word"] = key
        data["size"] = str(int(dict[key]*13000))
        arr.append(data)

    json_data = json.dumps(arr)
    return json_data

def findAndJsonParseMostTrendingWords(category):
    array_descriptions = getTextAndTitleFromArticle(category, 'description')
    array_titles = getTextAndTitleFromArticle(category, 'title')

    arrayOfExtraction = readTextsAndTransform(array_titles, array_descriptions);
    separator = " "
    text = separator.join(arrayOfExtraction)

    test_result =simple_graph_ranking_from_file(text, 0.15, 50, 50)
    json = parseDictToJson(test_result)

    return json

