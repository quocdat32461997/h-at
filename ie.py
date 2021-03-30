# import dependencies
import os

class InforExtractor(object):
    """
    Class InfoExtractor 
    """
    def __init__(self, data):
        """
        Constructor of InforExtractor class
        Args:
            data : list of paths to data or a single path to data
        """

        # read text
        self.data = self._read_data(data)

    def _read_data(self, input):
        """
        Read text data
        Args:
            input : list of paths to data or a single path to data
        Returns:
            input : list of str
        """
        input = input if isinstance(input, list) else [input]
        input = [open(file).read() for file in input]
        return input

    def extract(self, input):
        """
        Extract all informations
        Args:
            input : str
                Path to input
        Returns: TBD
        """

        input = self._read_data(input)

        return None
