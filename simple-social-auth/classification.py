from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
from nltk.stem import PorterStemmer, WordNetLemmatizer 
from nltk.tokenize import word_tokenize
import preprocessor as p
from empath import Empath
from keras.models import model_from_json
import re


def classification(list):
    p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.MENTION)

    with open('finalstemming.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)



    model = model_from_json(open('final_architecture.json').read())
    model.load_weights('final_weights.h5')

    # dont forget to compile your model
    model.compile(loss='categorical_crossentropy', optimizer='adam')



    lexicon = Empath()


    worryword=["worry","problem","concern","anxiety","worrying","regret","trouble","care","worried"];
    hatewords=["hate","hates","despise","annoys","annoying","pity","bully","bullying","bullshit","selfish","unfair","sucks","hell","stupid","idiot","jerks","fools","insult","insulted","fuck"];


    totalnumber=len(list)

    totalhate=0
    totalworry=0
    totalanger=0
    totalfear=0
    totalhappiness=0
    totalsad=0
    totallove=0
    totalsurprise=0
    conpos=0
    aggpos=0
    extpos=0
    inmodel=False
    notPresent = False
    for b in list:
        notPresent = False
        
        #  CREATING INTO A SINGLE VALUED LIST
        b = re.sub(r'[^\w\s]','',b) # REMOVING PUNCTUATION

        # NOT TEST
        if 'not' in b:
            notPresent = True
        b=[b]
        emotion=lexicon.analyze(b, normalize=True)
        if((emotion['achievement']>0)or(emotion['work']>0)):
            if notPresent:
                conpos=conpos+1;
            else:
                conpos=conpos+1;
        elif((emotion['help']>0)or(emotion['trust']>0)):
            if notPresent:
                aggpos=aggpos-1;
            else:            
                aggpos=aggpos+1;
        elif((emotion['traveling']>0)or(emotion['tourism']>0)or(emotion['exercise']>0)):
            if notPresent:
                extpos=extpos+1;
            else:            
                extpos=extpos+1;
        tokenizedb= word_tokenize(b[0])
        for i in tokenizedb:
            if i in hatewords:
                if notPresent:
                    totalhate=totalhate-1;
                else:
                    totalhate=totalhate+1;
                inmodel=False;
                break
            elif i in worryword:
                if notPresent:
                    totalworry=totalworry+1;
                else:        
                    totalworry=totalworry+1;
                inmodel=False;
                break
            else:
                inmodel=True;
        if(inmodel):
            b[0] = p.clean(b[0])
            stemmer = PorterStemmer()
            b = [" ".join([stemmer.stem(word) for word in sentence.split(" ")]) for sentence in b]
            sent3 = tokenizer.texts_to_sequences(b)
            trial_data = pad_sequences(sent3, maxlen=80)

            d=np.argmax(model.predict(trial_data))
            if (d==0):
                if notPresent:
                    totalanger=totalanger-1;
                else:
                    totalanger=totalanger+1;
            elif(d==1):
                if notPresent:
                    totalfear=totalfear-1;
                else:
                    totalfear=totalfear+1;
            elif(d==2):
                if notPresent:
                    totalhappiness=totalhappiness-1;
                else:
                    totalhappiness=totalhappiness+1;
            elif(d==3):
                if notPresent:
                    totallove=totallove-1;
                else:
                    totallove=totallove+1;
            elif(d==4):
                if notPresent:
                    totalsad=totalsad-1;
                else:
                    totalsad=totalsad+1;
            elif(d==5):
                if notPresent:
                    totalsurprise=totalsurprise-1;
                else:
                    totalsurprise=totalsurprise+1;                
    hate=(100*totalhate)/totalnumber
    hate=int(hate)

    worry=(100*totalworry)/totalnumber
    worry=int(worry)

    anger=(100*totalanger)/totalnumber
    anger=int(anger)

    fear=(100*totalfear)/totalnumber
    fear=int(fear)

    happiness=(100*totalhappiness)/totalnumber
    happiness=int(happiness)

    love=(100*totallove)/totalnumber
    love=int(love)

    sad=(100*totalsad)/totalnumber
    sad=int(sad)

    surprise=(100*totalsurprise)/totalnumber
    surprise=int(surprise) 
    conscient=(100*conpos)/totalnumber
    conscient=int(conscient) 
        
    aggreable=(100*aggpos)/totalnumber
    aggreable=int(aggreable) 
             
    extrovert=(100*extpos)/totalnumber
    extrovert=int(extrovert) 
             
    
    conscientiousnesspositive=love+happiness+conscient;
    conscientiousnessnegative=worry+sad+fear;

    aggreablepositive=love+happiness+aggreable;
    aggreablenegative=hate+anger;

    neuroticpositive=worry+sad+anger+hate;
    neuroticnegative=love+happiness;


    extrovertpositive=love+happiness+extrovert;
    extrovertnegative=worry+sad+fear+hate;


    opennesspositive=love+happiness;
    opennessnegative=fear+sad;
    return(anger,fear,happiness,hate,love,sad,surprise,worry,opennesspositive,opennessnegative,extrovertpositive,extrovertnegative,neuroticpositive,neuroticnegative,aggreablepositive,aggreablenegative,conscientiousnesspositive,conscientiousnessnegative);


def getextra(list):
    achievement=0
    alcohol=0
    clothing=0
    cooking=0
    family=0
    government=0
    music=0
    party=0
    programming=0
    science=0
    lexicon = Empath()
    totalnumber=len(list)
    p.set_options(p.OPT.URL, p.OPT.EMOJI,p.OPT.MENTION)

    for b in list:
        b = re.sub(r'[^\w\s]','',b)
        b=[b]
        b[0] = p.clean(b[0])
        emotion=lexicon.analyze(b, normalize=True)
        if(emotion['achievement']>0):
            achievement=achievement+1;
        elif(emotion['alcohol']>0):
            alcohol=alcohol+1;
        elif(emotion['clothing']>0):
            clothing=clothing+1;
        elif(emotion['cooking']>0):
            cooking=cooking+1;
        elif(emotion['family']>0):
            family=family+1;
        elif(emotion['government']>0):
            government=government+1;
        elif(emotion['music']>0):
            music=music+1;
        elif(emotion['party']>0):
            party=party+1;
        elif(emotion['programming']>0):
            programming=programming+1;
        elif(emotion['science']>0):
            science=science+1;
            
    achievement=(100*achievement)/totalnumber
    achievement=int(achievement)
    alcohol=(100*alcohol)/totalnumber
    alcohol=int(alcohol)
    clothing=(100*clothing)/totalnumber
    clothing=int(clothing)
    cooking=(100*cooking)/totalnumber
    cooking=int(cooking)
    family=(100*family)/totalnumber
    family=int(family)
    government=(100*government)/totalnumber
    government=int(government)
    music=(100*music)/totalnumber
    music=int(music)
    party=(100*party)/totalnumber
    party=int(party)
    programming=(100*programming)/totalnumber
    programming=int(programming)
    science=(100*science)/totalnumber
    science=int(science)
    
    return(achievement,alcohol,clothing,cooking,family,government,music,party,programming,science)

       
        
       
        
        

    
    


# In[169]:


# hate=(100*totalhate)/totalnumber
# hate=int(hate)

# worry=(100*totalworry)/totalnumber
# worry=int(worry)

# anger=(100*totalanger)/totalnumber
# anger=int(anger)

# fear=(100*totalfear)/totalnumber
# fear=int(fear)

# happiness=(100*totalhappiness)/totalnumber
# happiness=int(hapiness)

# love=(100*totallove)/totalnumber
# love=int(love)

# sad=(100*totalsad)/totalnumber
# sad=int(sad)

# surprise=(100*totalsurprise)/totalnumber
# surprise=int(surprise)


# In[ ]:


# conscientiousnesspositive=love+happiness;
# conscientiousnessnegative=worry+sad+fear;

# aggreablepositive=love+happiness;
# aggreablenegative=hate+anger;

# neuroticpositive=worry+sad+anger+hate;
# neuroticnegative=love+happiness;


# extrovertpositive=love+happiness;
# extrovertnegative=worry+sad+fear+hate;


# opennesspositive=love+happiness;
# opennessnegative=fear+sad;


# In[14]:


# type(b)


# In[22]:


# b=["so sad"]
# from nltk.stem import PorterStemmer, WordNetLemmatizer 
# stemmer = PorterStemmer()
# b = [" ".join([stemmer.stem(word) for word in sentence.split(" ")]) for sentence in b]
# sent3 = tokenizer.texts_to_sequences(b)

# trial_data = pad_sequences(sent3, maxlen=80)
# trial_data


# In[23]:


# model.predict(trial_data)


# In[24]:


# import numpy as np
# a=np.argmax(model.predict(trial_data))
# if (a==0):
#     print("anger")
# elif(a==1):
#     print("fear")
# elif(a==2):
#     print("hapiness")
# elif(a==3):
#     print("love")
# elif(a==4):
#     print("sad")
# elif(a==5):
#     print("surprise")


# In[150]:


# d=["i got promotion"]
# a=lexicon.analyze(d, normalize=True)
# # achievement,work cons
# # agg trust help
# # tourism traveling excercise extr
# if((a['achievement']<0) or(a['hate']>0)):
#     print("hi")
# achievement
# alcohol
# clothing
# cooking
# family
# government
# music
# party
# programming
# science

