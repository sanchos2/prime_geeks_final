# install and import packages
import re
import nltk
import numpy as np
import pandas as pd
from pymystem3 import Mystem
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# upload and preprocess data
vacancy_data = pd.read_csv('vacancy_export.csv', encoding='UTF-8')
vacancy_data.columns = ['vacancy', 'date', 'id', 'emp_type', 'emp_title', 'city', 'country',
                        'currency', 'income', 'income_l', 'income_r', 'work_type', 'c_level',
                        'spec', 'branch', 'url', 'desc']

no_nan_texts = vacancy_data.loc[~vacancy_data.iloc[:, -1].isnull(), :]
no_nan_texts = no_nan_texts.drop_duplicates().reset_index()

# наиболее популярные варианты написания обязанностей в вакансиях
# список можно расширить
resp = ['бязанност', 'предстоит', 'доверим тебе', 'ребовани']

# take responsibilities
output = pd.DataFrame()
start_index = list([])
for i in range(len(resp)):
    test = no_nan_texts.desc[no_nan_texts.desc.str.count(resp[i]) > 0]
    test_res = test.apply(lambda x: re.search(r'.' + str(resp[i]) + '.*?</p>.*?<p>', x))
    test_res1 = test_res[~test_res.isnull()].apply(lambda x: x.group(0))
    output = pd.concat([output, test_res1], ignore_index=False)
    start_index.extend(test_res1.index)

output.columns = ['resp']
output['ind'] = start_index
output = output[output.resp.astype('str').str.len() > 50]
output = output.drop_duplicates()


def preprocess_text(text, stop_words=None):
    tags_pattern = re.compile(r'<.*?>')
    no_html = re.sub(tags_pattern, ' ', text)
    space_pattern = re.compile(r'\s{2,10}')
    out = re.sub(space_pattern, ' ', no_html)
    if stop_words is not None:
        out = ' '.join([word for word in out.split() if word not in stop_words])
    return out


# define stop words
stop_words = list(stopwords.words('russian'))
specwords = ['бязанност', 'ребовани', 'слови', 'предстоит']
stop_words.extend(specwords)
stop_words = set(stop_words)

# extract features with TF-IDF
output2 = output.iloc[:, 0].apply(lambda txt: preprocess_text(txt, stop_words))
corpus = output2

import unicodedata
import string

def remove_control_characters(s):
    if s == s:
        out_string = "".join(ch if unicodedata.category(ch)[0] not in ["C", "Z"] else ' ' for ch in s)
        return re.sub(' +', ' ', out_string).strip()
    else:
        return float('nan')


def clean_text_prev(review_text):
    # remove punctuation
    no_punct = re.sub(r'\n', ' ', review_text.lower())
    no_punct = re.sub(r'[{}]+'.format(re.escape('!"$%&\'()*,-./:;<=>?@[\\]^_`{|}~')), ' ', no_punct)
    no_punct = re.sub(r'[^a-zа-яё#+\s]', ' ', no_punct)
    # removing redundant spaces
    space_pattern = re.compile(r'\s{2,20}')
    no_spaces = re.sub(space_pattern, ' ', no_punct)
    return no_spaces


corpus = list(map(lambda x: clean_text_prev(str(x)).strip(), corpus))

m = Mystem()
corpus = list(map(lambda x: ''.join(m.lemmatize(x)), corpus))
corpus = list(map(lambda x: re.sub(r'\n', '', x), corpus))

vectorizer = TfidfVectorizer(ngram_range=(1, 3))
vectorizer.fit(corpus)
X = vectorizer.transform(corpus).toarray()
corrs = np.corrcoef(X)

# get all existing interconnections between vacancies
indexes = np.argwhere((np.tril(corrs, k=-1) > 0.7) * (np.tril(corrs, k=-1) != 1))

# test for system analyst
# к сожалению, это одна из немногих хорошо спарсившихся вакансий
# в идеале нужно побольше данных
title = 'Системный аналитик'
title = title.lower()[1:-2]
no_nan_texts['check'] = list(map(lambda x: int(title in x), no_nan_texts.vacancy))
test = no_nan_texts[no_nan_texts.check > 0]
test_index = test.index.tolist()

pairs = []
for i in range(len(test_index)):
    for j in range(len(indexes)):
        if test_index[i] == indexes[j][0]:
            pairs.append(indexes[j][0])
        else:
            if test_index[i] == indexes[j][1]:
            pairs.append(indexes[j][1])
pairs = list(set(pairs))

# между сколькими вакансиями есть значимая корреляция =>
# можно говорить о наличии стандарта в описаниях данной вакансии
# и по сути брать любые в шаблоны
print('similar_among_vacancies ' + str(round(100 * len(pairs) / len(test_index), 1)) + '%')

# print templates
# темплейты нужно ещё приводить ещё в более читаемый вид, но в целом идея отработала
for i in range(len(pairs)):
    print(output2.iloc[pairs[i]])

