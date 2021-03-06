from __future__ import division

import unittest
import json
import numpy as np
import datetime
import pandas as pd

import great_expectations as ge

from .test_utils import assertDeepAlmostEqual

class TestPandasDataset(unittest.TestCase):

    def run_encapsulated_test(self, expectation_name, filename):
        with open(filename) as f:
            T = json.load(f)

        D = ge.dataset.PandasDataset(T["dataset"])
        D.set_default_expectation_argument("output_format", "COMPLETE")

        self.maxDiff = None

        for t in T["tests"]:

            if "title" in t:
                print(t["title"])
            else:
                print("WARNING: test set has no `title` field. In future versions of Great Expectations, this will be required.")

            expectation = getattr(D, expectation_name)
            out = expectation(**t['in'])
            out = json.loads(json.dumps(out))
            self.assertEqual(out, t['out'])

    def test_expect_column_values_to_be_of_type(self):

        D = ge.dataset.PandasDataset({
            'x' : [1,2,4],
            'y' : [1.0,2.2,5.3],
            'z' : ['hello', 'jello', 'mello'],
            'n' : [None, np.nan, None],
            'b' : [False, True, False],
            's' : ['hello', 'jello', 1],
            's1' : ['hello', 2.0, 1],
        })
        D.set_default_expectation_argument("result_format", "COMPLETE")

        T = [
                {
                    'in':{"column":"x","type_":"int","target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                {
                    'in':{"column":"x","type_":"string","target_datasource":"numpy"},
                    'out':{'success':False, 'unexpected_list':[1,2,4], 'unexpected_index_list':[0,1,2]}},
                {
                    'in':{"column":"y","type_":"float","target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                {
                    'in':{"column":"y","type_":"float","target_datasource":"numpy"},
                    'out':{'success':False, 'unexpected_list':[1.0,2.2,5.3], 'unexpected_index_list':[0,1,2]}},
                {
                    'in':{"column":"z","type_":"string","target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                {
                    'in':{"column":"b","type_":"boolean","target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}}
                #{
                #    'in':['n','null','python'],
                #    'kwargs':{},
                #    'out':{'success':False, 'unexpected_list':[np.nan]}},
                #{
                #    'in':['n','null','python'],
                #    'kwargs':{'mostly':.5},
                #    'out':{'success':True, 'unexpected_list':[np.nan]}}
        ]

        for t in T:
            out = D.expect_column_values_to_be_of_type(**t['in'])
            self.assertEqual(t['out']['success'], out['success'])
            self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
            self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

    def test_expect_column_values_to_be_in_type_list(self):

        D = ge.dataset.PandasDataset({
            'x' : [1,2,4],
            'y' : [1.0,2.2,5.3],
            'z' : ['hello', 'jello', 'mello'],
            'n' : [None, np.nan, None],
            'b' : [False, True, False],
            's' : ['hello', 'jello', 1],
            's1' : ['hello', 2.0, 1],
        })
        D.set_default_expectation_argument("result_format", "COMPLETE")

        T = [
                {
                    'in':{"column":"x","type_list":["int"],"target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                {
                    'in':{"column":"x","type_list":["string"],"target_datasource":"numpy"},
                    'out':{'success':False, 'unexpected_list':[1,2,4], 'unexpected_index_list':[0,1,2]}},
                {
                    'in':{"column":"y","type_list":["float"],"target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                {
                    'in':{"column":"y","type_list":["float"],"target_datasource":"numpy"},
                    'out':{'success':False, 'unexpected_list':[1.0,2.2,5.3], 'unexpected_index_list':[0,1,2]}},
                {
                    'in':{"column":"z","type_list":["string"],"target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                {
                    'in':{"column":"b","type_list":["boolean"],"target_datasource":"python"},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                {
                   'in':{"column":"s", "type_list":["string", "int"], "target_datasource":"python"},
                   'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list':[]}},
                #{
                #    'in':['n','null','python'],
                #    'kwargs':{'mostly':.5},
                #    'out':{'success':True, 'unexpected_list':[np.nan]}}
        ]

        for t in T:
            out = D.expect_column_values_to_be_in_type_list(**t['in'])
            self.assertEqual(t['out']['success'], out['success'])
            self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
            self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])





    # def test_expect_column_values_to_be_between(self):
    #     """

    #     """

    #     with open("./tests/test_sets/expect_column_values_to_be_between_test_set.json") as f:
    #         fixture = json.load(f)

    #     dataset = fixture["dataset"]
    #     tests = fixture["tests"]

    #     D = ge.dataset.PandasDataset(dataset)
    #     D.set_default_expectation_argument("result_format", "COMPLETE")

    #     self.maxDiff = None

    #     for t in tests:
    #         out = D.expect_column_values_to_be_between(**t['in'])

    #         # print '-'*80
    #         print(t)
    #         # print(json.dumps(out, indent=2))

    #         if 'out' in t:
    #             self.assertEqual(t['out']['success'], out['success'])
    #             if 'unexpected_index_list' in t['out']:
    #                 self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
    #             if 'unexpected_list' in t['out']:
    #                 self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

    #         if 'error' in t:
    #             self.assertEqual(out['exception_info']['raised_exception'], True)
    #             self.assertIn(t['error']['traceback_substring'], out['exception_info']['exception_traceback'])


    # def test_expect_column_values_to_match_regex_list(self):
    #     with open("./tests/test_sets/expect_column_values_to_match_regex_list_test_set.json") as f:
    #         J = json.load(f)
    #         D = ge.dataset.PandasDataset(J["dataset"])
    #         D.set_default_expectation_argument("result_format", "COMPLETE")
    #         T = J["tests"]

    #         self.maxDiff = None

    #     for t in T:
    #         out = D.expect_column_values_to_match_regex_list(**t['in'])
    #         self.assertEqual(t['out']['success'], out['success'])
    #         if 'unexpected_index_list' in t['out']:
    #             self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
    #         if 'unexpected_list' in t['out']:
    #             self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

    def test_expect_column_values_to_match_strftime_format(self):
        """
        """

        D = ge.dataset.PandasDataset({
            'x' : [1,2,4],
            'us_dates' : ['4/30/2017','4/30/2017','7/4/1776'],
            'us_dates_type_error' : ['4/30/2017','4/30/2017', 5],
            'almost_iso8601' : ['1977-05-25T00:00:00', '1980-05-21T13:47:59', '2017-06-12T23:57:59'],
            'almost_iso8601_val_error' : ['1977-05-55T00:00:00', '1980-05-21T13:47:59', '2017-06-12T23:57:59'],
            'already_datetime' : [datetime.datetime(2015,1,1), datetime.datetime(2016,1,1), datetime.datetime(2017,1,1)]
        })
        D.set_default_expectation_argument("result_format", "COMPLETE")

        T = [
                {
                    'in':{'column':'us_dates', 'strftime_format':'%m/%d/%Y'},
                    'out':{'success':True, 'unexpected_index_list':[], 'unexpected_list':[]}
                },
                {
                    'in':{'column':'us_dates_type_error','strftime_format':'%m/%d/%Y', 'mostly': 0.5, 'catch_exceptions': True},
                    # 'out':{'success':True, 'unexpected_index_list':[2], 'unexpected_list':[5]}},
                    'error':{
                        'traceback_substring' : 'TypeError'
                    },
                },
                {
                    'in':{'column':'us_dates_type_error','strftime_format':'%m/%d/%Y', 'catch_exceptions': True},
                    'error':{
                        'traceback_substring' : 'TypeError'
                    }
                },
                {
                    'in':{'column':'almost_iso8601','strftime_format':'%Y-%m-%dT%H:%M:%S'},
                    'out':{'success':True,'unexpected_index_list':[], 'unexpected_list':[]}},
                {
                    'in':{'column':'almost_iso8601_val_error','strftime_format':'%Y-%m-%dT%H:%M:%S'},
                    'out':{'success':False,'unexpected_index_list':[0], 'unexpected_list':['1977-05-55T00:00:00']}},
                {
                    'in':{'column':'already_datetime','strftime_format':'%Y-%m-%d', 'catch_exceptions':True},
                    # 'out':{'success':False,'unexpected_index_list':[0], 'unexpected_list':['1977-05-55T00:00:00']},
                    'error':{
                        'traceback_substring' : 'TypeError: Values passed to expect_column_values_to_match_strftime_format must be of type string.'
                    },
                }
        ]

        for t in T:
            out = D.expect_column_values_to_match_strftime_format(**t['in'])
            if 'out' in t:
                self.assertEqual(t['out']['success'], out['success'])
                if 'unexpected_index_list' in t['out']:
                    self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
                if 'unexpected_list' in t['out']:
                    self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])
            elif 'error' in t:
                self.assertEqual(out['exception_info']['raised_exception'], True)
                self.assertIn(t['error']['traceback_substring'], out['exception_info']['exception_traceback'])

    def test_expect_column_values_to_be_dateutil_parseable(self):

        D = ge.dataset.PandasDataset({
            'c1':['03/06/09','23 April 1973','January 9, 2016'],
            'c2':['9/8/2012','covfefe',25],
            'c3':['Jared','June 1, 2013','July 18, 1976'],
            'c4':['1', '2', '49000004632'],
            'already_datetime' : [datetime.datetime(2015,1,1), datetime.datetime(2016,1,1), datetime.datetime(2017,1,1)],
        })
        D.set_default_expectation_argument("result_format", "COMPLETE")

        T = [
                {
                    'in':{'column': 'c1'},
                    'out':{'success':True, 'unexpected_list':[], 'unexpected_index_list': []}},
                {
                    'in':{"column":'c2', "catch_exceptions":True},
                    # 'out':{'success':False, 'unexpected_list':['covfefe', 25], 'unexpected_index_list': [1, 2]}},
                    'error':{ 'traceback_substring' : 'TypeError: Values passed to expect_column_values_to_be_dateutil_parseable must be of type string' },
                },
                {
                    'in':{"column":'c3'},
                    'out':{'success':False, 'unexpected_list':['Jared'], 'unexpected_index_list': [0]}},
                {
                    'in':{'column': 'c3', 'mostly':.5},
                    'out':{'success':True, 'unexpected_list':['Jared'], 'unexpected_index_list': [0]}
                },
                {
                    'in':{'column': 'c4'},
                    'out':{'success':False, 'unexpected_list':['49000004632'], 'unexpected_index_list': [2]}
                },
                {
                    'in':{'column':'already_datetime', 'catch_exceptions':True},
                    'error':{ 'traceback_substring' : 'TypeError: Values passed to expect_column_values_to_be_dateutil_parseable must be of type string' },
                }
        ]

        for t in T:
            out = D.expect_column_values_to_be_dateutil_parseable(**t['in'])
            if 'out' in t:
                self.assertEqual(t['out']['success'], out['success'])
                self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
                self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])
            elif 'error' in t:
                self.assertEqual(out['exception_info']['raised_exception'], True)
                self.assertIn(t['error']['traceback_substring'], out['exception_info']['exception_traceback'])


    def test_expect_column_values_to_be_json_parseable(self):
        d1 = json.dumps({'i':[1,2,3],'j':35,'k':{'x':'five','y':5,'z':'101'}})
        d2 = json.dumps({'i':1,'j':2,'k':[3,4,5]})
        d3 = json.dumps({'i':'a', 'j':'b', 'k':'c'})
        d4 = json.dumps({'i':[4,5], 'j':[6,7], 'k':[8,9], 'l':{4:'x', 5:'y', 6:'z'}})
        D = ge.dataset.PandasDataset({
            'json_col':[d1,d2,d3,d4],
            'not_json':[4,5,6,7],
            'py_dict':[{'a':1, 'out':1},{'b':2, 'out':4},{'c':3, 'out':9},{'d':4, 'out':16}],
            'most':[d1,d2,d3,'d4']
        })
        D.set_default_expectation_argument("result_format", "COMPLETE")

        T = [
                {
                    'in':{'column':'json_col'},
                    'out':{'success':True, 'unexpected_index_list':[], 'unexpected_list':[]}},
                {
                    'in':{'column':'not_json'},
                    'out':{'success':False, 'unexpected_index_list':[0,1,2,3], 'unexpected_list':[4,5,6,7]}},
                {
                    'in':{'column':'py_dict'},
                    'out':{'success':False, 'unexpected_index_list':[0,1,2,3], 'unexpected_list':[{'a':1, 'out':1},{'b':2, 'out':4},{'c':3, 'out':9},{'d':4, 'out':16}]}},
                {
                    'in':{'column':'most'},
                    'out':{'success':False, 'unexpected_index_list':[3], 'unexpected_list':['d4']}},
                {
                    'in':{'column':'most', 'mostly':.75},
                    'out':{'success':True, 'unexpected_index_list':[3], 'unexpected_list':['d4']}}
        ]

        for t in T:
            out = D.expect_column_values_to_be_json_parseable(**t['in'])
            self.assertEqual(t['out']['success'], out['success'])
            self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
            self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

    # def test_expect_column_values_to_match_json_schema(self):

    #     with open("./tests/test_sets/expect_column_values_to_match_json_schema_test_set.json") as f:
    #         J = json.load(f)
    #         D = ge.dataset.PandasDataset(J["dataset"])
    #         D.set_default_expectation_argument("result_format", "COMPLETE")
    #         T = J["tests"]

    #         self.maxDiff = None

    #     for t in T:
    #         out = D.expect_column_values_to_match_json_schema(**t['in'])#, **t['kwargs'])
    #         self.assertEqual(t['out']['success'], out['success'])
    #         if 'unexpected_index_list' in t['out']:
    #             self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
    #         if 'unexpected_list' in t['out']:
    #             self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])


    def test_expectation_decorator_summary_mode(self):

        df = ge.dataset.PandasDataset({
            'x' : [1,2,3,4,5,6,7,7,None,None],
        })
        df.set_default_expectation_argument("result_format", "COMPLETE")

        # print '&'*80
        # print json.dumps(df.expect_column_values_to_be_between('x', min_value=1, max_value=5, result_format="SUMMARY"), indent=2)

        self.maxDiff = None
        self.assertEqual(
            df.expect_column_values_to_be_between('x', min_value=1, max_value=5, result_format="SUMMARY"),
            {
                "success" : False,
                "result" : {
                    "element_count" : 10,
                    "missing_count" : 2,
                    "missing_percent" : .2,
                    "unexpected_count" : 3,
                    "partial_unexpected_counts": [
                        {"value": 7.0,
                         "count": 2},
                        {"value": 6.0,
                         "count": 1}
                    ],
                    "unexpected_percent": 0.3,
                    "unexpected_percent_nonmissing": 0.375,
                    "partial_unexpected_list" : [6.0,7.0,7.0],
                    "partial_unexpected_index_list": [5,6,7],
                }
            }
        )

        self.assertEqual(
            df.expect_column_mean_to_be_between("x", 3, 7, result_format="SUMMARY"),
            {
                'success': True,
                'result': {
                    'observed_value': 4.375,
                    'element_count': 10,
                    'missing_count': 2,
                    'missing_percent': .2
                },
            }
        )

    def test_positional_arguments(self):

        df = ge.dataset.PandasDataset({
            'x':[1,3,5,7,9],
            'y':[2,4,6,8,10],
            'z':[None,'a','b','c','abc']
        })
        df.set_default_expectation_argument('result_format', 'COMPLETE')

        self.assertEqual(
            df.expect_column_mean_to_be_between('x',4,6),
            {'success':True, 'result': {'observed_value': 5, 'element_count': 5,
                'missing_count': 0,
                'missing_percent': 0.0}}
        )

        out = df.expect_column_values_to_be_between('y',1,6)
        t = {'out': {'success':False, 'unexpected_list':[8,10], 'unexpected_index_list': [3,4]}}
        if 'out' in t:
            self.assertEqual(t['out']['success'], out['success'])
            if 'unexpected_index_list' in t['out']:
                self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
            if 'unexpected_list' in t['out']:
                self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

        out = df.expect_column_values_to_be_between('y',1,6,mostly=.5)
        t = {'out': {'success':True, 'unexpected_list':[8,10], 'unexpected_index_list':[3,4]}}
        if 'out' in t:
            self.assertEqual(t['out']['success'], out['success'])
            if 'unexpected_index_list' in t['out']:
                self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
            if 'unexpected_list' in t['out']:
                self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

        out = df.expect_column_values_to_be_in_set('z',['a','b','c'])
        t = {'out': {'success':False, 'unexpected_list':['abc'], 'unexpected_index_list':[4]}}
        if 'out' in t:
            self.assertEqual(t['out']['success'], out['success'])
            if 'unexpected_index_list' in t['out']:
                self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
            if 'unexpected_list' in t['out']:
                self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

        out = df.expect_column_values_to_be_in_set('z',['a','b','c'],mostly=.5)
        t = {'out': {'success':True, 'unexpected_list':['abc'], 'unexpected_index_list':[4]}}
        if 'out' in t:
            self.assertEqual(t['out']['success'], out['success'])
            if 'unexpected_index_list' in t['out']:
                self.assertEqual(t['out']['unexpected_index_list'], out['result']['unexpected_index_list'])
            if 'unexpected_list' in t['out']:
                self.assertEqual(t['out']['unexpected_list'], out['result']['unexpected_list'])

    def test_result_format_argument_in_decorators(self):
        df = ge.dataset.PandasDataset({
            'x':[1,3,5,7,9],
            'y':[2,4,6,8,10],
            'z':[None,'a','b','c','abc']
        })
        df.set_default_expectation_argument('result_format', 'COMPLETE')

        #Test explicit Nones in result_format
        self.assertEqual(
            df.expect_column_mean_to_be_between('x',4,6, result_format=None),
            {'success':True, 'result': {'observed_value': 5, 'element_count': 5,
                'missing_count': 0,
                'missing_percent': 0.0
                }}
        )

        self.assertEqual(
            df.expect_column_values_to_be_between('y',1,6, result_format=None),
            {'result': {'element_count': 5,
                            'missing_count': 0,
                            'missing_percent': 0.0,
                            'partial_unexpected_counts': [{'count': 1, 'value': 8},
                                                          {'count': 1, 'value': 10}],
                            'partial_unexpected_index_list': [3, 4],
                            'partial_unexpected_list': [8, 10],
                            'unexpected_count': 2,
                            'unexpected_index_list': [3, 4],
                            'unexpected_list': [8, 10],
                            'unexpected_percent': 0.4,
                            'unexpected_percent_nonmissing': 0.4},
             'success': False}
        )

        #Test unknown output format
        with self.assertRaises(ValueError):
            df.expect_column_values_to_be_between('y',1,6, result_format="QUACK")

        with self.assertRaises(ValueError):
            df.expect_column_mean_to_be_between('x',4,6, result_format="QUACK")

    def test_from_pandas(self):
        pd_df = pd.DataFrame({
            'x':[1,3,5,7,9],
            'y':[2,4,6,8,10],
            'z':[None,'a','b','c','abc']
        })

        ge_df = ge.from_pandas(pd_df)
        self.assertIsInstance(ge_df, ge.dataset.Dataset)
        self.assertEquals(list(ge_df.columns), ['x', 'y', 'z'])
        self.assertEquals(list(ge_df['x']), list(pd_df['x']))
        self.assertEquals(list(ge_df['y']), list(pd_df['y']))
        self.assertEquals(list(ge_df['z']), list(pd_df['z']))


    def test_from_pandas_expectations_config(self):
        # Logic mostly copied from TestValidation.test_validate
        def load_ge_config(file):
            with open(file) as f:
                return json.load(f)

        my_expectations_config = load_ge_config("./tests/test_sets/titanic_expectations.json")

        pd_df = pd.read_csv("./tests/test_sets/Titanic.csv")
        my_df = ge.from_pandas(pd_df, expectations_config=my_expectations_config)

        my_df.set_default_expectation_argument("result_format", "COMPLETE")

        results = my_df.validate(catch_exceptions=False)

        expected_results = load_ge_config("./tests/test_sets/expected_results_20180303.json")

        self.maxDiff = None
        assertDeepAlmostEqual(self, results, expected_results)

    def test_ge_pandas_concatenating(self):
        df1 = ge.dataset.PandasDataset({
            'A': ['A0', 'A1', 'A2'],
            'B': ['B0', 'B1', 'B2']
        })

        df1.expect_column_values_to_match_regex('A', '^A[0-2]$')
        df1.expect_column_values_to_match_regex('B', '^B[0-2]$')

        df2 = ge.dataset.PandasDataset({
            'A': ['A3', 'A4', 'A5'],
            'B': ['B3', 'B4', 'B5']
        })

        df2.expect_column_values_to_match_regex('A', '^A[3-5]$')
        df2.expect_column_values_to_match_regex('B', '^B[3-5]$')

        df = pd.concat([df1, df2])

        exp_c = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}}
        ]

        # The concatenated data frame will:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Only have the default expectations

        self.assertIsInstance(df, ge.dataset.PandasDataset)
        self.assertEqual(df.find_expectations(), exp_c)

    def test_ge_pandas_joining(self):
        df1 = ge.dataset.PandasDataset({
            'A': ['A0', 'A1', 'A2'],
            'B': ['B0', 'B1', 'B2']},
            index=['K0', 'K1', 'K2'])

        df1.expect_column_values_to_match_regex('A', '^A[0-2]$')
        df1.expect_column_values_to_match_regex('B', '^B[0-2]$')

        df2 = ge.dataset.PandasDataset({
            'C': ['C0', 'C2', 'C3'],
            'D': ['C0', 'D2', 'D3']},
            index=['K0', 'K2', 'K3'])

        df2.expect_column_values_to_match_regex('C', '^C[0-2]$')
        df2.expect_column_values_to_match_regex('D', '^D[0-2]$')

        df = df1.join(df2)

        exp_j = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'C'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'D'}}
        ]

        # The joined data frame will:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Only have the default expectations

        self.assertIsInstance(df, ge.dataset.PandasDataset)
        self.assertEqual(df.find_expectations(), exp_j)

    def test_ge_pandas_merging(self):
        df1 = ge.dataset.PandasDataset({
            'id': [1, 2, 3, 4],
            'name': ['a', 'b', 'c', 'd']
        })

        df1.expect_column_values_to_match_regex('name', '^[A-Za-z ]+$')

        df2 = ge.dataset.PandasDataset({
            'id': [1, 2, 3, 4],
            'salary': [57000, 52000, 59000, 65000]
        })

        df2.expect_column_values_to_match_regex('salary', '^[0-9]{4,6]$')

        df = df1.merge(df2, on='id')

        exp_m = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'id'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'name'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'salary'}}
        ]

        # The merged data frame will:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Only have the default expectations

        self.assertIsInstance(df, ge.dataset.PandasDataset)
        self.assertEqual(df.find_expectations(), exp_m)

    def test_ge_pandas_sampling(self):
        df = ge.dataset.PandasDataset({
            'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8],
            'C': ['a', 'b', 'c', 'd'],
            'D': ['e', 'f', 'g', 'h']
        })

        # Put some simple expectations on the data frame
        df.expect_column_values_to_be_in_set("A", [1, 2, 3, 4])
        df.expect_column_values_to_be_in_set("B", [5, 6, 7, 8])
        df.expect_column_values_to_be_in_set("C", ['a', 'b', 'c', 'd'])
        df.expect_column_values_to_be_in_set("D", ['e', 'f', 'g', 'h'])

        exp1 = df.find_expectations()

        # The sampled data frame should:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Inherit ALL the non-failing expectations of the parent data frame

        samp1 = df.sample(n=2)
        self.assertIsInstance(samp1, ge.dataset.PandasDataset)
        self.assertEqual(samp1.find_expectations(), exp1)

        samp1 = df.sample(frac=0.25, replace=True)
        self.assertIsInstance(samp1, ge.dataset.PandasDataset)
        self.assertEqual(samp1.find_expectations(), exp1)

        # Change expectation on column "D", sample, and check expectations.
        # The failing expectation on column "D" is automatically dropped in
        # the sample.
        df.expect_column_values_to_be_in_set("D", ['e', 'f', 'g', 'x'])
        samp1 = df.sample(n=2)
        exp1 = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'C'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'D'}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'A', 'values_set': [1, 2, 3, 4]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'B', 'values_set': [5, 6, 7, 8]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'C', 'values_set': ['a', 'b', 'c', 'd']}}
        ]
        self.assertEqual(samp1.find_expectations(), exp1)


    def test_ge_pandas_concatenating(self):
        df1 = ge.dataset.PandasDataset({
            'A': ['A0', 'A1', 'A2'],
            'B': ['B0', 'B1', 'B2']
        })

        df1.expect_column_values_to_match_regex('A', '^A[0-2]$')
        df1.expect_column_values_to_match_regex('B', '^B[0-2]$')

        df2 = ge.dataset.PandasDataset({
            'A': ['A3', 'A4', 'A5'],
            'B': ['B3', 'B4', 'B5']
        })

        df2.expect_column_values_to_match_regex('A', '^A[3-5]$')
        df2.expect_column_values_to_match_regex('B', '^B[3-5]$')

        df = pd.concat([df1, df2])

        exp_c = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}}
        ]

        # The concatenated data frame will:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Only have the default expectations

        self.assertIsInstance(df, ge.dataset.PandasDataset)
        self.assertEqual(df.find_expectations(), exp_c)

    def test_ge_pandas_joining(self):
        df1 = ge.dataset.PandasDataset({
            'A': ['A0', 'A1', 'A2'],
            'B': ['B0', 'B1', 'B2']},
            index=['K0', 'K1', 'K2'])

        df1.expect_column_values_to_match_regex('A', '^A[0-2]$')
        df1.expect_column_values_to_match_regex('B', '^B[0-2]$')

        df2 = ge.dataset.PandasDataset({
            'C': ['C0', 'C2', 'C3'],
            'D': ['C0', 'D2', 'D3']},
            index=['K0', 'K2', 'K3'])

        df2.expect_column_values_to_match_regex('C', '^C[0-2]$')
        df2.expect_column_values_to_match_regex('D', '^D[0-2]$')

        df = df1.join(df2)

        exp_j = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'C'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'D'}}
        ]

        # The joined data frame will:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Only have the default expectations

        self.assertIsInstance(df, ge.dataset.PandasDataset)
        self.assertEqual(df.find_expectations(), exp_j)

    def test_ge_pandas_merging(self):
        df1 = ge.dataset.PandasDataset({
            'id': [1, 2, 3, 4],
            'name': ['a', 'b', 'c', 'd']
        })

        df1.expect_column_values_to_match_regex('name', '^[A-Za-z ]+$')

        df2 = ge.dataset.PandasDataset({
            'id': [1, 2, 3, 4],
            'salary': [57000, 52000, 59000, 65000]
        })

        df2.expect_column_values_to_match_regex('salary', '^[0-9]{4,6]$')

        df = df1.merge(df2, on='id')

        exp_m = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'id'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'name'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'salary'}}
        ]

        # The merged data frame will:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Only have the default expectations

        self.assertIsInstance(df, ge.dataset.PandasDataset)
        self.assertEqual(df.find_expectations(), exp_m)

    def test_ge_pandas_sampling(self):
        df = ge.dataset.PandasDataset({
            'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8],
            'C': ['a', 'b', 'c', 'd'],
            'D': ['e', 'f', 'g', 'h']
        })

        # Put some simple expectations on the data frame
        df.expect_column_values_to_be_in_set("A", [1, 2, 3, 4])
        df.expect_column_values_to_be_in_set("B", [5, 6, 7, 8])
        df.expect_column_values_to_be_in_set("C", ['a', 'b', 'c', 'd'])
        df.expect_column_values_to_be_in_set("D", ['e', 'f', 'g', 'h'])

        exp1 = df.find_expectations()

        # The sampled data frame should:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Inherit ALL the expectations of the parent data frame

        samp1 = df.sample(n=2)
        self.assertIsInstance(samp1, ge.dataset.PandasDataset)
        self.assertEqual(samp1.find_expectations(), exp1)

        samp1 = df.sample(frac=0.25, replace=True)
        self.assertIsInstance(samp1, ge.dataset.PandasDataset)
        self.assertEqual(samp1.find_expectations(), exp1)

        # Change expectation on column "D", sample, and check expectations.
        # The failing expectation on column "D" is NOT automatically dropped
        # in the sample.
        df.expect_column_values_to_be_in_set("D", ['e', 'f', 'g', 'x'])
        samp1 = df.sample(n=2)
        exp1 = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'C'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'D'}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'A', 'values_set': [1, 2, 3, 4]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'B', 'values_set': [5, 6, 7, 8]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'C', 'values_set': ['a', 'b', 'c', 'd']}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'D', 'values_set': ['e', 'f', 'g', 'x']}}
        ]
        self.assertEqual(samp1.find_expectations(), exp1)


    def test_ge_pandas_subsetting(self):
        df = ge.dataset.PandasDataset({
            'A':[1,2,3,4],
            'B':[5,6,7,8],
            'C':['a','b','c','d'],
            'D':['e','f','g','h']
        })

        # Put some simple expectations on the data frame
        df.expect_column_values_to_be_in_set("A", [1, 2, 3, 4])
        df.expect_column_values_to_be_in_set("B", [5, 6, 7, 8])
        df.expect_column_values_to_be_in_set("C", ['a', 'b', 'c', 'd'])
        df.expect_column_values_to_be_in_set("D", ['e', 'f', 'g', 'h'])

        # The subsetted data frame should:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Inherit ALL the expectations of the parent data frame

        exp1 = df.find_expectations()

        sub1 = df[['A', 'D']]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[['A']]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[:3]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[1:2]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[:-1]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[-1:]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df.iloc[:3, 1:4]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df.loc[0:, 'A':'B']
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

    def test_ge_pandas_automatic_failure_removal(self):
        df = ge.dataset.PandasDataset({
            'A': [1, 2, 3, 4],
            'B': [5, 6, 7, 8],
            'C': ['a', 'b', 'c', 'd'],
            'D': ['e', 'f', 'g', 'h']
        })

        # Put some simple expectations on the data frame
        df.expect_column_values_to_be_in_set("A", [1, 2, 3, 4])
        df.expect_column_values_to_be_in_set("B", [5, 6, 7, 8])
        df.expect_column_values_to_be_in_set("C", ['w', 'x', 'y', 'z'])
        df.expect_column_values_to_be_in_set("D", ['e', 'f', 'g', 'h'])

        # First check that failing expectations are NOT automatically
        # dropped when sampling.
        # For this data frame, the expectation on column "C" above fails.
        exp1 = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'C'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'D'}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'A', 'values_set': [1, 2, 3, 4]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'B', 'values_set': [5, 6, 7, 8]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'C', 'values_set': ['w', 'x', 'y', 'z']}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'D', 'values_set': ['e', 'f', 'g', 'h']}}
        ]
        samp1 = df.sample(n=2)
        self.assertEqual(samp1.find_expectations(), exp1)

        # Now check subsetting to verify that failing expectations are NOT
        # automatically dropped when subsetting.
        sub1 = df[['A', 'D']]
        self.assertEqual(sub1.find_expectations(), exp1)

        # Set property/attribute so that failing expectations are
        # automatically removed when sampling or subsetting.
        df.discard_subset_failing_expectations = True

        exp_samp = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'B'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'C'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'D'}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'A', 'values_set': [1, 2, 3, 4]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'B', 'values_set': [5, 6, 7, 8]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'D', 'values_set': ['e', 'f', 'g', 'h']}}
        ]

        samp2 = df.sample(n=2)
        self.assertEqual(samp2.find_expectations(), exp_samp)

        # Now check subsetting. In additional to the failure on column "C",
        # the expectations on column "B" now fail since column "B" doesn't
        # exist in the subset.
        sub2 = df[['A', 'D']]
        exp_sub = [
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'A'}},
            {'expectation_type': 'expect_column_to_exist',
             'kwargs': {'column': 'D'}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'A', 'values_set': [1, 2, 3, 4]}},
            {'expectation_type': 'expect_column_values_to_be_in_set',
             'kwargs': {'column': 'D', 'values_set': ['e', 'f', 'g', 'h']}}
        ]
        self.assertEqual(sub2.find_expectations(), exp_sub)


    def test_ge_pandas_subsetting(self):
        df = ge.dataset.PandasDataset({
            'A':[1,2,3,4],
            'B':[5,6,7,8],
            'C':['a','b','c','d'],
            'D':['e','f','g','h']
        })

        # Put some simple expectations on the data frame
        df.expect_column_values_to_be_in_set("A", [1, 2, 3, 4])
        df.expect_column_values_to_be_in_set("B", [5, 6, 7, 8])
        df.expect_column_values_to_be_in_set("C", ['a', 'b', 'c', 'd'])
        df.expect_column_values_to_be_in_set("D", ['e', 'f', 'g', 'h'])

        # The subsetted data frame should:
        #
        #   1. Be a ge.dataset.PandaDataSet
        #   2. Inherit ALL the expectations of the parent data frame
        #
        exp1 = df.find_expectations()

        sub1 = df[['A', 'D']]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[['A']]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[:3]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[1:2]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[:-1]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df[-1:]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df.iloc[:3, 1:4]
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

        sub1 = df.loc[0:, 'A':'B']
        self.assertIsInstance(sub1, ge.dataset.PandasDataset)
        self.assertEqual(sub1.find_expectations(), exp1)

if __name__ == "__main__":
    unittest.main()
