# Journal abbv. should be standardized.
# Titles may include special characters. - what should I do with them?
# 


class PdfParser():
    """
    Required functionalities:
    1. get Arxiv ID or Journal name + doi
    2. get title
    3. get author list
    4. 
    """
    def __init__(self):
        pass


class BibTex():
    """
    Refer to bibtex standard. 
    But I don't need them all. 
    Keep the information field as short as possible.

    There probably be some tools to work with bibtex.
    """
    def __init__(self):
        self.fields=dict()

    def journal(self):
        """
        Based on ADS search result, determine in which journal the paper has been published.
        """
        # Do some string comparing things. -> distance measuring! 
        self.fields["journal"] = ""

        

class Library():
    """
        Contains global data. 
        Functions to deal with SinglePaper entries.

    """
    def __init__(self):
        self.keywords=[]
        self.__Arxiv_url=""
        self.__ADS_url=""
        self.__journals=[]



class ADS_result():
    """
    A container of ADS search result.
    """
    def __init__(self):
        pass


class SinglePaper():
    """
        Note
        ----
        Take advantage of existing bibtex fields as much as possible.

        Some papers might not appear on Arxiv. -- Those with embargo.
    """
    def __init__(self):
        self.ArXivID=None
        #self._title=""
        #self.author1=""
        #self.year=""
        #self.journal=""
        self.bibtex=BibTex()
        self._file=""
        self._keywords=[]


    def check_published(self):
        if self.bibtex.journal is not None:
            return
        ads = search_ads(self.ArXivID)

        try:
            self.bibtex.ads.journal(ads.journal)
        except:
            print("preprint since {}. {}.".format(self.bibtex["year"], self.bibtex["month"]))
