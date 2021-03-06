from enum import Enum
from typing import List

import re

from pyminutiaeviewer.errors import CorruptFileError
from pyminutiaeviewer.minutia import Minutia, MinutiaType


class MinutiaeFileFormat(Enum):
    NBIST = "NBIST"
    MINDTCT = "MINDTCT"
    SIMPLE = "SIMPLE"
    XYT = "XYT"


class MinutiaeReader(object):
    def __init__(self, file_format: MinutiaeFileFormat):
        self._file_format = file_format
        if file_format == MinutiaeFileFormat.NBIST:
            self._parser = _parse_nbist_format
        elif file_format == MinutiaeFileFormat.MINDTCT:
            self._parser = _parse_nbist_format
        elif file_format == MinutiaeFileFormat.SIMPLE:
            self._parser = _parse_simple_format
        elif file_format == MinutiaeFileFormat.XYT:
            self._parser = _parse_xyt_format
        else:
            raise AttributeError("MinutiaeReader is not configured to read file format: {}".format(file_format))

    def read(self, absolute_file_path: str) -> List[Minutia]:
        """
        Reads minutiae from a text file.
        :param absolute_file_path: The absolute file path to the minutiae text file.
        :return: The minutiae.
        """
        with open(absolute_file_path) as f:
            lines = f.readlines()
            lines = [x.strip() for x in lines]

        return self._parser(lines)


# # # # # # # # # # # # # # # # # # # # # # # #
#
# File parsers
#
# # # # # # # # # # # # # # # # # # # # # # # #

def _parse_nbist_format(lines: List[str]) -> List[Minutia]:
    """
    Reads a NBIST format file that is generated by MINDTCT.
    :param lines: The lines of the text file.
    :return: The minutiae.
    """
    minutiae = []

    # Skip first two lines

    # Number of minutiae:
    num_minutiae = int(lines[2].split(' ')[0])

    # Skip blank line

    # read minutiae
    for line in lines[4:]:
        symbols = re.split('[:;, ]', line)
        symbols = list(filter(None, symbols))

        minutia_type = symbols[5]
        if minutia_type == "BIF":
            minutia_type = MinutiaType.BIFURCATION
        elif minutia_type == "RIG":
            minutia_type = MinutiaType.RIDGE_ENDING
        else:
            raise CorruptFileError("Unknown minutiae type '{}'".format(minutia_type))

        minutiae.append(Minutia(
            x=int(symbols[1]),
            y=int(symbols[2]),
            angle=float(symbols[3]) * 11.25,
            minutia_type=minutia_type,
            quality=float(symbols[4])
        ))

    # Ensure the number of minutiae read is the expected number:
    if len(minutiae) != num_minutiae:
        raise CorruptFileError("The file declared there would be  {} minutiae, but only read {}."
                               .format(num_minutiae, len(minutiae)))

    return minutiae


def _parse_simple_format(lines: List[str]) -> List[Minutia]:
    """
    Reads a simplified minutiae file.
    :param lines: The lines of the text file.
    :return: The minutiae.
    """
    minutiae = []

    for line in lines:
        symbols = line.split(' ')

        minutia_type = symbols[3]
        if minutia_type == "BIF":
            minutia_type = MinutiaType.BIFURCATION
        elif minutia_type == "END":
            minutia_type = MinutiaType.RIDGE_ENDING
        else:
            raise CorruptFileError("Unknown minutiae type '{}'".format(minutia_type))

        minutiae.append(Minutia(
            x=int(symbols[0]),
            y=int(symbols[1]),
            angle=float(symbols[2]),
            minutia_type=minutia_type,
            quality=float(symbols[4])
        ))

    return minutiae


def _parse_xyt_format(lines: List[str]) -> List[Minutia]:
    """
    Reads a xyt minutiae file.
    :param lines: The lines of the text file.
    :return: The minutiae.
    """
    minutiae = []

    for line in lines:
        symbols = line.split(' ')

        minutiae.append(Minutia(
            x=int(symbols[0]),
            y=int(symbols[1]),
            angle=float(symbols[2]),
            minutia_type=MinutiaType.RIDGE_ENDING,
            quality=float(symbols[3])
        ))

    return minutiae
