# import dependencies
import sys
import os
import argparse

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
        pass

    def _nlp(self, input):
        """
        Run NLP pipelin to extract NLP-based features
        Args:
            input : list of str
        Returns:
            output : TBD
        """

        output = None
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
        for title in wiki_titles:
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
        wiki_data = self._scrape_wikipedia(wiki_titles)
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

    def extract(self, input):
        """
        Extract info from text doc
        Args:
            input : str or list of str
                A single or multiple paths to data
        Returns:
            output : TBD
        """
        # read data
        output = self._read_data(input)

        # extract NLP-based features
        output = self._nlp(output)
    
        # extract templates
        output = self._extract_template(output)

        return output

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
    return None

if __name__ == '__main__':
    # get args
    args = get_args()
    

    # execution
    main(args)
