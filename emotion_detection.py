import nltk,csv,sys,re
import matplotlib.pyplot as plt
import string
import numpy as np
import plotly.plotly as py
import pandas as pd
from nltk.stem import PorterStemmer
from replacers import RepeatReplacer
from replacers import AntonymReplacer
from replacers import RegexpReplacer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

#reading the csv file and extracting the column of tweets into a list
csv_file=sys.argv[1]

df=pd.read_csv(csv_file)
saved_column=df['text']
list1=list(saved_column)
#print (list1)

replacer=AntonymReplacer()
rep1=RepeatReplacer()
rep2=RegexpReplacer()

for i in range(0,len(list1)):
    list1[i]=re.sub(r'[^\x00-\x7F]',r' ',list1[i]) #Replacing non-ascii characters with a space
    list1[i]=rep2.replace(list1[i])                 #texts like can't are converted into can not
    list1[i]=list1[i].split()                       #Splitting each sentence into words
    #list1[i]=[w for w in list1[i] if (len(w)>2)]    #String length of a word is more than 2
    list1[i]=replacer.replace_negations(list1[i])   #Replaces the negative words with antonyms

emo={}
f=open('emotions.txt','r')
for line in f:
    line=line.split(',')
    emo[line[0]]=line[1].rstrip()
#print(emo)
abb={}
f=open('abb.txt','r')
for line in f:
    line=line.split(',')
    abb[line[0].lower()]=(line[1].rstrip()).lower()
#print(abb)
#for i in ran

for i in range(0,len(list1)):
    for j in range(0,len(list1[i])):
        #list1[i][j]=list1[i][j].lower()
        list1[i][j]=rep1.replace(list1[i][j])       #Removes unnecessary repeated characters in a word
        list1[i][j]=list1[i][j].lower()
        list1[i][j]=str(list1[i][j])
        

#print(list1)
list2=[]                                            #This list stores the values(meanings) of the emoticons present in the tweet
list3=[]                                            #This list stores the words of the abbrevations for ex: lol -> list3=['laughing','out','loud']
for i in range(0,len(list1)):
    for j in range(0,len(list1[i])):
        if(list1[i][j] in emo.keys()):
            list2=word_tokenize(emo[list1[i][j]])
            list1[i]=list1[i]+list2
    list1[i]=[w for w in list1[i] if not w in emo.keys()]   #Removes the emoticons from the list
for i in range(0,len(list1)):
    for j in range(0,len(list1[i])):
        list3=[]
        if(list1[i][j] in abb.keys()):
            list3=word_tokenize(abb[list1[i][j]])           #All the words of the abbrevations are tokenized
            list1[i]=list1[i]+list3                         #All the words of the abbrevations are added to the list
    list1[i]=[w for w in list1[i] if not w in abb.keys()]   #Removes the abbrevations from the list

#print list1
#print list2

for i in range(0,len(list1)):
    for j in range(0,len(list1[i])):
        list1[i][j]=(list1[i][j]).lower()


#print happy_active
x=[]
pos=['than','as','because']
neg=['but','so']
a=0
list2=[]
for i in range(0,len(list1)):
    list2=[]
    a=0
    for j in range(0,len(list1[i])):
        if(list1[i][j] in pos):
            a=1
            for k in range(0,j):
                list2.append(list1[i][k])#Collect the sentence till the conjunction
    if (a==1):
        list1.pop(i)    #Pop the entire sentence
        list1.insert(i,list2)#Put the collected sentence into the list

#print list1

for i in range(0,len(list1)):
    list2=[]
    a=0
    for j in range(0,len(list1[i])):
        if(list1[i][j] in neg):
            a=1
            k=j
            break
    if(a==1):
        del list1[i][0:k+1]
    
#print list1

happy=['enthrallment','confidence','giggle','relief ','good','best','rapture','eagerness','funniest', 'hope', 'optimism','celebrate','incredible','bright','congrats','pride','fantastic', 'triumph','amusement', 'bliss', 'cheerfulness','glee','jolliness','joviality', 'joy', 'delight','yummy', 'enjoyment', 'gladness','amazement', 'surprise', 'astonishment', 'happiness','jubilation', 'elation', 'ecstasy', 'euphoria', 'elated','overjoyed','enjoy','excited','proud','joyful','happy','blessed','amazing','wonderful','awesome','excellent','delighted','enthusiastic','felicitous','beautiful','beaming','laugh','funny', 'Adoration', 'affection', 'love', 'fondness', 'attraction','caring', 'compassion', 'sentimentality','calm','peaceful','contentment', 'pleasure ','satisfied','relax','enthusiasm', 'zeal', 'zest', 'excitement', 'thrill','great','win' ,'exhilaration']
fear=['shock', 'fear', 'fright', 'horror', 'terror','threat','panic', 'hysteria','mortification', 'anxiety', 'tenseness', 'uneasiness', 'apprehension','worry', 'distress', 'dread','nervous','tension','afraid','fearful','terrifying','bother','disturbed','worship']
sad=['sad','sorrow','disappointed','miserable','bad','confuse','dilemma','excluded','alone','hopeless','sorry','tragic','unhappy','pity','pensive','depress','pessimism','fatigued','gloomy','unhappy','fail','lack','suicidal','downhearted','hapless','dispirited','Torment','sympathy', 'Agony', 'suffering', 'hurt', 'anguish','despair', 'glumness','grief', 'woe','melancholy','dismay','dejected','displeasure','guilt','struggle', 'shame','regret', 'remorse','alienation', 'isolation', 'neglect', 'loneliness', 'rejection','homesickness', 'defeat', 'dejection', 'insecurity', 'embarrassment','humiliation', 'insult','dislike']
anger=['wild','agressive','aggravation', 'livid','stormy','sore','irritation','deceive','rudeness','agitation', 'annoyance','angry','serious','grouchiness','grumpiness','exasperation','shout','frustration','anger', 'rage', 'outrage', 'fury', 'wrath', 'hostility', 'ferocity', 'bitterness','hate','scorn','spite','vengefulness','resentment','annoyed','annoying','stress','irritated','mad','furious','distress','stressful','disgust', 'revulsion', 'contempt','loathing' ,'envy','jealousy','jerk']

#Exclamatory words
ihappy=['Yahoo','yay','yaay','hurrah','wow','yummy','whoa']
ifear=['Aah','yikes','ewww']
isad=['owww','alas','aw','ouch','oops']
ianger=['grrr','uff','yuck']

stemmer=PorterStemmer()

for i in range(0,len(happy)):
    happy[i]=happy[i].lower()
    happy[i]=stemmer.stem(happy[i])
for i in range(0,len(fear)):
    fear[i]=fear[i].lower()
    fear[i]=stemmer.stem(fear[i])
for i in range(0,len(sad)):
    sad[i]=sad[i].lower()
    sad[i]=stemmer.stem(sad[i])
for i in range(0,len(anger)):
    anger[i]=anger[i].lower()
    anger[i]=stemmer.stem(anger[i])

st=[]
happy1=[]
fear1=[]
sad1=[]
angry1=[]
for line in open('data.txt'):
    st=[]
    st=line.split()
    if(st[1]=='joy'):
        happy1.append(st[2:])
    elif(st[1]=='anger'):
        angry1.append(st[2:])
    elif(st[1]=='fear'):
        fear1.append(st[2:])
    else:
        sad1.append(st[2:])
for i in range(0,len(happy1)):
    happy1[i]=' '.join(happy1[i])
for i in range(0,len(angry1)):
    angry1[i]=' '.join(angry1[i])
for i in range(0,len(sad1)):
    sad1[i]=' '.join(sad1[i])
for i in range(0,len(fear1)):
    fear1[i]=' '.join(fear1[i])

h2=[]
s2=[]
f2=[]
a2=[]

for i in range(0,len(happy1)):
    happy1[i]=(happy1[i]).split()
    for j in range(0,len(happy1[i])-1):
        h2.append((happy1[i][j],happy1[i][j+1]))
for i in range(0,len(sad1)):
    sad1[i]=(sad1[i]).split()
for i in range(0,len(sad1)):
    for j in range(0,len(sad1[i])-1):
        s2.append((sad1[i][j],sad1[i][j+1]))
for i in range(0,len(angry1)):
    angry1[i]=(angry1[i]).split()
for i in range(0,len(angry1)):
    for j in range(0,len(angry1[i])-1):
        a2.append((angry1[i][j],angry1[i][j+1]))
for i in range(0,len(fear1)):
    fear1[i]=(fear1[i]).split()
for i in range(0,len(fear1)):
    for j in range(0,len(fear1[i])-1):
        f2.append((fear1[i][j],fear1[i][j+1]))

h3=[]
s3=[]
f3=[]
a3=[]

for i in range(0,len(happy1)):
    for j in range(0,len(happy1[i])-2):
        h3.append((happy1[i][j].lower(),happy1[i][j+1].lower(),happy1[i][j+2].lower()))
for i in range(0,len(sad1)):
    for j in range(0,len(sad1[i])-2):
        s3.append((sad1[i][j].lower(),sad1[i][j+1].lower(),sad1[i][j+2].lower()))
for i in range(0,len(angry1)):
    for j in range(0,len(angry1[i])-2):
        a3.append((angry1[i][j].lower(),angry1[i][j+1].lower(),angry1[i][j+2].lower()))
for i in range(0,len(fear1)):
    for j in range(0,len(fear1[i])-2):
        f3.append((fear1[i][j].lower(),fear1[i][j+1].lower(),fear1[i][j+2].lower()))


h4=[]
s4=[]
f4=[]
a4=[]

for i in range(0,len(happy1)):
    for j in range(0,len(happy1[i])-3):
        h4.append((happy1[i][j].lower(),happy1[i][j+1].lower(),happy1[i][j+2].lower(),happy1[i][j+3].lower()))
for i in range(0,len(sad1)):
    for j in range(0,len(sad1[i])-3):
        s4.append((sad1[i][j].lower(),sad1[i][j+1].lower(),sad1[i][j+2].lower(),sad1[i][j+3].lower()))
for i in range(0,len(angry1)):
    for j in range(0,len(angry1[i])-3):
        a4.append((angry1[i][j].lower(),angry1[i][j+1].lower(),angry1[i][j+2].lower(),angry1[i][j+3].lower()))
for i in range(0,len(fear1)):
    for j in range(0,len(fear1[i])-3):
        f4.append((fear1[i][j].lower(),fear1[i][j+1].lower(),fear1[i][j+2].lower(),fear1[i][j+3].lower()))


bigrams=[]
trigrams=[]
quadgrams=[]

hap=0
sa=0
ang=0
fea=0
neu=0

y=''


for i in range(0,len(list1)):
    quadgrams=[]
    trigrams=[]
    bigrams=[]
    x=[]
    t=()
    for j in range(0,len(list1[i])):
        if(stemmer.stem(list1[i][j]) in happy or stemmer.stem(list1[i][j]) in ihappy):
            if(list1[i][j-1]=='not'):
                x.append('sad')
            else:
                x.append('happy')
        elif(stemmer.stem(list1[i][j]) in sad or stemmer.stem(list1[i][j]) in isad):
            x.append('sad')
        elif(stemmer.stem(list1[i][j]) in fear or stemmer.stem(list1[i][j]) in fear):
            x.append('fear')
        elif(stemmer.stem(list1[i][j]) in anger or stemmer.stem(list1[i][j]) in ianger):
            x.append('anger')
    if not x:
        if(len(list1[i])>=4):
            for k in range(0,len(list1[i])-3):
                quadgrams.append((list1[i][k],list1[i][k+1],list1[i][k+2],list1[i][k+3]))
            for k in range(0,len(quadgrams)):
                if(quadgrams[k] in f4):
                       x.append('fear')
                if(quadgrams[k] in s4):
                       x.append('sad')
                if(quadgrams[k] in h4):
                       x.append('happy')
                if(quadgrams[k] in a4):
                       x.append('angry')
    if not x:
        if(len(list1[i])>=3):
              for k in range(0,len(list1[i])-2):
                  trigrams.append((list1[i][k],list1[i][k+1],list1[i][k+2]))
              for k in range(0,len(trigrams)):
                   if(trigrams[k] in f3):
                         x.append('fear')
                   if(trigrams[k] in s3):
                         x.append('sad')
                   if(trigrams[k] in h3):
                         x.append('happy')
                   if(trigrams[k] in a3):
                         x.append('angry')
    if not x:
         if(len(list1[i])>=2):
               for k in range(0,len(list1[i])-1):
                     bigrams.append((list1[i][k],list1[i][k+1]))
               for k in range(0,len(bigrams)):
                     if(bigrams[k] in s2):
                        x.append('sad')
                     if(bigrams[k] in h2):
                        x.append('happy')
                     if(bigrams[k] in a2):
                        x.append('angry')
                     if(bigrams[k] in f2):
                        x.append('fear')
    if not x or (len(list(set(x)))>=2):
        x=['neutral']
    if('happy' in x):
        hap=hap+1
    if('sad' in x):
        sa=sa+1
    if('anger' in x):
        ang=ang+1
    if('fear' in x):
        fea=fea+1
    if('neutral' in x):
        neu=neu+1
    y=','.join(list(set(x)))
    t=(list1[i],y)
    list2.append(t)

print list2

hap=(hap*100/len(list1))
sa=(sa*100/len(list1))
ang=(ang*100/len(list1))
fea=(fea*100/len(list1))
neu=(neu*100/len(list1))

print hap,sa,ang,fea,neu

objects = ('Happy', 'Sad', 'Anger', 'Fear', 'Neutral')
y_pos = np.arange(len(objects))
performance = [hap,sa,ang,fea,neu]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Percentage of Emotions')
plt.show()
