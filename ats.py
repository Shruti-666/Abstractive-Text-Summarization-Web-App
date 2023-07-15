import pandas
from heapq import nlargest
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

text ='''A flower, sometimes known as a bloom or blossom, is the reproductive structure found in flowering plants (plants of the division Angiospermae). Flowers produce gametophytes, which in flowering plants consist of a few haploid cells which produce gametes. The "male" gametophyte, which produces non-motile sperm, is enclosed within pollen grains; the "female" gametophyte is contained within the ovule. When pollen from the anther of a flower is deposited on the stigma, this is called pollination. Some flowers may self-pollinate, producing seed using pollen from the same flower or a different flower of the same plant, but others have mechanisms to prevent self-pollination and rely on cross-pollination, when pollen is transferred from the anther of one flower to the stigma of another flower on a different individual of the same species.

Self-pollination happens in flowers where the stamen and carpel mature at the same time, and are positioned so that the pollen can land on the flower's stigma. This pollination does not require an investment from the plant to provide nectar and pollen as food for pollinators.

Some flowers produce diaspores without fertilization (parthenocarpy). Flowers contain sporangia and are the site where gametophytes develop.

Most flowering plants depend on animals, such as bees, moths, and butterflies, to transfer their pollen between different flowers, and have evolved to attract these pollinators by various strategies, including brightly colored, conspicuous petals, attractive scents, and the production of nectar, a food source for pollinators. In this way, many flowering plants have co-evolved with pollinators be mutually dependent on services they provide to one another—in the plant's case, a means of reproduction; in the pollinator's case, a source of food. After fertilization, the ovary of the flower develops into fruit containing seeds.

Flowers have long been appreciated by humans for their beauty and pleasant scents, and also hold cultural significance as religious, ritual, or symbolic objects, or sources of medicine and food. '''

def summarization(rawdocs):
    stopwords = list(STOP_WORDS)

    nlp =spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

    tokens = [token.text for token in doc]

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] =1
            else:
                word_freq[word.text] +=1

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores ={}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens)*0.3)

    summary = nlargest(select_len,sent_scores,key = sent_scores.get)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    
    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))