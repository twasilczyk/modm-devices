# -*- coding: utf-8 -*-
# Copyright (c) 2013-2016, Niklas Hauser
# Copyright (c)      2016, Fabian Greif
# All rights reserved.

import os
import re
import logging

from lxml import etree

LOGGER = logging.getLogger('dfg.input.xml')

class XMLReader:
    """ DeviceReader
    Base class for all readers for handling the opening and reading of XML files etc...
    """
    _PARSER = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

    def __init__(self, path):
        self.filename = path
        self.tree = self._openDeviceXML(self.filename)

    def _openDeviceXML(self, filename):
        LOGGER.debug("Opening XML file '%s'", os.path.basename(self.filename))
        with open(filename, 'r') as raw_file:
            xml_file = raw_file.read()
        xml_file = re.sub(' xmlns="[^"]+"', '', xml_file, count=1).encode('utf-8')
        xmltree = None
        try:
            xmltree = etree.fromstring(xml_file, parser=XMLReader._PARSER)
        except:
            LOGGER.error("Failure to open XML file!")
        return xmltree

    def queryTree(self, query):
        """
        This tries to apply the query to the device tree and returns either
        - an array of element nodes,
        - an array of strings or
        - None, if the query failed.
        """
        response = None
        try:
            response = self.tree.xpath(query)
        except:
            LOGGER.error("Query failed for '%s'", str(query))

        return response

    def query(self, query):
        """
        This wraps the queryTree and returns an (empty) array.
        """
        # LOGGER.debug("Query for '%s'", str(query))
        result = self.queryTree(query)

        if result != None:
            # if len(result) == 0:
            #     LOGGER.warning("No results found for '%s'", str(query))
            result = list(set(result))
            return result

        return []

    def compactQuery(self, query):
        # LOGGER.debug("Compact query for '%s'", str(query))
        result = self.queryTree(query)
        # LOGGER.debug("Compact query result: '%s'", str(result))
        if result != None:
            # if len(result) == 0:
            #     LOGGER.debug("No results found for '%s'", str(query))
            result = list(set(result))
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "XMLReader({}, [\n{}])".format(os.path.basename(self.filename), ",\n".join(map(str, self.properties)))
