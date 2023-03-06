def serialize(word, mode):
    if mode == "bad_words":
        file_name = mode + ".csv"
    else:
        file_name = mode +".csv"

    with open(file_name, 'a+') as csv_file:
        csv_file.write(word + "\n")


def deserialize(mode):
    if mode == "bad_words":
        file_name = mode + ".csv"

        with open(file_name, "r") as f:
            sub_words = f.readlines()

        words = map(lambda x: x.replace("\n", ""), sub_words)

        alphabet_dict = {}

        for word in words:
            if alphabet_dict.get(word[0], None):
                alphabet_dict[word[0]].append(word)
            else:
                alphabet_dict[word[0]] = [word]

        return alphabet_dict
    else:
        file_name = mode +".csv"

        with open(file_name,"r") as f:
            exceptions = f.readlines()

        exceptions = list(map(lambda x: x.replace("\n", ""), exceptions))

        return exceptions


def _to_default():
    with open("bad_words.txt",'r') as f:
        words_list = f.readlines()[0].split(", ")

    with open("bad_words.csv","w") as csv_file:
        for word in words_list:
            csv_file.write(word + "\n")

