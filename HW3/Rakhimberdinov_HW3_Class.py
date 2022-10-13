class CountVectorizer:
    def __init__(self, lowercase=True):
        self.lowercase = lowercase
        self.tokens = []

    @staticmethod
    def lower(container_to_lower):
        return [x.lower() for x in container_to_lower]

    def fit_transform(self, contain_param):
        if self.lowercase:
            container = self.lower(contain_param)
        else:
            container = contain_param

        all_words = [a for i in container for a in i.split()]
        counter_matrix = []
        for sent in container:
            counter = dict().fromkeys(all_words, 0)
            for w in sent.split():
                counter[w] = counter.get(w) + 1
            counter_matrix.append([*counter.values()])

        self.tokens = [*dict().fromkeys(all_words, 0).keys()]

        return counter_matrix

    # this method is optional because there is the same attribute
    def get_feature_names(self):
        return self.tokens

if __name__ == '__main__':
    corpus = ['Crock Pot Pasta Never boil pasta again', 'Pasta Pomodoro Fresh ingredients Parmesan to taste']
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(count_matrix)
