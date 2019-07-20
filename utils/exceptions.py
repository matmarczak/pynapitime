class PyNapiTimeException(Exception):
    """Common excpetion for diffrent cases
    """


class MovieNotFound(Exception):
    """Exception if video wasn't found in database.
    """


class SubtitlesNotFound(Exception):
    """Exception if subtitles were not found in subtitle database.
    """
