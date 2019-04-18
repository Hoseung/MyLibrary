import json
import requests
from lxml import etree

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

def _store_token(token):
    with open(".token.dat", "w") as f:
        f.write(token)


def get_journal_ref(journal_str):
    """
    To do
    -----

    refer to 
    """
    pass

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


        To do
        -----
        Some keywords of meta are different from those of arxiv.meta.
        -> Try using a custom format export (http://adsabs.github.io/help/actions/export)

        """
        self.meta = dict(
            title=None,
            journal=None,
            journal_ref=None,
            volume=None,
            page=None,
            lastpage=None,
            year=None,
            month=None,
            keywords=[],            
            pubdate=None, 
            author=[],
            url=None,
            abstract=None, 
            DOI=None,
            eprintid=None,
            )
        # to be compared with _generate_bibcode
        self.bibcode=self.meta["url"].split("/")[-1]
        
        
    def _generate_bibcode(self):
        """
        Specification: http://adsabs.github.io/help/actions/bibcode
        19 digits: YYYYJJJJJVVVVMPPPPA, where
        Y = year, J = Journal abbreviation, V = volume, M = qualifer for publication,
        P = page, A = First letter of the last name of the first author.
        """
        return "{:4d}{:.<5}{:4d}{:1s}{:4d}{:1s}".format(self.meta["year"],
                                                        self.meta["journal_ref"],
                                                        self.meta["volume"],
                                                        ".",
                                                        self.meta["pages"],
                                                        self.meta["author"][0][0])
    def request_by_bibcode(self, bibcode):
        r = requests.post("https://api.adsabs.harvard.edu/v1/metrics", \
                 headers={"Authorization": User + token, "Content-type": "application/json"}, \
                 data=json.dumps(bibcode))
        return r.json()

    def ref_by_bibcode(self, bibcode, format="refabsxml"):
        """
        format = {bibtex, bibtexabs, ads, endnote, rss, refxml, refabsxml, cusmtom, ...}

        NOTE
        ----
        bibtexabs = bibtex + abstract.
        refabsxml = abstract + xml feed
        """
        return requests.post("https://api.adsabs.harvard.edu/v1/export/"+format, \
                 headers={"Authorization": User + token,
                  "Content-type": "application/json"}, 
                 data=json.dumps(bibcode)).json

    def parse_bibtex_pybtex(self, json_bib):
        import pybtex
        chk = json_bib["msg"] # message
        db = pybtex.database.parse_string(json_bib["export"], bib_format="bibtex")
        ent = db.entries[self.extract_bibcode(json_bib)]
        # Todo
        # parse ent

    def parse_bibtex(self, json_bib):
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(json_bib["export"].encode("utf-8"), parser=parser)
        #for element in root.find("{http://ads.harvard.edu/schema/abs/1.1/abstracts}record"):
        keys = self.meta.keys()
        for element in root.find("{http://ads.harvard.edu/schema/abs/1.1/abstracts}record"):
            name = element.tag.split("}")[-1]
            if name in keys:
                if isinstance(self.meta[name], list):
                    if len(element.getchildren()) > 0:
                        for Echild in element.getchildren():
                            self.meta[name].append(Echild.text)             
                    else:
                        self.meta[name].append(element.text)   
                else:
                    try:
                        self.meta[name] = element.attrib["term"]
                    except:
                        self.meta[name] = element.text

    def extract_bibcode(self, json_bib):
        return json_bib["export"].split("{")[1].split(",")[0]

    def request_citations(self):
        return requests.post("https://ui.adsabs.harvard.edu/link_gateway/"+\
            self.bibcode+"/citations").json()

    def standardize_meta(self):
        # year
        try:
            self.meta["month"], self.meta["year"] = self.meta["pubdate"].split()
            self.meta["year"] = int(self.meat["year"])
        except:
            pass

        # Journal abbv
        try:
            self.meta["journal_ref"] = get_journal_ref(self.meta["jorunal"])
        except:
            pass

    