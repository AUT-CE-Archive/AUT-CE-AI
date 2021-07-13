import re
import spacy
import pandas as pd
import json

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


unigrams, bigrams = [], []

for index, row in comments_df.iterrows():
    
    comment = row['cleaned_sentence']
    
    if pd.isnull(comment):
        break
    
    # Unigrams
    unigrams += comment.split(' ')
    
    # bigrams
    bigrams += [' '.join(bigram) for bigram in zip(comment.split(" ")[:-1], comment.split(" ")[1:])]


# Get count and store as dictionary
unigrams_dict = pd.Series(unigrams).value_counts().to_dict()
bigrams_dict = pd.Series(bigrams).value_counts().to_dict()

# Save JSONs
with open('Datasets/Processed/unigrams_dict.json', 'w') as write:
    json.dump(unigrams_dict, write)
    
with open('Datasets/Processed/bigrams_dict.json', 'w') as write:
    json.dump(bigrams_dict, write)


# Load JSONs
with open('Datasets/Processed/unigrams_dict.json', 'r') as read:
    unigrams_dict = json.load(read)
    
with open('Datasets/Processed/bigrams_dict.json', 'r') as read:
    bigrams_dict = json.load(read)


def unigram_prob(word):
    
    # Just in case
    if word not in unigrams_dict:
        return 1
        
    word_count = unigrams_dict[word]
    unigram_size = len(unigrams_dict)
    return word_count / unigram_size


def bigram_prob(first_word, second_word, alpha, beta, gamma, coefficient):
    
    bigram = ' '.join([first_word, second_word])
    
    # Alpha prob
    if bigram not in bigrams_dict:
        alpha_prob = 1
    else:
        bigram_count = bigrams_dict[bigram]
        alpha_prob = alpha * (bigram_count / unigrams_dict[first_word])
    
    # Beta prob
    beta_prob = beta * unigram_prob(second_word)
    
    # coefficient
    coef = gamma * coefficient
    
    return alpha_prob + beta_prob + coef


def sentence_prob(sentence, alpha, beta, gamma, coefficient):
    
    # Clean & get sentence tokens
    cleaned_sentence = clean_sentence(sentence)
    words = cleaned_sentence.split(' ')
    
    # Calculate the first unigram prob
    probability = unigram_prob(words[0])
    
    bigrams = [bigram for bigram in zip(cleaned_sentence.split(" ")[:-1], cleaned_sentence.split(" ")[1:])]
    for bigram in bigrams:
        probability *= bigram_prob(bigram[0], bigram[1], alpha, beta, gamma, coefficient)
        
    return round(probability * 0.5, 10)


sentence_prob('why did you make me do this?', 0.4, 0.3, 0.3, 0.5)


while True:
    
    comment = input()
    
    if comment == 'get_ipython().getoutput("q':")
        break
    
    prob = sentence_prob(comment, 0.4, 0.3, 0.3, 0.5)
    print(prob)












