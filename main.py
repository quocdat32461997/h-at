# import dependencies
import sys
import os
import argparse
from tqdm import tqdm

from nlp import NLP
from ml import ML

class IE(object):
    """
    IE: Information Extraction class
    """
    def __init__(self, **kwargs):
        """
        Constructor
        Args:
            kwargs : dict
        """
        self._nlp = NLP()

    def _nlp_extract(self, input, title):
        """
        Run NLP pipeline to extract NLP-based features
        Args:
            input : str
                Input data
            title : str
                Input tile
                
        Returns:
            output : Tuples of (list of str, list of str, dict)
                Tuple with 3 items: a list of sentences, a list of tokens, and a dict of features
        """

        outputs = []
        for input, title in zip(inputs, titles):
            print('\nExtracting NLP features for article, {}'.format(title))
            outputs.append(self._nlp.extract(input))

        return outputs

    def _read_wiki_data(self, wiki_file_dir):
>>>>>>> aec62c69135142015c8edb9bd804fbedc6b6b879
        """
        Read data
        Args:
            wiki_file_dir : str
                Directory path containing Wikipedia articles as .txt files.
        Returns:
            wiki_data : list of str
                A list of the text corresponding (by list index) to the articles from the titles found in wiki_file_dir.
            wiki_titles : list of str
                A list of the article file names
        """
        wiki_titles = []
        wiki_data = []
        for file in os.listdir(wiki_file_dir):
            if os.path.isfile(os.path.join(wiki_file_dir, file)):
                wiki_titles.append(file)
                with open(os.path.join(wiki_file_dir, file), encoding='latin-1') as wiki_file:
                    wiki_data.append("".join(line.rstrip() for line in wiki_file))
        print("Found Wikipedia Articles/Files: "+str(wiki_titles))
        print("Done")
        return wiki_data, wiki_titles

    def _extract_template(self, sents, tokens, features, title):
        """
        Extract information following templates
        Args:
            sents : list
                A list of sentences in an article
            tokens : nested-list
                A list of list of tokens per article
            features : dict
                Dictionary of features
            title : str
                Article titlle
        Returns:
            outputs : list
                A list of all possible templates
        """
        print('Extracting templates for article, {}'.format(title))
        return self._nlp.fill(sents, features)

    def extract(self, wiki_file_dir):
        """
        Extract info from text doc
        Args:
            wiki_file_dir : str
                A single path to a directory with Wikipedia articles as .txt files.
        Returns:
            outputs : list
                A list of templates per article
        """
        # read data
        data, titles = self._read_wiki_data(wiki_file_dir)
        print("Total Data: "+str(sum([len(d.encode('utf-8')) for d in data]))+" bytes")

        # extract NLP-based features and file templates
        outputs = []
        for text, title in zip(data, titles):
            print("Extracting NLP Features:\n------------------------")
            sents, tokens, features = self._nlp_extract(text, title)
            
            print("Extracting templates:\n------------------------")
            outputs.append(self._extract_template(sents, tokens, features, title))

        print("------------------------\nDone")
    
        return outputs

class DefaultHelpParser(argparse.ArgumentParser):
    """
    DefaultHelpParser: ArgumentParser used by get_args() instead of the default ArgumentParser.
    This ArgumentParser prints the -h/--help and exits whenever there's an error.
    """
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def get_args():
    #initialize argument parser
    parser = DefaultHelpParser('Argument Paser for h-at, an Information Extraction tool')

    # add arguments
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-w', '--wiki',
                        metavar='<path>',
                        required=True,
                        help='Input path of directory to Wikipedia articles (.txt files) to read and analyze.')
    args = parser.parse_args()

    # validate input file
    if not os.path.isdir(args.wiki):
        print("error: \""+args.wiki+"\" does not exist")
        quit()

    return args

def main(args):
    print("\nH-AT: A Deep NLP Pipeline for Information Extraction\n====================================================")
    print("Input Wikipedia File Directory: "+args.wiki)
    my_ie = IE()
    my_ie.extract(args.wiki)
    print("====================================================\nFinished")

if __name__ == '__main__':
    # get args
    args = get_args()
    

    # execution
    main(args)
