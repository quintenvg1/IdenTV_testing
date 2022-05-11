import re, json, os
class accesstoken_fetcher:

    def __init__(self, _access_token):
        print("init accesstoken fetcher test class")
        self.access_token = _access_token

    def get_access_token(self, process_output):#in plaats van telkens een nieuwe token te gaan vragen gebruiken we sample test data
        self.access_token = process_output
        #.decode("utf-8")
        #access token looks a little like this "outputprompt: {"access_token":"tokeznqsfioshdflshf","smthelse":"sdfsdf"},access token: accesstokengoiujdg"
        #attempt 1 drop the latter part of the string and keep the presumed json data
        access_token_jsonstring = re.search('{(.*)}', self.access_token)
        access_token_json = "{"+access_token_jsonstring.group(1)+"}" #now the data is in json format and can easily be transformed into a python dict
        access_token_dict = json.loads(access_token_json)
        self.access_token = access_token_dict["access_token"]
        return(self.access_token)#asserteer dat het de juiste string is
    
    def write_access_token_to_file(self):
        try:
            f = open("./access_token_clean.txt", "w")#will overwrite the tokenfile
            f.write(self.access_token)
            f.close()
            print("file successfully written")
        except:
            print("error in writing file")
            return("error in writing file, check permissions and script directory")
        try:
            f = open("./access_token_clean.txt", 'r')
            access_token_fromfile = f.read()
            f.close()
            print("read access token from file, tossing it out soon.")
            return(access_token_fromfile)
        except:
            print("error in opening file, check permissions and script direcotry")
            return("error in opening file")
