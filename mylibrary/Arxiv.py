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

#from urllib3 import PoolManager
import requests
from lxml import etree

"""
Will it be better to keep PoolManager as a single, global instance?
"""
#http = PoolManager()

class Arxiv_meta():
    """
    """
    def __init__(self, id=None, load=True):
        self.meta = dict(
            title=None,
            published=None,
            updated=None, 
            author=[],
            primary_category=None,
            category=[],
            summary=None, 
            doi=None,
            id=str(id),
            journal_ref=None,
            )
        
        if load:
            self.query_by_id(self.meta["id"])

    def _get_ads_query(self):
        return requests.get("http://export.arxiv.org/api/query?id_list={}".format(self.meta["id"])).raw
        #return http.request("GET", "http://export.arxiv.org/api/query?id_list={}".format(self.meta["id"]))

    def query_by_id(self, parse=True, return_raw=False):
        r = self._get_ads_query()
        
        if parse:
            self.parse_xml(r.data)
        if return_raw:
            return r.data

    def parse_xml(self, xml_data):
        root = etree.fromstring(xml_data)

        for element in root.find("{http://www.w3.org/2005/Atom}entry"):
            name = element.tag.split("}")[-1]
            if name == "author":
                for Echild in element.getchildren():
                    self.meta[name].append(Echild.text)            
            else:
                try:
                    if isinstance(self.meta[name], list):
                        try:
                            self.meta[name].append(element.attrib["term"])
                        except:
                            self.meta[name].append(element.text)
                    else:
                        try:
                            self.meta[name] = element.attrib["term"]
                        except:
                            self.meta[name] = element.text
                except:
                    continue

    def _strip_parsed_text(self):
        pass
