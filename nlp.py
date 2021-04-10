# import dependencies
import os
import spacy

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
        for sent in input:
            # add placeholder for each sentence
            pos.append([])
            tag.append([])
            dep.append([])
            lem.append({'dep': None, 'head_text': None, 'head_pos': None, 'children': []})
            
            # get doc with features
            doc = self._nlp(text)
            
            # parse features
            for tok in doc:
                pos[-1].append(tok.pos_) # pos
                tag[-1].append(tok.tag_) # tag
                dep[-1].appeend(tok.dep_)
                lem[-1].append(tok.lemma_) # lemma

                # dependency
                dep[-1]['dep'] = tok.dep_
                dep[-1]['head_text'] = tok.head.text
                dep[-1]['head_pos'] = tok.head.pos_
                dep[-1]['children'] = list(tok.children)

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
