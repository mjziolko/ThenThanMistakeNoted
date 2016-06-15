import httplib, urllib, base64, json
from config import WLM_KEY

class WLMHandler:
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": WLM_KEY
    }
    
    params = urllib.urlencode({
         "model": "query"
    })
    
    def __init__(self):
        return
    
    def createJSONStructure(self, words):
        data = {
                    "queries":
                    [
                        { 
                            "words": words,
                            "word": "then"
                        },
                        {
                            "words": words,
                            "word": "than"
                         }
                     ]
                }
        return json.dumps(data)
    
    def deconstructJSONStructure(self, jdata):
        try:
            data = json.loads(jdata)
            thenthanData = {
                            data["results"][0]["word"]: data["results"][0]["probability"],
                            data["results"][1]["word"]: data["results"][1]["probability"] 
            }
            
            return thenthanData
        except:
            print jdata
            return None
    
    def sendRequest(self, jdata):
        try:
            conn = httplib.HTTPSConnection("api.projectoxford.ai")
            conn.request("POST", "/text/weblm/v1.0/calculateConditionalProbability?%s" % self.params, jdata, self.headers)
            response = conn.getresponse()
            data = response.read()
            return data
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    def thenOrThan(self, thenthanData):
        then = thenthanData["then"]
        than = thenthanData["than"]
        
        return ("then", then, than) if then > than else ("than", than, then)
    
    def determine(self, words):
        jdata = self.createJSONStructure(words)
        rjdata = self.sendRequest(jdata)
        data = self.deconstructJSONStructure(rjdata)
        
        if (data != None):
            return self.thenOrThan(data)
        else:
            return None