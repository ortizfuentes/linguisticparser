# Linguisticparser

Linguisticparser allows you to segment paragraphs, sentences and words without making mistakes with acronyms and abbreviations.

You can also transform a text into a dataframe of sentences that include paragraph information.


## Installing

```
pip install git+https://github.com/ortizfuentes/linguisticparser
```

## Using

```
from linguisticparser.textparser import TextParser
mytext = 'I am a text example. This is a sentence. This is another sentence. \n\n This is another paragraph. The letters e.g mean for example.'
tp = TextParser(mytext, text_name='example')
tp.text2df_tokenize()
```

```
  text_name  num_paragraph  ...  num_subsentence                           wordings
0   example              1  ...                1               I am a text example.
1   example              1  ...                1                This is a sentence.
2   example              1  ...                1          This is another sentence.
3   example              2  ...                1         This is another paragraph.
4   example              2  ...                1  The letters e.g mean for example.

[5 rows x 5 columns]
```
## Other functions

### clean_text(text)

```
from linguisticparser.textparser import TextParser
mytext = 'I      am a text example. This is a sentence. This is another sentence. \n\n This is another paragraph. The letters e.g mean for example.'
mytext = TextParser.clean_text(mytext)
print(mytext)
```

```
I am a text example. This is a sentence. This is another sentence. \n This is another paragraph. The letters e.g mean for example.
```

### paragraphs_tokenize(text)

```
from linguisticparser.textparser import TextParser
paragraphs = TextParser.paragraphs_tokenize(mytext)
print(paragraphs)
```

```
['I am a text example. This is a sentence. This is another sentence.',
 'This is another paragraph. The letters e.g mean for example.']```
```

### sentence_tokenize(paragraph)

```
from linguisticparser.textparser import TextParser
sentences  = TextParser.sentence_tokenize(paragraphs[1])
print(sentences)
```

```
['This is another paragraph.', 'The letters e.g mean for example.']
```

### word_tokenize(sentence)

```
from linguisticparser.textparser import TextParser
words  = TextParser.word_tokenize(sentences[1])
print(words)
```

```
['The', 'letters', 'e.g', 'mean', 'for', 'example.']
```

