import re
import spacy
import pandas as pd
import numpy as np
import json
import random as rand

nlp = spacy.load("en_core_web_md")   # Load language model


pos_list, neg_list = None, None

with open('Datasets/Raw/rt-polarity.pos', 'r') as pos_reader:
    pos_list = pos_reader.readlines()
    
with open('Datasets/Raw/rt-polarity.neg', 'r') as neg_reader:
    neg_list = neg_reader.readlines()


pos_df = pd.DataFrame(data = {'raw_sentence': pos_list, 'tag': ['positive' for _ in pos_list]})
neg_df = pd.DataFrame(data = {'raw_sentence': neg_list, 'tag': ['negative' for _ in neg_list]})

# Combine pos_df & neg_df
comments_df = pos_df.append(neg_df)
comments_df


def clean_sentence(text):

    # Remove leading whitespaces, then convert to Spacy Doc object
    doc = nlp(text.strip())
    
    # Remove punctuations & lemmatize
    stopwords = nlp.Defaults.stop_words
    text = ' '.join([token.lemma_ for token in doc if not token.is_punct])
    
    # Manual mapping
    text = text.replace('n\'t', 'not')

    # Remove other punctuations
    return re.sub('\'s', '', text)

# Clean sentences
comments_df['cleaned_sentence'] = comments_df['raw_sentence'].apply(clean_sentence)


comments_df.to_csv('Datasets/Processed/comments_df.csv', index = False)


comments_df = pd.read_csv('Datasets/Processed/comments_df.csv')
comments_df


pos_unigrams, neg_unigrams, pos_bigrams, neg_bigrams = [], [], [], []

for index, row in comments_df.iterrows():
    
    comment = row['cleaned_sentence']
    tag = row['tag']
    
    if pd.isnull(comment):
        break
    
    # Unigrams
    if tag == 'positive':
        pos_unigrams += comment.split(' ')
    else:
        neg_unigrams += comment.split(' ')
    
    # bigrams
    if tag == 'positive':
        pos_bigrams += [' '.join(bigram) for bigram in zip(comment.split(" ")[:-1], comment.split(" ")[1:])]
    else:
        neg_bigrams += [' '.join(bigram) for bigram in zip(comment.split(" ")[:-1], comment.split(" ")[1:])]


# Get count and store as dictionary
pos_unigrams_dict = pd.Series(pos_unigrams)[10:-10].value_counts().to_dict()
neg_unigrams_dict = pd.Series(neg_unigrams)[10:-10].value_counts().to_dict()

pos_bigrams_dict = pd.Series(pos_bigrams)[10:-10].value_counts().to_dict()
neg_bigrams_dict = pd.Series(neg_bigrams)[10:-10].value_counts().to_dict()

# Save JSONs
with open('Datasets/Processed/vocab.json', 'w') as write:
    output = {
        'pos_unigrams_dict':pos_unigrams_dict,
        'neg_unigrams_dict': neg_unigrams_dict,
        'pos_bigrams_dict': pos_bigrams_dict,
        'neg_bigrams_dict': neg_bigrams_dict
    }
    
    json.dump(output, write)


# Load JSONs
with open('Datasets/Processed/vocab.json', 'r') as read:
    vocab = json.load(read)

pos_unigrams, neg_unigrams, pos_bigrams, neg_bigrams = [vocab[key] for key in vocab.keys()]


def unigram_prob(word, unigrams):
    ''' Calculates probability of the unigram '''
    
    # Just in case
    if word not in unigrams:
        return 0
        
    word_count = unigrams[word]
    unigram_size = len(unigrams)
    return word_count / unigram_size * 10


def bigram_prob(first_word, second_word, alpha, beta, gamma, coefficient, unigrams, bigrams):
    ''' Calculates probability of the bigram '''
    
    bigram = ' '.join([first_word, second_word])
    
    # Alpha prob
    if bigram not in bigrams:
        alpha_prob = 0
    else:
        bigram_count = bigrams[bigram]
        alpha_prob = alpha * (bigram_count / unigrams[first_word]) * 10
    
    # Beta prob
    beta_prob = beta * unigram_prob(second_word, unigrams)
    
    # coefficient
    coef = gamma * coefficient * 10
    
    return alpha_prob + beta_prob + coef


def sentence_prob(sentence, alpha, beta, gamma, coefficient, unigrams, bigrams):
    ''' Calculates probability of the sentence '''
    
    # Clean & get sentence tokens
    cleaned_sentence = clean_sentence(sentence)
    words = cleaned_sentence.split(' ')
    
    # Calculate the first unigram prob
    probability = unigram_prob(words[0], unigrams)
    
    bigrams = [bigram for bigram in zip(cleaned_sentence.split(" ")[:-1], cleaned_sentence.split(" ")[1:])]
    for bigram in bigrams:
        probability *= bigram_prob(bigram[0], bigram[1], alpha, beta, gamma, coefficient, unigrams, bigrams)
        
    return round(probability, 10)


def get_sentiment(sentence, alpha, beta, gamma, coefficient, pos_unigrams, neg_unigrams, pos_bigrams, neg_bigrams):
    ''' Retusn sentiment of the sentence '''
    
    pos_prob = sentence_prob(sentence, alpha, beta, gamma, coefficient, pos_unigrams, pos_bigrams)
    neg_prob = sentence_prob(sentence, alpha, beta, gamma, coefficient, neg_unigrams, neg_bigrams)
    
    sentiment = 'POSITIVE' if (pos_prob > neg_prob) else 'NEGATIVE'
    
    return sentiment, pos_prob, neg_prob


while True:
    
    comment = input()
    
    if comment == 'get_ipython().getoutput("q':")
        break
    
    sentiment = get_sentiment(comment, 0.4, 0.3, 0.3, 0.5, pos_unigrams, neg_unigrams, pos_bigrams, neg_bigrams)
    print(sentiment)


test_case = [
    'loved the movie',                                        # POSITIVE
    'Terrible movie, totally hate it.',                       # NEGATIVE
    'What a waste of time watching this terible movie',       # NEGATIVE    
    'It was fun watching the movie. I was amazing for kids',  # POSITIVE
    'Good movie I really like it',                            # POSITIVE
    'Terrible plot, come one man',                            # NEGATIVE
    'good actors, well played.',                              # POSITIVE    
]

for test in test_case:
    sentiment, pos_prob, neg_prob = get_sentiment(test, 0.5, 0.3, 0.2, 0.29, pos_unigrams, neg_unigrams, pos_bigrams, neg_bigrams)
    print('+' if sentiment == 'POSITIVE' else '-', f'{sentiment} | POS: {pos_prob}\t NEG: {neg_prob}')


# tune_test_case = [
#     'I like the movie',
# ]

# while True:
    
#     r = [rand.random() for i in range(3)]
#     s = sum(r)
#     alpha, beta, gamma = [ i/s for i in r]
    
#     coeffitient = rand.random()
    
#     sentiment, pos_prob, neg_prob = get_sentiment(tune_test_case[0], alpha, beta, gamma, coeffitient, pos_unigrams, neg_unigrams, pos_bigrams, neg_bigrams)
    
#     if sentiment == 'POSITIVE':
#         print('Best Parametes:', alpha, beta, gamma, coeffitient)
#         break









