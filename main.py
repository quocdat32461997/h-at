# import dependencies
import sys
import os
import argparse
from tqdm import tqdm

# For scraping Wikipedia articles for data
import wikipedia
import re

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

    def _nlp_extract(self, input):
        """
        Run NLP pipelin to extract NLP-based features
        Args:
            input : str
                Giant str of input data
        Returns:
            output : tuple of (list of str, list of str, dict)
                Tuple with 3 items: a list of sentences, a list of tokens, and a dict of features
        """

        output = self._nlp.extract(input)
        return output
        
    def _scrape_wikipedia(self, wiki_titles):
        """
        Scrape text from Wikipedia articles
        Args:
            wiki_titles : list of str
                A list of plain titles (not urls) to Wikipedia articles
                Ex: ["Alan Turing", "NASA"]
        Returns:
            wiki_texts : list of strs
                A list of the text corresponding (by list index) to the articles from wiki_titles
        """
        wiki_texts = []
        for i in tqdm(range(len(wiki_titles)), dynamic_ncols=True):
            title = wiki_titles[i]
            # Retrieve the wiki page
            wiki = wikipedia.page(title, auto_suggest=False)
            # Get the content (headers + paragraphs)
            text = wiki.content
            # Clean text by removing headers (surrounded by "==") and newlines
            text = re.sub(r'==.*?==+', '', text)
            text = text.replace('\n', ' ')
            
            wiki_texts.append(text)
        return wiki_texts
        
    def _read_wiki_titles(self, input_file):
        """
        Retrieve list of line-separated Wikipedia article titles from a file.
        Empty lines and lines starting with "#" are ignored.
        Article title validation is not performed.
        Ex:
            File:
                # Persons
                Alan Turing
                
                Albert Einstein
            Output: ["Alan Turing", "Albert Einstein"]
        Args:
            input_file : str
                File path containing a line-separated list of Wikipedia article titles.
        Returns:
            wiki_titles : list of str
                A list of the Wikipedia article titles retrieved from input_file
        """
        wiki_titles = []
        # Iterate through lines in file
        with open(input_file) as in_file:
            for line in in_file:
                # Check if not empty and not whitespace and doesn't start with "#"
                if line and (not line.isspace()) and (not line.strip().startswith('#')):
                    wiki_titles.append(line.strip())
        return wiki_titles

    def _read_wiki_data(self, wiki_title_file):
        """
        Read data
        Args:
            wiki_title_file : str
                File path containing a line-separated list of Wikipedia article titles.
        Returns:
            wiki_data : list of str
                A list of the text corresponding (by list index) to the articles from the titles found in wiki_title_file.
        """
        wiki_titles = self._read_wiki_titles(wiki_title_file)
        print("Scraping Wikipedia Articles: "+str(wiki_titles))
        wiki_data = self._scrape_wikipedia(wiki_titles)
        print("Done")
        return ' '.join(wiki_data)

    def _extract_template(self, input):
        """
        Extract information following templates
        Args:
            input : TBD
        Returns:
            output : TBD
        """
        output = None
        return output

    def extract(self, wiki_title_file):
        """
        Extract info from text doc
        Args:
            input_file : str
                A single path to a file with Wikipedia article titles
        Returns:
            output : TBD
        """
        # read data
        data = self._read_wiki_data(wiki_title_file)

        # extract NLP-based features
        print("Extracting NLP Features:\n------------------------")
        features = self._nlp_extract(data)
        print("------------------------\nDone")
        print("Sentences: "+str(len(features[0])))
        print("Tokens: "+str(len(features[1])))
    
        # extract templates
        templates = self._extract_template(features)

        return features, templates

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
                        help='Input file of line-separated titles to Wikipedia articles (not URLs) to scrape as input data.')
    args = parser.parse_args()

    # validate input file
    if not os.path.isfile(args.wiki):
        print("error: \""+args.wiki+"\" does not exist")
        quit()

    return args

def main(args):
    print("\nH-AT: A Deep NLP Pipeline for Information Extraction\n====================================================")
    print("Input Wikipedia File: "+args.wiki)
    my_ie = IE()
    my_ie.extract(args.wiki)
    print("====================================================\nFinished")

if __name__ == '__main__':
    # get args
    args = get_args()
    

    # execution
    main(args)
