# import dependencies
import os
import spacy
from nltk.corpus import wordnet
from tqdm import tqdm
import neuralcoref
from collections import defaultdict

class NLP(object):
    """
    NLP pipeline
    """
    def __init__(self):
        """
        Constructor of NLP pipeline
        """
        self._nlp = spacy.load("en")
        neuralcoref.add_to_pipe(self._nlp)

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
        ents = []
        hypernyms, hyponyms, meronyms, holonyms = [], [], [], []
        for i in tqdm(range(len(input)), dynamic_ncols=True):
            sent = input[i]
            # add placeholder for each sentence
            pos.append([])
            tag.append([])
            dep.append([])
            ents.append([(ent.text, ent.label_) for ent in self._nlp(sent).ents])
            lem.append({'dep': None, 'head_text': None, 'head_pos': None, 'children': []})
            hypernyms.append([])
            hyponyms.append([])
            meronyms.append([])
            holonyms.append([])
            
            # get doc with features
            doc = self._nlp(sent)
            
            # parse features
            for tok in doc:
                pos[-1].append(tok.pos_) # pos
                tag[-1].append(tok.tag_) # tag
                dep[-1].append(tok.dep_) # dep

                # lemma
                lem[-1]['dep'] = tok.dep_
                lem[-1]['head_text'] = tok.head.text
                lem[-1]['head_pos'] = tok.head.pos_
                lem[-1]['children'] = list(tok.children)

                # wordnet features
                hypernyms[-1].append(
                        [x.hypernyms() for x in wordnet.synsets(tok.text)])
                hyponyms[-1].append(
                        [x.hyponyms() for x in wordnet.synsets(tok.text)])
                meronyms[-1].append(
                        [x.part_meronyms() for x in wordnet.synsets(tok.text)])
                holonyms[-1].append(
                        [x.part_holonyms() for x in wordnet.synsets(tok.text)])

        return {'lem' : lem,
                'pos' : pos, 
                'tag' : tag, 
                'dep' : dep, 
                'ents' : ents, 
                'hypernyms' : hypernyms, 
                'hyponyms' : hyponyms,
                'meronyms' : meronyms, 
                'holonyms' : holonyms}
   
    def fill_born(self, sents, features):
        return None
    
    def fill_acquire(self, sents, features):
        res = []
        for x in features['ents']:
            print(x)
            
        return None
    
    def fill_part_of(self):
        return None

    def fill(self, sents, features):
        """
        Fill templates of BORN, ACQUIRE, and PART_OF pert article
        Args:
            sents : list of str
                A list of str per article
            features : dict
                Dictionary of features
        Returns:
            output : list
                A list of filled templates
        """
        templates = defaultdict(list)
        # BORN template
        templates['BORN'] = self.fill_born(sents, features)
            
        # ACQUIRE template
        templates['ACQUIRE'] = self.fill_acquire(sents, features)
            
        # PART-OF template
            
        return templates

    def extract(self, input):
        """
        Extract NLP features 
        Args:
            input : str
        Returns:
            sents: list(str)
            tokens: list(list(str))
            features: dict
                Dictionary of extracted lemmas, pos, tags, and dependencies
        """
        input_doc = self._nlp(input)

        # to sentences
        sents = [sent.text for sent in input_doc.sents]

        # get corefs
        corefs = input_doc._.coref_clusters if input_doc._.has_coref else []

        # to tokens
        tokens = [token.text for token in input_doc]

        # get pos, tags, lemmas, and dependency
        features = self._get_features(sents)
        features['corefs'] = corefs

        return sents, tokens, features
