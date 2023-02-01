import torch
import torch.nn as nn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


class Network(nn.Module):
    def __init__(self):
        super().__init__()

        # Layers
        self.m1 = nn.Linear(986, 986)
        self.f1 = nn.LeakyReLU()
        self.m2 = nn.Linear(986, 4096)
        self.f2 = nn.LeakyReLU()
        self.m3 = nn.Linear(4096, 1024)
        self.f3 = nn.LeakyReLU()
        self.m4 = nn.Linear(1024, 709)
        self.f4 = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.m1(x)
        x = self.f1(x)
        x = self.m2(x)
        x = self.f2(x)
        x = self.m3(x)
        x = self.f3(x)
        x = self.m4(x)
        x = self.f4(x)

        return x


class Bot:
    def __init__(self):
        self.model = self.load_model()
        self.vectorizer = self.fit_vectorizer()
        self.label_map = self.load_label_map()

    def load_model(self):
        model = Network()
        model.load_state_dict(torch.load('ML/model_weights.pth'))
        return model

    def fit_vectorizer(self):
        df = pd.read_csv('ML/data.csv')
        train_df = df.drop(['example'], axis=1)
        vectorizer = CountVectorizer()
        vectorizer = vectorizer.fit(train_df['text'])
        return vectorizer

    def load_label_map(self):
        df = pd.read_csv('ML/data.csv')
        label_map = {i: j for (i, j) in zip(range(0, len(df)), df['label'])}
        return label_map

    def ask_dnn(self, query):
        output = self.model(torch.FloatTensor(
                self.vectorizer.transform([query]).toarray()
            ))
        pred_func = self.label_map[torch.argmax(output).item()]
        return pred_func