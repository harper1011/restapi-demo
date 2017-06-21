#!/usr/bin/env python
import logging
import pprint
import subprocess
import unittest

import requests
import sys

APP_NAME = 'test_rest_server'
FORMAT = '%(asctime)s %(module)s:%(lineno)-3s[%(levelname)s] %(message)s'

logging.basicConfig(filename='testing.log', format=FORMAT, level=logging.WARN)
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.DEBUG)


EXPECTED_FAIL_REASON = 'Invalid Position data'
REST_SERVER_PORT = 3000
V2_URL = 'http://%s:%s/api/v2/'
ROOT_URL = 'http://%s:%s/'
NON_EXIST_URL = 'http://%s:%s/something/notexist/'
LOCAL_REST_URL = 'http://%s:%s/api/v1/'
TEST_REST_URL = 'http://%s:%s/tst/v1/'
RESET_DATA_AUTH_STRING = 'UnitTest_only'


class SimpleRestServerTestCase(unittest.TestCase):
    def setUp(self):
        try:
            r = requests.delete(TEST_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT) + RESET_DATA_AUTH_STRING)
            logger.debug('Return Code for resetting server existing data: %s.', r.status_code)
        except:
            logger.exception('Failed to reset all existing data')

        r = requests.get(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT))
        logger.debug('Return Code for querying server initialized data: %s, data: %s', r.status_code, r.json())
        if r.status_code == 404 or r.status_code == 400:
            try:
                subprocess.check_call('/opt/script/restapi/simple_rest_server.py 127.0.0.1 3000', shell=True)
            except Exception as e:
                logger.exception('Exception occurred during start simple REST server: %s', e.message)

        self.idx1 = None
        self.idx2 = None
        self.idx3 = None
        self.idx4 = None
        self.item1 = dict()
        self.item2 = dict()
        self.item3 = dict()
        self.item4 = dict()

    def tearDown(self):
        pass

    def test_single_combined_case(self):
        self.get_all_items()
        self.push_one_item_succ()
        self.get_one_item_succ('1')
        self.update_one_item_succ('1')
        self.delete_one_item_succ('1')
        self.get_one_item_fail('1')
        self.push_multiple_items_succ()
        self.get_all_items()
        self.push_items_fail()
        self.delete_one_item_fail('4')
        self.update_one_item_fail('4')
        self.query_unsupported_url()

    def get_all_items(self):
        r = requests.get(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT))
        all_data_keys = [self.idx1, self.idx2, self.idx3]
        if not any(all_data_keys):
            all_data_keys = []
        all_data_values = [self.item1, self.item2, self.item3]
        all_data = dict(zip(all_data_keys, all_data_values))
        logger.debug('get_all_items\n%s', pprint.pformat(all_data))
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), all_data)
        self.assertEqual(len(r.json()), len(all_data_keys))

    def push_one_item_succ(self):
        self.item1 = dict.fromkeys(['position', 'description'])
        self.item1['position'] = [40.7410861, -73.9896297241625]
        self.item1['description'] = 'something u wont know'
        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item1)
        self.assertEqual(r.headers['location'].split('/')[-1], '1')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json(), self.item1)

    def push_items_fail(self):
        self.item4 = dict.fromkeys(['position', 'description'])
        self.item4['position'] = [100.7410861, -73.9896297241625]
        self.item4['description'] = 'something will fail'
        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item4)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), self.item4)
        self.assertEqual(r.__getstate__()['reason'], EXPECTED_FAIL_REASON)

        self.item4['position'] = [80.7410861, -190.9896297241625]
        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item4)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), self.item4)
        self.assertEqual(r.__getstate__()['reason'], EXPECTED_FAIL_REASON)

        self.item4['position'] = [80.7410861, 200.9896297241625]
        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item4)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), self.item4)
        self.assertEqual(r.__getstate__()['reason'], EXPECTED_FAIL_REASON)

        self.item4['position'] = [-100.7410861, 80.9896297241625]
        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item4)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), self.item4)
        self.assertEqual(r.__getstate__()['reason'], EXPECTED_FAIL_REASON)

        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), data=self.item4)
        self.assertEqual(r.status_code, 415)

    def get_one_item_succ(self, idx):
        r = requests.get(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT) + idx)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), self.item1)

    def delete_one_item_succ(self, idx):
        r = requests.delete(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT) + idx)
        self.assertEqual(r.status_code, 204)

    def delete_one_item_fail(self, idx):
        r = requests.delete(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT) + idx)
        self.assertEqual(r.status_code, 404)

    def get_one_item_fail(self, idx):
        r = requests.get(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT) + idx)
        self.assertEqual(r.status_code, 404)

    def update_one_item_succ(self, idx):
        self.item1['position'] = [22, -33]
        self.item1['description'] = 'This is changed by Update'
        r = requests.put(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT) + idx, json=self.item1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), self.item1)

    def push_multiple_items_succ(self):
        self.item2 = dict.fromkeys(['position', 'description'])
        self.item2['position'] = [50.7410861, -83.9896297241625]
        self.item2['description'] = 'something u know'
        self.item3 = dict.fromkeys(['position', 'description'])
        self.item3['position'] = [60.7410861, -93.9896297241625]
        self.item3['description'] = 'something u knew'

        r1 = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item1)
        r2 = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item2)
        r3 = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item3)
        r4 = requests.get(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT))

        self.idx1 = r1.headers['location'].split('/')[-1]
        self.idx2 = r2.headers['location'].split('/')[-1]
        self.idx3 = r3.headers['location'].split('/')[-1]
        all_data_keys = [self.idx1, self.idx2, self.idx3]
        all_data_values = [self.item1, self.item2, self.item3]
        all_data = dict(zip(all_data_keys, all_data_values))
        logger.debug('get_all_items\n%s', pprint.pformat(all_data))

        self.assertEqual(r1.status_code, 201)
        self.assertEqual(r1.json(), self.item1)
        self.assertEqual(r2.status_code, 201)
        self.assertEqual(r2.json(), self.item2)
        self.assertEqual(r3.status_code, 201)
        self.assertEqual(r3.json(), self.item3)
        self.assertEqual(r4.status_code, 200)
        self.assertDictEqual(r4.json(), all_data)

    def update_one_item_fail(self, idx):
        self.item4['position'] = [80.7410861, 70.9896297241625]
        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT) + idx, json=self.item4)
        self.assertEqual(r.status_code, 404)

        self.item4['position'] = [80.7410861, -190.9896297241625]
        r = requests.post(LOCAL_REST_URL % (REST_SERVER_IP, REST_SERVER_PORT), json=self.item4)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), self.item4)
        self.assertEqual(r.__getstate__()['reason'], EXPECTED_FAIL_REASON)

    def query_unsupported_url(self):
        r = requests.get(V2_URL  % (REST_SERVER_IP, REST_SERVER_PORT))
        self.assertEqual(r.status_code, 404)

        r = requests.delete(ROOT_URL % (REST_SERVER_IP, REST_SERVER_PORT))
        self.assertEqual(r.status_code, 404)

        r = requests.post(NON_EXIST_URL % (REST_SERVER_IP, REST_SERVER_PORT))
        self.assertEqual(r.status_code, 404)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        REST_SERVER_IP = sys.argv.pop()
    else:
        REST_SERVER_IP = '127.0.0.1'

    unittest.main()
