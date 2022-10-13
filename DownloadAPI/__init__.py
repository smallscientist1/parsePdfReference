from .dblp import dblp
from .crossref import crossref

__all__ = {
    "dblp": dblp,
    "crossref": crossref
}

def buildBibDownloader(db_name, file_list:list):
    assert db_name in __all__.keys()
    return __all__[db_name](file_list)