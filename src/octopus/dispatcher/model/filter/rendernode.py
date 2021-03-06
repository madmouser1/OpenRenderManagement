#!/usr/bin/python
# -*- coding: latin-1 -*-

"""
"""

import logging
import re

__all__ = []


class FilterError(Exception):
    pass


class IFilterRenderNode:
    """
    Class helping to filter on node objects.
    Supported filters are:
    - id
    - name
    """
    def __init__(self):
        self.currFilter = None

    def matchKeyValue(self):
        raise NotImplementedError

    def matchDatetime(self):
        raise NotImplementedError

    def matchFloat(self):
        raise NotImplementedError

    def matchString(self):
        raise NotImplementedError

    def matchHost(self, elem):
        regex = '|'.join(self.currFilter)
        return re.match(regex, elem.host)

    def matchId(self, elem):
        return True if elem.id in self.currFilter else False

    def matchName(self, elem):
        regex = '|'.join(self.currFilter)
        return re.match(regex, elem.name)

    def matchPool(self, elem):
        for pool in elem.pools:
            if pool.name in self.currFilter:
                return True
        return False

    def matchStatus(self, elem):
        return True if elem.status in self.currFilter else False

    def matchVersion(self, elem):
        return True if elem.puliversion in self.currFilter else False

    def match(self, filters, nodes):

        if 'id' in filters and filters.get('id') is not []:
            self.currFilter = [int(id) for id in filters['id']]
            nodes = filter(self.matchId, nodes)
            logging.getLogger('main.filter').info("-- Filtering on id %s, nb remaining nodes: %d", self.currFilter, len(nodes))

        if 'name' in filters and filters.get('name') is not []:
            self.currFilter = filters['name']
            nodes = filter(self.matchName, nodes)
            logging.getLogger('main.filter').info("-- Filtering on names %s, nb remaining nodes: %d", self.currFilter, len(nodes))

        if 'status' in filters and filters.get('status') is not []:
            self.currFilter = filters['status']
            nodes = filter(self.matchStatus, nodes)
            logging.getLogger('main.filter').info("-- Filtering on status %s, nb remaining nodes: %d", self.currFilter, len(nodes))

        if 'host' in filters and filters.get('host') is not []:
            self.currFilter = filters['host']
            nodes = filter(self.matchHost, nodes)
            logging.getLogger('main.filter').info("-- Filtering on host name  %s, nb remaining nodes: %d", self.currFilter, len(nodes))

        if 'version' in filters and filters.get('version') is not []:
            self.currFilter = filters['version']
            nodes = filter(self.matchVersion, nodes)
            logging.getLogger('main.filter').info("-- Filtering on version %s, nb remaining nodes: %d", self.currFilter, len(nodes))

        if 'pool' in filters and filters.get('pool') is not []:
            self.currFilter = filters['pool']
            nodes = filter(self.matchPool, nodes)
            logging.getLogger('main.filter').info("-- Filtering on pools %s, nb remaining nodes: %d", self.currFilter, len(nodes))

        return nodes
