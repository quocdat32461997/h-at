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
        dep_root = []
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
            dep_root.append(list(doc.sents)[0].root) # dep_root
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
                'dep_root' : dep_root,
                'ents' : ents, 
                'hypernyms' : hypernyms, 
                'hyponyms' : hyponyms,
                'meronyms' : meronyms, 
                'holonyms' : holonyms}
   
    def fill_born(self, sents, features):
        res = []
        for i, lemmas, ents, dep, root in zip(range(len(sents)), features['lem'], features['ents'], features['dep'], features['dep_root']):
            # in sentence
            try:
                # 1. Find index of the born verb in sentence
                index = lemmas.index('bear')    # Born is the past participle of the verb bear
                
                # parse entities
                def _parse_ents(inputs):
                    """
                    Parse entities into ORGs and DATEs
                    """
                    bornees, dates, locs = [], [], []
                    for ent in inputs:
                        if ent[-1] == 'DATE':
                            dates.append(ent[0])
                        elif ent[-1] == 'PERSON' or ent[-1] == 'ORG':
                            bornees.append(ent[0])
                        elif ent[-1] == 'LOC' or ent[-1] == 'GPE':  # LOC: Non-GPE locations, mountain ranges, bodies of water.; GPE: Countries, cities, states.
                            locs.append(ent[0])
                        
                    return bornees, dates, locs
                
                def _find_token_i_in_parse_tree(root, search_i):
                    """
                    Recursive tree search for value search_i == attribute i of the nodes.
                    """
                    if root is None or root.i == search_i:
                        return root
                    else:
                        for child in root.children:
                            node = _find_token_i_in_parse_tree(child, search_i)
                            if node is not None and node.i == search_i:
                                return child
                        return None
                
                # 2. Search for the parse tree node with i = index, the index of the 'bear' lemma previously found
                born_token = _find_token_i_in_parse_tree(root, index)
                print("sent: "+str(sents[i]))
                print("ents: "+str(ents))
                print("dep: "+str(dep)+"\n")
                
                # 3. Analyze the parents and children of the born node to fill in the BORN template
                bornee, loc, date = None, None, None
                # 3a. Find the person or org being born
                for child in born_token.children:
                    #if child.dep_ == 'nsubjpass' or child.dep_ == 'nsubj':    # Found the thing being born
                    print("child: "+str(child.text)+", ent: "+str(child.ent_type_))
                    if child.ent_type_ == 'PERSON' or child.ent_type_ == 'ORG':   # The thing is a PERSON or ORG
                        bornee = child.text
                        print("bornee: " + bornee)
                        break
                # 3b. Find their born date
                if bornee is not None:  # Once a bornee is found, look for their born location and date
                    for child in born_token.children:
                        # Look for the preposition of the born location and date
                        if child.dep_ == 'prep':
                            for grandchild in child.children:
                                print("grandchild: "+str(grandchild.text)+", ent: "+str(grandchild.ent_type_))
                                if grandchild.ent_type_ == 'DATE' and date is None:
                                    # Found the preposition date
                                    date = grandchild.text
                                if (grandchild.ent_type_ == 'LOC' or grandchild.ent_type_ == 'GPE') and date is None:
                                    # Found the preposition location
                                    loc = grandchild.text
                                    
                if bornee is not None:
                    res.append((bornee, date, loc))
                continue
                
                bornees, dates, locs = _parse_ents(ents)

                # get all possible ACQUIRE templates
                if len(bornees) < 1:
                    # find no entites
                    continue

                
                # Get person/org born (assumption: they're the subject of the sentence)
                if 'nsubj' in dep and lemmas[dep.index('nsubj')] in bornees:
                    # active
                    bornee = lemmas[dep.index('nsubj')]
                elif 'nsubjpass' in dep and lemmas[dep.index('nsubjpass')] in bornees:
                    # passive
                    bornee = lemmas[dep.index('nsubjpass')]
                else:
                    continue
                
                # Get location, if any (assumption: it's the first prepositional object in the sentence)
                if 'pobj' in dep and lemmas[dep.index('pobj')] in locs:
                    loc = lemmas[dep.index('pobj')]
                else:
                    loc = 'None'
                    
                # Get date, if any (assumption: it's the first date in the sentence)
                if len(dates) >= 1:
                    date = dates[0]
                else:
                    date = 'None'
                
                res.append({
                    'template' : 'BORN',
                    'sentences' : sents[i],
                    'arguments' : {
                    '1' : bornee,
                    '2' : loc, 
                    '3' : date}})
            except Exception as e:
                #print(e)
                pass
        return res
    
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
                temp = []
                if len(dates) == 1:
                    temp.append((buyer, orgs.pop(0), dates[-1]))
                else:
                    while dates and orgs:
                        temp.append((buyer, orgs.pop(0), dates.pop(0)))

                # add results
                while temp:
                    x = temp.pop()
                    res.append({
                        'template' : 'BUY',
                        'sentences' : sents[i],
                        'arguments' : {
                            '1' : x[0],
                            '2' : x[1],
                            '3' : x[2]}})
            except:
                pass
        return res
    
    def fill_part_of(self, sents, features):
        return []

    def fill(self, title, sents, features):
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
        templates = {'document' : title,
                'extractions' : []}
        # BORN template
        templates['extractions'].extend(self.fill_born(sents, features))
            
        # ACQUIRE template
        templates['extractions'].extend(self.fill_acquire(sents, features))
            
        # PART-OF template
        templates['extractions'].extend(self.fill_part_of(sents, features))
            
        print(templates)
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
