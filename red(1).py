import networkx as nx
import matplotlib.pyplot as plt
import nltk
from nltk.wsd import lesk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn
stop_words = set(stopwords.words('english'))


sent =[' I like beer. Miller just launched. A new pilsner. but, because i am a beer snob, i am only going to drink pretentious belgian ale.','Balu has an automobile workshop. anjali went there to repair her car. shain was already there with his ambulance']

GlobalList=[]

for txt in sent:
    text = txt.split(' ')
    tagged= list()
    tokenized=sent_tokenize(txt)
    for i in tokenized:

        # Word tokenizers is used to find the words
        # and punctuation in a string
        wordsList = nltk.word_tokenize(i)

        # removing stop words from wordList
        wordsList = [w for w in wordsList if not w in stop_words]

        #  Using a Tagger. Which is part-of-speech
        # tagger or POS-tagger.
        tagged += nltk.pos_tag(wordsList)
        newWords = [(word) for word , tag in tagged if tag in ('NN','NNS','NNP')]

    replaceWord = []
    ConceptWeight=[]
    Weight=[]


    txtNew = []
    txtNew = text

    print("printing replaced words\n")
    for word in newWords:
        replaceWord.append((lesk(text,word,'n')))
        print("\t> " + str(replaceWord))

    print("\n----------------------------------")

    RWords=[]
    for Words in replaceWord:
        if (Words is not None):
            RWords.append(Words.name())

    print("\n\nPrinting Word Count\n")
    for nword in newWords:
        print("  New word Count of " + nword)
        NewwordCount=newWords.count(nword)
        print("\t\t" + str(NewwordCount))

    print("\n------------------------------------")
    Lexicalchainscores=[]
    mylist = []

    r1=1
    r2=0.5
    r3=0.25
    G=nx.Graph()
    print("printing rword\n")
    for rword in RWords:
        print(" > " + str(rword))
        RSynsets = wn.synset(rword)
        hypernym = RSynsets.hypernyms()
    for hyper in hypernym:
        for i in range(0,len(RWords)-1):
            if(hyper.name() in RWords[i]):
                print("\nConceptCount of "+ rword)
                conceptweightcountsOne=RWords.count(rword)
                print("\t" + str(conceptweightcountsOne))
                print("\nConceptCount of "+ RWords[i])
                conceptweightcountsTwo=RWords.count(RWords[i])
                print("\t" + str(conceptweightcountsTwo))
                ConceptScoreOne=conceptweightcountsOne*r1+conceptweightcountsTwo*1*0.25
                ConceptScoreTwo=conceptweightcountsTwo*r1+conceptweightcountsOne*1*0.25
                print ("\nConceptScore of "+rword,ConceptScoreOne)
                print ("\nConceptScore of "+RWords[i],ConceptScoreTwo)
                Lexicalchainscore=ConceptScoreOne+ConceptScoreTwo
                print("\n------------------------------------")
                print("\nScore of this lexical chain is\n")
                print("\tprinting rword and RWord[i]:\t",rword,RWords[i])
                if rword not in mylist:
                    mylist.append(rword)
                if RWords[i] not in mylist:
                    mylist.append(RWords[i])
                    print("printing mylist " + str(mylist))
                    GlobalList.append([mylist])

                G.add_edge(rword,RWords[i],weight=0.6)

        lex=0
        lex=lex+Lexicalchainscore
        print("\n\tLex: " + str(lex))

Lexicalchainscores.append(lex)
for i in Lexicalchainscores:
    print("\tChain score: " + str(i))

print("\n------------------------------------")
print("\nprinting global list")
print(GlobalList)
for i in GlobalList:
    print("\t> " + str(i))

pos=nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos , node_size=500)
nx.draw_networkx_edges(G,pos,width=1)
nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')
plt.axis('off')
plt.show()
