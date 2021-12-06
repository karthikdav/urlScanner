import unittest
import dblayer


class MyTestCase(unittest.TestCase):
    def test_a_truncate_db(self):
        print("Currently Executing {}".format(self._testMethodName))
        print("To clear all the records before test cases start")
        try:
            response = dblayer.truncate_table()
            if response == 1:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

    def test_b_insert_record(self):
        print("Currently Executing {}".format(self._testMethodName))
        print("Inserting first record")
        try:
            request_url = 'http://test.com/safe'
            response = dblayer.insert_record(request_url)
            if response == 1:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

    def test_c_update_record(self):
        print("Currently Executing {}".format(self._testMethodName))
        print("Updating the first record")
        try:
            request_url = 'http://test.com/notsafe'
            response = dblayer.update_record(1, request_url, True)
            if response == 1:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

    def test_d_insert_second_record(self):
        print("Currently Executing {}".format(self._testMethodName))
        print("Inserting second record")
        try:
            request_url = 'http://10.10.10.10:9200/isclean'
            response = dblayer.insert_record(request_url)
            if response == 1:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

    def test_e_read_first_record(self):
        print("Currently Executing {}".format(self._testMethodName))
        print("Reading one record")
        try:
            response = dblayer.get_record_by_id(1)
            if len(response) > 2:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

    def test_f_read_all_record(self):
        print("Currently Executing {}".format(self._testMethodName))
        print("Reading all record")
        try:
            response = dblayer.get_all_records()
            if len(response) > 2:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

    def test_g_delete_record(self):
        print("Currently Executing ".format(self._testMethodName))
        print("Deleting a record")
        try:
            response = dblayer.update_record(2, '', False)
            if response == 1:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

    def test_h_truncate_row(self):
        print("Currently Executing Cleanup")
        print("Cleaning the DB after test cases are finished")
        try:
            response = dblayer.truncate_table()
            if response == 1:
                assert True
            else:
                assert False
        except Exception as e:
            print(e)
            assert False

if __name__ == '__main__':
    unittest.main()
