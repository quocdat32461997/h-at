# import dependencies
import os
import argparse

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

    def _read_data(self, input):
        """
        Read data
        Args:
            data : str or list of str
                A single or list of paths to data
        Returns:
            TBD
        """
        data = data if isinstance(data, list) else [data]
        data = [open(file).read() for file in data]
        return data

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

def get_args():
    #initialize argument parser
    parser = argparse.ArgumentParser('Argument Paser for h-at, an Information Extraction tool')

    # add arguments
    parser.add_argument('--input', type = str, help = 'Text input')

    return parser.parse_args()

def main(args):
    return None

if __name__ == '__main__':
    # get args
    args = get_args()
    

    # execution
    main(args)
