import pandas as pd
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer


dataset = pd.read_json('Sarcasm_Headlines_Dataset.json', lines=True)


def find_unique_words(headline):
    # tokenize
    words = word_tokenize(headline)
    # remove stopwords
    stop_words = set(stopwords.words("english"))
    no_stopwords = [w for w in words if w.lower() not in stop_words and len(w) > 2]

    # remove synonyms
    no_synonyms = set()
    for i in no_stopwords:
        synonyms = wordnet.synsets(i)
        if len(synonyms) > 0:
            no_synonyms.add((wordnet.synset(synonyms[0].name()).lemma_names()[0]).lower())
        else:
            no_synonyms.add(i.lower())

    # stem
    stemmed = set()
    ps = PorterStemmer()
    for w in no_synonyms:
        stemmed.add(ps.stem(w))

    return stemmed


def save_unique_words():
    unique_words = set()

    for i in range(len(dataset)):
        # print(i / len(dataset) * 100, "%")
        print(i)
        headline = dataset["headline"][i]
        is_sarcasm = dataset["is_sarcastic"][i]
        stemmed = find_unique_words(headline)
        stemmed = list(stemmed)
        stemmed.append(is_sarcasm)
        # print(stemmed)
        with open('optimized.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(stemmed)
        csvFile.close()

    #     for word in stemmed:
    #         unique_words.add(word)
    #
    # with io.open("unique_words.txt", "w", encoding="utf-8") as f:
    #     for item in unique_words:
    #         if item[0].isdigit():
    #             continue
    #         if item[0] == "'":
    #             f.write(item[1:] + "\n")
    #         else:
    #             f.write(item + "\n")
    #
    # print(len(unique_words))


def train():
    with open('unique_words.txt', 'r') as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    train_lists = list()
    for i in range(len(dataset)):
        print(i / len(dataset) * 100, "%")
        headline = dataset["headline"][i]
        is_sarcastic = dataset['is_sarcastic'][i]
        stemmed = find_unique_words(headline)

        headline_list = [0] * (len(content) + 1)

        for i in stemmed:
            if i in content:
                index = content.index(i)
                headline_list[index] = 1

        headline_list[-1] = is_sarcastic
        # train_list = [headline_list, is_sarcastic]
        train_lists.append(headline_list)

        with open('sarcasm_train_data.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(headline_list)
        csvFile.close()


# test = find_unique_words("man thinks he managed to masturbate without waking roommate")
# knn(list(test), 3)

#Main
# save_unique_words()