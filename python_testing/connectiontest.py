#original imports
from lib2to3.pgen2 import token
import requests
import time
import unittest
import access_token_tests as mytokenhandler
#end original imports

class TestStringMethods(unittest.TestCase):
    #set test variables
    global delay
    delay = 0
    f = open('access_token.txt', 'r')#verkijg de testdata uit de file
    global test_token_data
    test_token_data = f.read()
    global testhandler
    testhandler = mytokenhandler.accesstoken_fetcher(test_token_data)

    #testing starts here
    def test_ig_connection(self):
        print("connectiviteit testen met de IG")
        global delay
        url = "http://identit-stage02.nynox.lcl:9090"
        starttime = time.process_time() #tijd tot completie
        response = requests.get(url)#ping de web server
        delay = time.process_time() - starttime #bereken verstreken tijd
        print(response) #print het antwoord van de server
        self.assertTrue(response)
    #endtest
    def test_ig_delay(self):
        print("controlleren van delay naar de IG")
        global delay
        print("delay " + str(delay))
        self.assertTrue(delay <= 0.5) #ig heeft minder dan 500ms delay, zoals omschreven in testplan
    #endtest    #endtest
    def test_openam_connection(self):
        global delay
        print("connectiviteit testen met de authenticatieserver on premise")
        url = "http://identit-stage02.nynox.lcl:8081/openam"
        starttime = time.process_time()
        #delay = ('%s: %.3f' % (self.id(), starttime))
        response = requests.get(url)#ping the web server
        delay = time.process_time() - starttime
        print(response)
        self.assertTrue(response)
    #endtest
    def test_openam_delay(self):
        print("controlleren van de delay naar de authenticatieserver")
        global delay
        print("delay " + str(delay))
        self.assertTrue(delay <= 0.5)
    #endtest
    #endpoint connectie testen
    def test_authenticatie_endpoint(self):
        url = "http://identit-stage02.nynox.lcl:8081/openam/json/authenticate" #should return a 405 unauthorized
        global delay
        starttime = time.process_time()
        response = requests.get(url)
        delay = time.process_time() - starttime
        print(response)
        self.assertFalse(response) #response bevat een 405 unauthorized en wordt gezien als assertFalse
    #endtest
    def test_authendpoint_delay(self):
        print("controlleren van de delay naar de authenticatie endpoint")
        global delay
        print("delay " + str(delay))
        self.assertTrue(delay <= 0.5)
    #endtest
    def test_login_route(self):
        global delay
        url = "http://identit-stage02.nynox.lcl:8081/openam/XUI/?realm=alpha&authIndexType=service&authIndexValue=Login"
        starttime = time.process_time()
        response = requests.get(url)
        delay = time.process_time() - starttime
        self.assertFalse("404" in response) #testen dat de login route bestaat en bereikbaar is.
    #endtest
    def test_login_journey_sanity(self):
        global delay
        print("controlleren van de delay naar de login journey")
        self.assertTrue(delay <= 0.5)
    #endtest
    def test_portal_connection(self): #test de verbinding naar het gebruikers portaal
        print("gebruikersportaal testen")
        global delay
        url = "http://identit-stage02.nynox.lcl:8080/index.html"
        starttime = time.process_time()
        response = requests.get(url)
        delay = time.process_time() - starttime
        self.assertTrue(response) #testen dat de login route bestaat en bereikbaar is
    #endtest
    def test_portal_sanity(self):
        print("gebruikersportaal delay testen")
        global delay
        print(delay)
        print("controlleren van de delay naar het gebruikersportaal")
        self.assertTrue(delay <= 0.5)
    #endtest
    #access token testing
    def test_access_token_filter(self):
        global testhandler
        print("attempting to get test data")
        f = open('access_token.txt', 'r')#verkijg de testdata uit de file
        test_token_data = f.read()
        f.close()
        print("intialising token handler")
        mytoken = testhandler.get_access_token(test_token_data)
        #if(str(mytoken) == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIodXNyIXJhc3BiZXJyeXBpKSIsImN0cyI6Ik9BVVRIMl9TVEFURUxFU1NfR1JBTlQiLCJhdWRpdFRyYWNraW5nSWQiOiJiMWFjNzZiOC0wMjk5LTRhMGUtYjg2OS0wMzMzN2NhZjVjNzgtNDEwNjkxNyIsInN1Ym5hbWUiOiJyYXNwYmVycnlwaSIsImlzcyI6Imh0dHA6Ly9pZGVudGl0LXN0YWdlMDIubnlub3gubGNsOjgwODEvb3BlbmFtL29hdXRoMi9yZWFsbXMvcm9vdC9yZWFsbXMvYWxwaGEiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJxNUdLdENwSDNLeHN1UFVtVTlHcnUweTlIVGMiLCJhdWQiOiJmb3JnZXJvY2staW90LW9hdXRoMi1jbGllbnQiLCJuYmYiOjE2NTIyNjE5NTcsImdyYW50X3R5cGUiOiJ1cm46aWV0ZjpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTpqd3QtYmVhcmVyIiwic2NvcGUiOlsicHVibGlzaCJdLCJhdXRoX3RpbWUiOi0xLCJyZWFsbSI6Ii9hbHBoYSIsImV4cCI6MTY1MjI2NTU1NywiaWF0IjoxNjUyMjYxOTU3LCJleHBpcmVzX2luIjozNjAwLCJqdGkiOiJZVGRZMHl2UHphc2tKRmp1Ml80Y3RIdURTcXcifQ.euSjyckJ7x87W-vNKFY5fRTe3-8zDZk9kQ1ljBHexRs"):
        #    print("token correct")
        self.assertTrue(mytoken == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIodXNyIXJhc3BiZXJyeXBpKSIsImN0cyI6Ik9BVVRIMl9TVEFURUxFU1NfR1JBTlQiLCJhdWRpdFRyYWNraW5nSWQiOiJiMWFjNzZiOC0wMjk5LTRhMGUtYjg2OS0wMzMzN2NhZjVjNzgtNDEwNjkxNyIsInN1Ym5hbWUiOiJyYXNwYmVycnlwaSIsImlzcyI6Imh0dHA6Ly9pZGVudGl0LXN0YWdlMDIubnlub3gubGNsOjgwODEvb3BlbmFtL29hdXRoMi9yZWFsbXMvcm9vdC9yZWFsbXMvYWxwaGEiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJxNUdLdENwSDNLeHN1UFVtVTlHcnUweTlIVGMiLCJhdWQiOiJmb3JnZXJvY2staW90LW9hdXRoMi1jbGllbnQiLCJuYmYiOjE2NTIyNjE5NTcsImdyYW50X3R5cGUiOiJ1cm46aWV0ZjpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTpqd3QtYmVhcmVyIiwic2NvcGUiOlsicHVibGlzaCJdLCJhdXRoX3RpbWUiOi0xLCJyZWFsbSI6Ii9hbHBoYSIsImV4cCI6MTY1MjI2NTU1NywiaWF0IjoxNjUyMjYxOTU3LCJleHBpcmVzX2luIjozNjAwLCJqdGkiOiJZVGRZMHl2UHphc2tKRmp1Ml80Y3RIdURTcXcifQ.euSjyckJ7x87W-vNKFY5fRTe3-8zDZk9kQ1ljBHexRs")
    #endtest
    def test_file_write(self):
        global testhandler
        token = (testhandler.write_access_token_to_file())
        print("test passes if string and key have the same value")
        self.assertTrue(token == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIodXNyIXJhc3BiZXJyeXBpKSIsImN0cyI6Ik9BVVRIMl9TVEFURUxFU1NfR1JBTlQiLCJhdWRpdFRyYWNraW5nSWQiOiJiMWFjNzZiOC0wMjk5LTRhMGUtYjg2OS0wMzMzN2NhZjVjNzgtNDEwNjkxNyIsInN1Ym5hbWUiOiJyYXNwYmVycnlwaSIsImlzcyI6Imh0dHA6Ly9pZGVudGl0LXN0YWdlMDIubnlub3gubGNsOjgwODEvb3BlbmFtL29hdXRoMi9yZWFsbXMvcm9vdC9yZWFsbXMvYWxwaGEiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJxNUdLdENwSDNLeHN1UFVtVTlHcnUweTlIVGMiLCJhdWQiOiJmb3JnZXJvY2staW90LW9hdXRoMi1jbGllbnQiLCJuYmYiOjE2NTIyNjE5NTcsImdyYW50X3R5cGUiOiJ1cm46aWV0ZjpwYXJhbXM6b2F1dGg6Z3JhbnQtdHlwZTpqd3QtYmVhcmVyIiwic2NvcGUiOlsicHVibGlzaCJdLCJhdXRoX3RpbWUiOi0xLCJyZWFsbSI6Ii9hbHBoYSIsImV4cCI6MTY1MjI2NTU1NywiaWF0IjoxNjUyMjYxOTU3LCJleHBpcmVzX2luIjozNjAwLCJqdGkiOiJZVGRZMHl2UHphc2tKRmp1Ml80Y3RIdURTcXcifQ.euSjyckJ7x87W-vNKFY5fRTe3-8zDZk9kQ1ljBHexRs")
    #endtest
    def test_reverseproxyhandler_security(self):
        url = "http://identit-stage02.nynox.lcl:9090/videos/galaxy.mp4"
        response = requests.get(url)#should return a 401 unauthorized
        print(response)
        self.assertFalse(response)
    #endtest
    def test_reverseproxyhandler_security_pt2(self):
        url = "http://identit-stage02.nynox.lcl:9090/videos/galaxy.png"
        response = requests.get(url)#should return a 401 unauthorized
        print(response)
        self.assertTrue(response)
    #endtest
    def test_kodi_video_list(self):
        url = "http://identit-stage02.nynox.lcl:9090/videos/kodi_video_list"
        response = requests.get(url)
        print("response")
        self.assertTrue(response)
    #endtest
if __name__ == '__main__':
    unittest.main()
