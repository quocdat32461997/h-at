# import dependencies
import os
import spacy
from nltk.corpus import wordnet

class NLP(object):
    """
    NLP pipeline
    """
    def __init__(self):
        """
        Constructor of NLP pipeline
        """
        self._nlp = spacy.load("en_core_web_sm")

        pass
    def _get_features(self, input):
        """
        Get lemma, pos, tag, dependency
        Args: 
            input ; list of str
                List of sentences
        Returns:
            _ : dict
                Dictionary of
                    'lem' : list(list(str))
                    'pos' : list(list(str))
                    'tag': list(list(str))
                    'dep' : list(list(str))
        """
        pos = []
        tag = []
        dep = []
        lem = []
        hypernyms, hyponems, meronyms, holonyms = [], [], [], []
        for sent in input:
            # add placeholder for each sentence
            pos.append([])
            tag.append([])
            dep.append([])
            lem.append({'dep': None, 'head_text': None, 'head_pos': None, 'children': []})
            hypernyms.append([])
            hyponyms.append([])
            meronyms.append([])
            holonyms.append([])
            
            # get doc with features
            doc = self._nlp(text)
            
            # parse features
            for tok in doc:
                pos[-1].append(tok.pos_) # pos
                tag[-1].append(tok.tag_) # tag
                dep[-1].appeend(tok.dep_) # dep
                lem[-1].append(tok.lemma_) # lemma

                # dependency
                dep[-1]['dep'] = tok.dep_
                dep[-1]['head_text'] = tok.head.text
                dep[-1]['head_pos'] = tok.head.pos_
                dep[-1]['children'] = list(tok.children)

                # wordnet features
                hypernyms[-1].append(
                        [x.hypernyms() for x in wordnet.synset(tok.text)])
                hyponyms[-1].append(
                        [x.hyponyms() for x in wordnet.synset(tok.text)])
                meronyms[-1].append(
                        [x.part_meronyms() for x in wordnet.synset(tok.text)])
                holonyms[-1].append(
                        [x.part_holonyms() for x in wordnet.synset(tok.text)])

        return {'lem': lem, 'pos': pos, 'tag': tag, 'dep': dep}

    def extract(self, input):
        """
        Extract NLP features 
        Args:
            input : str
        Returns:
            sents: list(str)
            tokeens: list(list(str))
            features: dict
                Dictionary of extracted lemmas, pos, tags, and dependencies
        """
        # to strings
        sents = None

        # to tokens
        tokens = None

        # get pos, tags, lemmas, and dependency
        features = self._get_features(sents)

        return sents, tokens, features
