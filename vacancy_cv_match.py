# install and import packages
import re
import nltk
import numpy as np
import pandas as pd
from pymystem3 import Mystem

from vacancy_templates import output, no_nan_texts, corpus_vacancy

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


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


def search_in_list(series, var):
    var = str(var)
    a = series.apply(lambda x: ''.join(x))
    output = list(map(lambda x: 1 if str(x).find(var) != 0 else 0, a))
    return output


# vacancy example - system analyst, see here: https://hh.ru/vacancy/37820546
# в действительности это задаётся HR по названию вакансии
vacancy_to_fit = no_nan_texts.iloc[output.iloc[399, 1]]

# input from vacancy
salary = int(vacancy_to_fit.income_l)
spec = vacancy_to_fit.spec.split(',')
country = [vacancy_to_fit.country if vacancy_to_fit.country != 'planetEarth' else 'Россия']
city = vacancy_to_fit.city
c_level = vacancy_to_fit.c_level
branch = vacancy_to_fit.branch
work_type = [vacancy_to_fit.work_type if vacancy_to_fit.work_type == vacancy_to_fit.work_type else 'полный день']
title = str(vacancy_to_fit.vacancy)

# upload and preprocess data
candidate_data = pd.read_csv('candidate_export.csv', encoding='UTF-8')
candidate_data.columns = ['gender', 'age', 'city', 'ready_to_move', 'title', 'salary', 'branch',
                          'spec', 'work_type', 'work_schedule', 'total_work_exp',
                          'last_employee', 'last_job_title', 'last_job_time', 'skills',
                          'about_candidate', 'education', 'source', 'source_id',
                          'last_job_resp']

# filter candidates w/o education, w/o last job title, 18+
fcandidate_data = candidate_data.loc[~candidate_data.education.isnull(), :]
fcandidate_data = fcandidate_data.loc[~fcandidate_data.last_job_title.isnull(), :]
fcandidate_data = fcandidate_data.loc[~fcandidate_data.age.isnull(), :]
fcandidate_data = fcandidate_data.loc[fcandidate_data.age >= 18, :]
fcandidate_data.reset_index()
# filter duplicates
# warning: у нас нет бизнес-аккаунта на hh, чтобы получить имя кандидата, поэтому эта строка закомментена
# fcandidate_data = fcandidate_data.drop_duplicates(['name', 'gender', 'city', 'last_employee'])

# check work_type
fcandidate_data.work_type = fcandidate_data.work_type.apply(lambda x: clean_text_prev(x)).tolist()
fcandidate_data.work_type = search_in_list(fcandidate_data.work_type, work_type)

# check salary interval if possible (+- 20%)
fcandidate_data.salary = fcandidate_data.salary.apply(lambda x: 1 if 1.2 * salary >= x >= 0.8 * salary and
                                                      x == x else 0)

# check last job responsibilities
fcandidate_data = fcandidate_data.loc[~fcandidate_data.last_job_resp.isnull(), :]



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
corpus = fcandidate_data.loc[:, 'last_job_resp'].apply(lambda txt: preprocess_text(txt, stop_words))

import unicodedata

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


corpus.loc[len(corpus)] = corpus_vacancy[399]
vacancy_id = len(corpus)
corpus = list(map(lambda x: clean_text_prev(str(x)).strip(), corpus))

m = Mystem()
corpus = list(map(lambda x: ''.join(m.lemmatize(x)), corpus))
corpus = list(map(lambda x: re.sub(r'\n', '', x), corpus))

vectorizer = TfidfVectorizer(ngram_range=(1, 3))
vectorizer.fit(corpus)
X = vectorizer.transform(corpus).toarray()
corrs = np.corrcoef(X)


# дальше надо найти по строке с вакансией топ-10 максимальных корреляций
# и вывести резюме всех подходящих кандидатов
