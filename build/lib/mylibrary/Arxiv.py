"""
Refer to https://arxiv.org/help/api/user-manual for the description of Arxiv API.


Summary:
ArXiv request returns in the Atom format ().


Note:
Refer to https://arxiv.org/help/prep for metadata spec.

Since new submissions are updated only once in a day, 
the same query to the ArXiv API will only be updated once a day.
Thus, repeated query in the same day should be refrained. 

To do:
------
Check for replacement of an article.
Check if published version is available. 
- First determine if it will never be published elsewhere. - e.g., white paper.

"""

from urllib3 import PoolManager

def get_sentence_standard(ll, tag):
    return ll.split("</{}>".format(tag))[-2].split("<{}>".format(tag))[-1]

def parse_arxiv(arx, qresult):
    """
    Note
    ----
    Summary is multi-line. 
    One author comprises multiple sub-entries (name/affiliation, and more?),
    and there may be multiple authors.

    Non atom-standard fields look arbitrary in formats.
    I don't expect these hardcoded parsing will always work...
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
                arx.id=get_sentence_standard(ll, "id").split("/")[-1]
            if arx.updated is None and "<updated>" in ll:
                arx.updated = get_sentence_standard(ll, "updated")
            if arx.published is None and "<published>" in ll:
                arx.published = get_sentence_standard(ll, "published")
            if arx.title is None and "<title>" in ll:
                arx.title = get_sentence_standard(ll, "title")
            if _ibeg_summary is None and "<summary>" in ll:
                _ibeg_summary = i
            if _iend_summary is None and "</summary>" in ll:
                _iend_summary = i
            if read_author:
                arx.authors.append(get_sentence_standard(ll, "name"))
                read_author=False
            if not read_author and "<author>" in ll:
                read_author = True
            if arx.doi is None and "":
                arx.doi = ll.split(">")[1].split("<")[0]
            if arx.primary_category is None and "arxiv:primary_category" in ll:
                arx.primary_category = ll.split('"')[3]
            if "category term" in ll:
                arx.categories.append(ll.split('"')[1])
                

    arx.summary = "".join(lines[_ibeg_summary:_iend_summary]).split("<summary>")[1]
    


#def 

class Arxiv_meta():
    """
    """
    def __init__(self, id=None, load=True):
        self.title=None
        self.published=None
        self.updated=None
        self.authors=[]
        self.primary_category=None
        self.categories=[]
        self.summary=None
        self.doi=None
        self.id=str(id)
        if load:
            self.query_by_id(self.id)

    def query_by_id(self, parse=True, return_raw=False):
        """
        Will it be better to keep PoolManager as a single, global instance?
        """
        http = PoolManager()
        r = http.request("GET", "http://export.arxiv.org/api/query?id_list={}".format(self.id))
        if parse:
            parse_arxiv(self, r.data)
        if return_raw:
            return r.data


