import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding,Dense,Bidirectional,LSTM
from keras.activations import relu,softmax,sigmoid
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

input_sentences=[]

with open('sentenses.txt',encoding='utf8') as f:
    contents=f.readlines()
    input_sentences=contents


# tokenizer=Tokenizer(num_words=100,oov_token="<00v>")
# tokenizer.fit_on_texts(input_sentences)
# word_index=tokenizer.word_index

# print(len(word_index))




# tokenizer=Tokenizer(num_words=100,oov_token="<00v>")
tokenizer=Tokenizer()

total_words=0
input_sequences=[]

#get input sequences for the nn
def getNGramsAndAppendToInputSequence():
    global input_sequences
    for line in input_sentences:
        token_list=tokenizer.texts_to_sequences([line])[0]
        for i in range(1,len(token_list)):
            n_gram_sequence=token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    return input_sequences



#generate input sequences
def processSentenses(sentence_list):
    global total_words
    tokenizer.fit_on_texts(sentence_list)
    word_index=tokenizer.word_index
    total_words=len(word_index)+1
    sequences=getNGramsAndAppendToInputSequence()
    return sequences

def plot_graphs(history, string):
      plt.plot(history.history[string])
      plt.xlabel("Epochs")
      plt.ylabel(string)
      plt.show()

#set input sequences
input_sequences=processSentenses(input_sentences)

#get the longest sentense in the sequence
max_sequence_len=max([len(x) for x in input_sequences]) #gets length of longest sentense

#padding the ngrams with zeros
input_sequences=np.array(pad_sequences(input_sequences,maxlen=max_sequence_len))

#Training data and labels
X=input_sequences[:,:-1]
labels=input_sequences[:,-1]
ys=to_categorical(labels,num_classes=total_words)





model = Sequential()

model.add(Embedding(total_words,240,input_length=max_sequence_len-1))
# model.add(Bidirectional(LSTM(64,return_sequences=True))) #say return_sequences only when feeding another bidirectional layer 
model.add(Bidirectional(LSTM(150)))
model.add(Dense(total_words,activation=softmax))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history=model.fit(X,ys,epochs=80)

#plot_graphs(history,"accuracy")

seed_text = "Introduction to machine learning"
next_words = 500
  
for _ in range(next_words):
	token_list = tokenizer.texts_to_sequences([seed_text])[0]
	token_list = pad_sequences([token_list], maxlen=max_sequence_len-1)
	predicted = np.argmax(model.predict(token_list, verbose=0))
	output_word = ""
	for word, index in tokenizer.word_index.items():
		if index == predicted:
			output_word = word
			break
	seed_text += "  " + output_word
print(seed_text)

# with open("article.txt",encoding='utf8') as file:
#     file.write(seed_text)
