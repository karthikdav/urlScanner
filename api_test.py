import requests
import unittest

host = "http://192.168.0.34:3200"

class AppUnitTest(unittest.TestCase):

    # Test case for insert an url
    def test_a_insertrecord(self):
        print("Currently Executing {}".format(self._testMethodName))
        try:
            url = host + "/rest/api/v1/urlScanner/add"
            inserturl = "www.yahoo.com"
            payload = {'insert_url': inserturl}
            response = requests.request("POST", url, data=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, "the insert_url is " + inserturl)
        except Exception as e:
            print('Exception occurred while testing inserting the record{}'.format(e))
            assert False

    # Test case for update a record
    def test_b_updaterecord(self):
        print("Currently Executing {}".format(self._testMethodName))
        try:
            url = host + "/rest/api/v1/urlScanner/1"
            updateurl = "www.google.com"
            id = url.rsplit('/', 1)[-1]
            payload = {'update_url': updateurl}
            response = requests.request("PUT", url, data=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, "url id with " + id + " is updated with url string " + updateurl)
        except Exception as e:
            print('Exception occured while testing updating the record{}'.format(e))
            assert False

    # Test case for clearing the table values
    def test_d_vanishrecord(self):
        print("Currently Executing {}".format(self._testMethodName))
        try:
            url = host + "/rest/api/v1/urlScanner/1"
            response = requests.request("DELETE", url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, "url id with 1 is Deleted")
        except Exception as e:
            print('Exception occurred while testing deleting the record{}'.format(e))
            assert False

    # test case for checking whether an URL is present
    def test_c_urlcheck(self):
        print("Currently Executing {}".format(self._testMethodName))
        try:
            url = host + "/rest/api/v1/urlScanner/isSafeUrl?hostname=www.google.com&originalpathquerystring"
            headers = {'Content-Type': 'application/json'}
            response = requests.request("GET", url, headers=headers)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.text, "The URL is unsafe")
        except Exception as e:
            print('Exception occurred while checking url {}'.format(e))
            assert False


if __name__ == '__main__':
    unittest.main()