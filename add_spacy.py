#pip install -U spacy
#python -m spacy download de
import spacy

nlp = spacy.load('de')
doc = nlp(u'This is a sentence.')