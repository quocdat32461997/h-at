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
            doc = self._nlp(sent)

            # add placeholder for each sentence
            pos.append([])
            tag.append([])
            dep.append([])
            lem.append([])
            ents.append([(ent.text, ent.label_) for ent in doc.ents])
            hypernyms.append([])
            hyponyms.append([])
            meronyms.append([])
            holonyms.append([])

            for tok in doc:
                lem[-1].append(tok.lemma_)
                pos[-1].append(tok.pos_) # pos
                tag[-1].append(tok.tag_) # tag
                dep[-1].append(tok.dep_) # dep

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
        for i, lemmas, ents, dep in zip(range(len(sents)), features['lem'], features['ents'], features['dep']):

            # in sentence
            try:
                # find index of acquire in lemmas
                index = lemmas.index('acquire') or lemmas.index('buy')

                # parse entities
                def _parse_ents(inputs):
                    """
                    Parse entities into ORGs and DATEs
                    """
                    dates, orgs = [], []
                    for ent in inputs:
                        if ent[-1] == 'DATE':
                            dates.append(ent[0])
                        elif ent[-1] == 'ORG':
                            orgs.append(ent[0])
                    return dates, orgs

                dates, orgs = _parse_ents(ents)

                # get all possible ACQUIRE templates
                if len(dates) < 1 or len(orgs) < 2:
                    # find no entites
                    continue

                # get buyer
                if lemmas[dep.index('nsubj')] == orgs[0]:
                    # active
                    buyer = orgs.pop(0)
                elif lemmas[dep.index('nsubjpass')] == orgs[-1]:
                    # passive
                    buyer = orgs.pop()
                else:
                    buyer = 'None'
                
                # get sellers
                if len(dates) == 1:
                    res.append((buyer, orgs.pop(0), dates[-1]))
                else:
                    while dates and orgs:
                        res.append((buyer, orgs.pop(0), dates.pop(0)))
            except:
                pass
        return res
    
    def fill_part_of(self, sents, features):
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
        print("Acquire Template: " + str(templates['ACQUIRE']))
            
        # PART-OF template
        templates['PART_OF'] = self.fill_part_of(sents, features)
            
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

        # to tokens
        tokens = [token.text for token in input_doc]

        # get pos, tags, lemmas, and dependency
        features = self._get_features(sents)

        return sents, tokens, features
