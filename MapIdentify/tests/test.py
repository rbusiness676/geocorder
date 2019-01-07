from unittest import TestCase

from django.test import Client

class MYTest(TestCase):

    def test1(self):

        params = {}
        params['google_key']= input("Enter google api key")
        params['file_in'] = input("Enter input file path")
        params['file_out'] =  input("Enter output file path")

        client = Client()
        response = client.get('/find/',data=params)
        self.assertEqual(response.status_code, 200)

    def test2(self):
        params = {}
        params['google_key'] = input("Enter google api key")
        params['file_in'] = input("Enter input file path")
        params['file_out'] = input("Enter output file path")

        client = Client()
        response = client.get('/location/', data=params)
        self.assertEqual(response.status_code, 200)
