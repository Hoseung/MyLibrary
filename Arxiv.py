"""
Refer to https://arxiv.org/help/api/user-manual for the description of Arxiv API.


Summary:
ArXiv request returns in the Atom format ().


Note:
Since new submissions are updated only once in a day, 
the same query to the ArXiv API will only be updated once a day.
Thus, repeated query in the same day should be refrained. 
"""

from urllib3 import PoolManager


class Arxiv_meta():
    """
    """
    def __init__(self):
        self.title=None
        self.id=None
        self.published=None
        self.updated=None
        self.authors=[]
        self.category=None
        self.summary=None
        

def arxiv_query_by_id(id):
    http = PoolManager()
    r = http.request("GET", "http://export.arxiv.org/api/query?id_list={}".format(id))
    return r.data

def get_sentence(ll, tag):
    return ll.split("</{}>".format(tag))[-2].split("<{}>".format(tag))[-1]

def parse_arxiv(arx, qresult):
    """
    Note
    ----
    Summary is multi-line. 
    One author comprises multiple sub-entries (name/affiliation, and more?),
    and there may be multiple authors.
    """

    lines = qresult.decode("UTF-8").split("\n")
    entry=False
    _ibeg_summary=None
    _iend_summary=None
    read_author=False
    for i, ll in enumerate(lines):
        if "</entry>" in ll:
            break
        if "<entry>" in ll:
            entry=True
        if entry:
            if arx.id is None and "<id>" in ll:
                arx.id=get_sentence(ll, "id").split("/")[-1]
            if arx.updated is None and "<updated>" in ll:
                arx.updated = get_sentence(ll, "updated")
            if arx.published is None and "<published>" in ll:
                arx.published = get_sentence(ll, "published")
            if arx.title is None and "<title>" in ll:
                arx.title = get_sentence(ll, "title")
            if _ibeg_summary is None and "<summary>" in ll:
                _ibeg_summary = i
            if _iend_summary is None and "</summary>" in ll:
                _iend_summary = i
            if read_author:
                arx.authors.append(get_sentence(ll, "name"))
                read_author=False
            if not read_author and "<author>" in ll:
                read_author = True

    arx.summary = "".join(lines[_ibeg_summary:_iend_summary]).split("<summary>")[1]
    