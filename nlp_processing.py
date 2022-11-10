from operator import ge
import nltk
nltk.download('stopwords')
import os
from tokenize import Number
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

def nlp_processing(searches_df):
  if searches_df.empty:
      print('THERE IS NO FILE')
  else:
    # words like and, then etc.
    stop_words = stopwords.words('english')
    
    # count the full search text
    searches_df_counts = searches_df.value_counts()
    print("all searches counted:", searches_df_counts)
    # split the searches into single words
    split_searches = (searches_df.assign(searches=searches_df['search'].str.split()).explode('searches'))
    
    # drop the column with the full texts
    split_searches.drop('search', axis=1, inplace=True)
    
    # count how many times every single word appears
    split_searches_counts = split_searches.value_counts()
    print('all_words_counted:')
    print(split_searches_counts)
    
    # get a list of all the words counted
    words_counted = split_searches_counts.index.tolist()
    
    # loop through every word, if the word is a stop word, remove it from the dataframe 
    for w in words_counted:
      # if the word is a stop_word
      if w[0] in stop_words:
        print('Stop word to remove:', w[0])
        word_to_drop = str(w[0])
        split_searches_counts_after = split_searches_counts.drop(word_to_drop)
    
    # print the words counted after filtering out stop words
    print('words_counted_filtered:')
    print(split_searches_counts_after)
    return {
      'searches_total_count': searches_df_counts, 
    'total_word_count': split_searches_counts
    }

def main():
    searches_df = pd.read_csv('website_searches.csv')
    nlp_processing(searches_df)

if __name__ == "__main__":
    main()

