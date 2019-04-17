import json
import requests

"""
To do
1. How should I store and read my token?
2. Is there other option than json? 
3. If I need to use json, can I avoide using xml in arxiv?
4. How to retrieve citation list?
5. 
"""

token = "asdf"
User  = "hoseung"

ADS_fields=["author", "title", "journal", "archivePrefix", "eprint", 
        "keywords", "year", "month", 
        "volume", "eid", "pages", 
        "doi", "adsurl", "adsnote"]

class ADS_bib():
    """
    There're some overlaps between Arxiv and ADS metadata. 
    Figureout how I should deal with these redundancy. 
    """
    def __init__(self, bib=None):
        self.bib = dict(
            title=None,
            journal=None,
            archivePrefix=None, 
            eprint=None,
            keywords=None,
            year=None,
            month=None, 
            volume=None,
            eid=None,
            pages=None,
            doi=None,
            adsurl=None,
            adsnote=None)
    
        if bib is not None:
            self.parse_bib(bib)
    
    def parse_bib(self, bib):
        """
        
        To do
        -----
        1. Identify each name of author.
        1.1 Simply removing all {} will make identifying author's last names impossible... Hmm.. 
        2. Interpret journal abbreviation (with escape characteres) correctly. 
        3. Keywords field format is a bit complicated...!
        
        """
        for ll in bib.split("\n"):
            # fields should appear only once.
            # Should I remove each field on being mathced?
            for ff in ADS_fields:
                if ff in ll:
                    name, value = ll.translate(str.maketrans('', '', "{},'")).split("=")
                    try:
                        self.bib[name.strip()]=int(value)
                    except:
                        self.bib[name.strip()]=value.strip()


class ADS():
    def __init__(self):
        """
        bibcode = {"bibcodes":["2003ApJS..148..175S"]}
        """
        self.bibcode=""

    def generate_bibcode(self):
        pass

    def metric_by_bibcode(self, bibcode):
        r = requests.post("https://api.adsabs.harvard.edu/v1/metrics", \
                 headers={"Authorization": User + token, "Content-type": "application/json"}, \
                 data=json.dumps(bibcode))
        return r.json()

    def bibtex_by_bibcode(self, bibcode):
        r = requests.post("https://api.adsabs.harvard.edu/v1/export/bibtex", \
                 headers={"Authorization": User + token, "Content-type": "application/json"}, \
                 data=json.dumps(bibcode))
        return r.json()

    