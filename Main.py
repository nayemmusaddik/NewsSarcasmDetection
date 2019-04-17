from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer
import csv
from tkinter import *
from tkinter import ttk


class Application(Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.show_content()

    def show_content(self):
        # create instruction label
        Label(self, text="News Sarcasm Detection", font="Helvetica 16 bold italic",
              fg="dark green").grid(column=1, columnspan=3, sticky=W)
        # Entry
        Label(self, text="Enter a New Headline:").grid(row=2, column=0, sticky=W)
        self.varNewHeadline = StringVar()
        Entry(self, textvariable=self.varNewHeadline, width=70).grid(row=2, column=1, columnspan=7, sticky=W)

        # Button
        Button(self, text="Submit", bg="green", fg="White", command=self.getNewHeadline).grid(row=4, column=1,
                                                                                              sticky=NSEW)
        # progressbar
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")

        # Labels
        self.lblSarcasm = Label(self, text="Its Sarcastic", font="Helvetica 10 bold italic", fg="blue", anchor="e")
        self.lblNotSarcasm = Label(self, text="Its Not Sarcastic", font="Helvetica 10 bold italic", fg="blue",
                                   anchor="e")

    def find_unique_words(self, headline):

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

    def knn(self, test_sentence, k):

        with open("optimized.csv", 'r', newline='') as csvfile:
            rows = csv.reader(csvfile)
            self.distance_list = list()
            for row in rows:

                tst = list.copy(test_sentence)
                trained = row[:-1]

                for i in row[:-1]:
                    if i in test_sentence:
                        tst.remove(i)
                        trained.remove(i)

                distance = (len(tst) + len(trained)) ** 0.5
                the_list = [distance, row[-1]]
                self.distance_list.append(the_list)

            csvfile.close()
        self.distance_list.sort()
        self.distance_list = self.distance_list[:k]
        print(self.distance_list)
        print(len(self.distance_list))

        print("Test sarcasm: ", self.distance_list[0][1])
        if self.distance_list[0][1] == "1":
            self.lblNotSarcasm.grid_remove()
            self.lblSarcasm.grid(row=5, columnspan=2)
        elif self.distance_list[0][1] == "0":
            self.lblSarcasm.grid_remove()
            self.lblNotSarcasm.grid(row=5, columnspan=2)

    def getNewHeadline(self):
        self.progress.grid(row=5, columnspan=2)
        self.lblSarcasm.grid_remove()
        self.lblNotSarcasm.grid_remove()
        import time
        self.progress['value'] = 20
        self.update_idletasks()
        time.sleep(1)
        self.progress['value'] = 50
        self.update_idletasks()
        time.sleep(1)
        self.progress['value'] = 80
        self.update_idletasks()
        time.sleep(1)
        self.progress['value'] = 100
        test = self.find_unique_words(self.varNewHeadline.get())
        self.knn(list(test), 3)
        self.progress.grid_remove()


# GUI
root = Tk()
root.title("XYZ Restaurant")
root.geometry("600x400")
app = Application(root)
root.mainloop()
