import nltk
nltk.download('gutenberg')

from nltk.corpus import gutenberg
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
import random

class ngram:
    model = defaultdict(lambda: defaultdict(lambda: 0))
    cur_index=0
    def __init__(self, wordlist):
        self.wordlist=list(wordlist)
        self.listlength=len(wordlist)
        self.wordused=[0]*len(wordlist)
        self.threshold=0.01
    
    def train(self):
        self.model = defaultdict(lambda: defaultdict(lambda: 0))

        for sentence in gutenberg.sents():
            for a, b, c in trigrams(sentence, pad_right=True, pad_left=True):
                if not(a=='None' or b=='None' or c=='None'):
                    if(isinstance(a, str) and isinstance(b, str) and isinstance(c, str)):
                        if not (a.isdigit() or b.isdigit() or c.isdigit()):
                            self.model[(a,b)][c]+=1
                    else:
                        self.model[(a,b)][c]+=1

        for a_b in self.model:
            total=float(sum(self.model[a_b].values()))
            for c in self.model[a_b]:
                self.model[a_b][c]/=total
    
    def starting_bigram(self):
        bigrams=[['She','was'],['It','was'],['She','was'],['I','thought'],['I','have'],['To','be'],['That','is'],['Well',','],['I','was'],['I','wonder']]
        chosen=random.choice(bigrams)
        return chosen
    #safe words: afraid
    def generate(self):
        starting_words=self.starting_bigram()
        cur_word=0
        words_done=0
        sentence_end=0
        cur_bigram=[starting_words[0],starting_words[1]]
        sent=[starting_words[0],starting_words[1]]
        sent_length=0
        self.wordlist.append('edhfjeifkgjrjdf')
        
        while(sentence_end==0):
            new_word=self.choose_word(self.wordlist[cur_word],cur_bigram)
            if (new_word == self.wordlist[cur_word]):
                cur_word+=1
                if (cur_word == self.listlength):
                    words_done=1
            if (new_word=='#END'):
                sentence_end=1
                new_word=' '
            if (words_done == 1):
                if (new_word=='.' or new_word==';' or new_word=='!' or new_word=='?' or new_word=='#END'):
                    sentence_end=1
                    if (new_word == ';' or new_word =='#END'):
                        new_word='.'
            cur_bigram[0]=cur_bigram[1]
            cur_bigram[1]=new_word
            if (new_word is not None):
                sent.append(new_word)
                sent_length+=1
            
            if (sent_length>100):
                sentence_end=1
            self.cur_index=cur_word
        print(sent)
        return sent
            
    def choose_word(self, ourword,cur_bigram):
        ourword_used=0
        chosen_word=''
        bag=[]
        for word in self.model[cur_bigram[0],cur_bigram[1]]:
                if (self.model[cur_bigram[0],cur_bigram[1]].get(word) >= self.threshold):
                    if word==ourword:
                        print(word)
                        chosen_word=word
                        ourword_used=True
                        break
                    if isinstance(word,str):
                        if not word.isdigit():
                            bag.append(word)
        if (ourword_used)==False:
            if (len(bag)==0):
                chosen_word='#END'
            else:
                chosen_word=random.choice(bag)
        #print('Chosen word is',chosen_word)
        return chosen_word
            
    

def generatetext(words):
    a=ngram(words)
    a.train()
    c=0
    text=[]
    while(a.cur_index < a.listlength):
        s=a.generate()
        text.append(s)
        if (c>4):
            break
        c+=1

def translations(words):
    lines=[line.strip() for line in open('Manchu.txt')]
    eng=[]
    man=[]
    translated=[]
    for line in lines:
        a,b=line.split()
        eng.append(a)
        man.append(b)
    for w in words:
        i=eng.index(w)
        if w not in eng:
            i=0
        translated.append(man[i])
        return translated
