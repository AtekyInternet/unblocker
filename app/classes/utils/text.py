import unicodedata

class Text:
    
    @staticmethod 
    def normalize(text):
        ntdk_form = unicodedata.normalize('NFKD', text)
        return ntdk_form.encode('ascii','ignore')