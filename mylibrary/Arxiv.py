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
"""
Will it be better to keep PoolManager as a single, global instance?
"""
http = PoolManager()


def get_sentence_standard(ll, tag):
    return ll.strip("<"+tag).split(">")[1].split("<")[0]

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
    key=None
    entry=False

    i_beg=-1
    i_end=-1

    for i, ll in enumerate(lines):
        if "</entry>" in ll:
            break
        if "<entry>" in ll:
            entry=True
            continue
        
        if entry:
            if i_beg <0:
                # update key
                try:
                    key = ll.split("<")[1].split(">")[0]
                except:
                    continue
                try:
                    key = key.split()[0].split(":")[1]
                    key_escape = "arxiv:" + key
                except:
                    key_escape = key
                    pass
                if key in arx.meta.keys():
                    #if arx.meta[key] is None:
                    i_beg=i
                        
                    if "</{}>".format(key_escape) in ll:
                        # If one-line string
                        i_end=i
            elif "</{}>".format(key_escape) in ll:
                # if multi-line string
                i_end = i            
            if i_end > 0:
                arx.meta[key]=get_sentence_standard("".join(lines[i_beg:i+1]).strip(), key_escape)#.split("/")[-1]
                i_beg=i_end=-1


#def 

class Arxiv_meta():
    """
    """
    def __init__(self, id=None, load=True):
        self.meta = dict(
            title=None,
            published=None,
            updated=None, 
            authors=None,
            primary_category=None,
            categories=[],
            summary=None, 
            doi=None,
            id=str(id),
            journal_ref=None,
            )
        
        if load:
            self.query_by_id(self.meta["id"])

    def _get_ads_query(self):
        return http.request("GET", "http://export.arxiv.org/api/query?id_list={}".format(self.meta["id"]))

    def query_by_id(self, parse=True, return_raw=False):
        r = self._get_ads_query()
        
        if parse:
            parse_arxiv(self, r.data)
        if return_raw:
            return r.data


