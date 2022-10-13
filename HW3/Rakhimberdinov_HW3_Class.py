class CountVectorizer:
    """
    A class used to convert a collection of text documents to a matrix of token counts.

    ...

    Attributes
    ----------
    lowercase : bool
        whether to apply lower case to words or not
        default is True
    feature_names : set
        all unique tokens in documents

    Methods
    -------
    lower()
        Return a list of lowered strings

    fit_transform(self, container):
        Assign feature names
        Return a matrix of token counts

    get_feature_names(self)
        Return all unique tokens in documents
    """
    def __init__(self, lowercase=True):
        self.lowercase_flag = lowercase
        self.feature_names = set()

    @staticmethod
    def lower(container_to_lower):
        """
        :param container_to_lower:
            default is True
        :return: a list of lowered strings
        """
        return [x.lower() for x in container_to_lower]

    def fit_transform(self, container):
        """
        :param container:
        :return: a matrix of token counts
        """
        container = self.lower(container) if self.lowercase_flag else container
        container_split = [document.split() for document in container]

        self.feature_names = set(word for document in container_split for word in document)
        counter_matrix = []

        for document in container_split:
            counter = dict().fromkeys(self.feature_names, 0)
            for word in document:
                counter[word] = counter[word] + 1
            counter_matrix.append([*counter.values()])

        return counter_matrix

    def get_feature_names(self):
        """
        :return: all unique tokens in documents
        """
        return self.feature_names


if __name__ == '__main__':
    corpus = ['Crock Pot Pasta Never boil pasta again', 'Pasta Pomodoro Fresh ingredients Parmesan to taste']
    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(count_matrix)
