def serialize(word):
    with open("bad_words.csv",'a+') as csv_file:
        csv_file.write(word + "\n")


def deserialize():
    with open("bad_words.csv","r") as f:
        sub_words = f.readlines()
        sub_words.remove("\n")

    words = map(lambda x:x.replace("\n",""),sub_words)

    alphabet_dict = {}

    for word in words:
        if alphabet_dict.get(word[0],None):
            alphabet_dict[word[0]].append(word)
        else:
            alphabet_dict[word[0]] = [word]

    return alphabet_dict


def _to_default():
    with open("bad_words.txt",'r') as f:
        words_list = f.readlines()[0].split(", ")

    with open("bad_words.csv","w") as csv_file:
        for word in words_list:
            csv_file.write(word + "\n")


