import re
import csv
from nltk.corpus import stopwords

ham_messages = []
spam_messages = []
en_stops = set(stopwords.words('english'))

with open('sms-spam-corpus.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        row[1] = re.sub(r'[^\w\s]+|[\d]+', r'', row[1]).strip().lower() 
        for word in row[1].replace('. ', ' ').split():
            if word in en_stops:
                row[1] = row[1].replace(word, "")
                row[1] = ' '.join(row[1].split())
        if row[0] == "ham":
            ham_messages.append(row[1])
        else:
            spam_messages.append(row[1])

#   HAM PREPARATIONS
ham_words = {}
file = open('ham_word_count.txt')
for f in file:
    ham_words[f.split()[0]] = f.split()[1]
ham_words_sum = sum(int(ham_words[item]) for item in ham_words)

#   SPAM PREPARATIONS
spam_words = {}
file = open('spam_word_count.txt')
for f in file:
    spam_words[f.split()[0]] = f.split()[1]
spam_words_sum = sum(int(spam_words[item]) for item in spam_words)

print("enter message:")
#   Nah I don't think he goes to usf, he lives around here though
#   FreeMsg Hey there darling it's been 3 week's now and no word back! I'd like some fun you up for it s...
#   Even my brother is not like to speak with me. They treat me like aids patent
#   WINNER!! As a valued network customer you have been selected to receivea �900 prize reward! To claim...
#   Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera f...
body_text = input()
body_text = re.sub(r'[^\w\s]+|[\d]+', r'', body_text).strip().lower()
for word in body_text.replace('. ', ' ').split():
    if word in en_stops:
        body_text = body_text.replace(word, "")
        body_text = ' '.join(body_text.split())

body_text = body_text.split()
probability = 1     # P(bodyText | ham)
for word in body_text:
    if word in ham_words.keys():
        probability *= (int(ham_words[word]) + 1) / (ham_words_sum + (1 * spam_words_sum))
    else:
        probability *= 1 / (ham_words_sum + (1 * spam_words_sum))
pham = len(ham_messages) / (len(ham_messages) + len(spam_messages))     # P(ham)
ham_probability = probability / pham

probability = 1     # P(bodyText | spam)
for word in body_text:
    if word in spam_words.keys():
        probability *= (int(spam_words[word]) + 1) / (spam_words_sum + (1 * ham_words_sum))
    else:
        probability *= 1 / (spam_words_sum + (1 * ham_words_sum))
pspam = len(spam_messages) / (len(ham_messages) + len(spam_messages))   # P(spam)
spam_probability = probability / pspam

print("ham probability: " + str(ham_probability))
print("spam probability: " + str(spam_probability))
if ham_probability > spam_probability:
    print("it's ham")
else:
    print("it's spam")
