class PyNapiTimeException(Exception):
    """Common excpetion for different cases
    """


class MovieNotFound(PyNapiTimeException):
    """Exception if video wasn't found in database.
    """


class SubtitlesNotFound(PyNapiTimeException):
    """Exception if subtitles were not found in subtitle database.
    """

class BadFile(PyNapiTimeException):
    """Exception if file is malformed or not supported."""