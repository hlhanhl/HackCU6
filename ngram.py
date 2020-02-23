import nltk
nltk.download('gutenberg')

from nltk.corpus import gutenberg
from nltk import bigrams, trigrams
from collections import Counter, defaultdict
import random



model = defaultdict(lambda: defaultdict(lambda: 0))

for sentence in gutenberg.sents():
    for a, b, c in trigrams(sentence, pad_right=True, pad_left=True):
        if not(a=='None' or b=='None'):
            model[(a,b)][c]+=1

count=0
for a_b in model:
    total=float(sum(model[a_b].values()))
    for c in model[a_b]:
        model[a_b][c]/=total

    
#print(dict(model['She', 'was']))
#cut off point: 0.005 

sentence_end=False
sentence=['She','was']
cur_bigram=['She','was']
count=0

#safe words: afraid

ourword='fear'
ourword_used=False
while(sentence_end==False):
    bag=[]
    for word in model[cur_bigram[0],cur_bigram[1]]:
        if (model[cur_bigram[0],cur_bigram[1]].get(word) > 0.005):
            if word==ourword:
                print(word)
                chosen_word=word
                ourword_used=True
                break
            bag.append(word)
    if (ourword_used)==False:
        chosen_word=random.choice(bag)
    print('Chosen word is',chosen_word)
    sentence.append(chosen_word)
    cur_bigram[0]=cur_bigram[1]
    cur_bigram[1]=chosen_word
    if chosen_word == "." or chosen_word == "!" or chosen_word =="?":
        sentence_end=True
        print(sentence)
    print(chosen_word)
    count+=1
    if(count>50):
        sentence_end=True
        print(str(sentence))
        break
    ourword_used=False

    
