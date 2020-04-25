#!/usr/bin/env python3
# coding: utf8

import json
import re

import requests


class NIH(object):
    """
    NIH's APIs wrapper
    """

    def __init__(self):
        pass

    def pmid_to_pmcid(self, pmid):
        """
        PMID to PMCID conversion
        """
        api_request = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=MELoDiST&email=bertha@omictools.com&format=json&ids={}'.format(
            re.sub(' ', '', str(pmid)))
        json_data = json.loads(requests.get(api_request).text)
        if len(json_data['records']) == 1:  # Check just in case ..
            try:
                return json_data['records'][0]['pmcid']
            except KeyError:
                return None

    def pmcid_to_pmid(self, pmcid):
        api_request = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=MELoDiST&email=bertha@omictools.com&format=json&ids=PMC{}'.format(
            pmcid)
        json_data = json.loads(requests.get(api_request).text)
        if len(json_data['records']) == 1:  # Check just in case ..
            try:
                return json_data['records'][0]['pmid']
            except KeyError:
                return None

    def doi_to_pmid(self, doi):
        api_request = 'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=MELoDiST&email=bertha@omictools.com&format=json&ids={}'.format(
            doi)
        json_data = json.loads(requests.get(api_request).text)
        try:
            if len(json_data['records']) == 1:  # Check just in case ..
                return json_data['records'][0]['pmid']
        except KeyError:
            return None
