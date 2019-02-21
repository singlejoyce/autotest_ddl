# _*_ coding: utf-8 _*_

__author__ = "joyce"

import configparser


class ConfigReader(object):
    def __init__(self, path):
        self.CReader = configparser.ConfigParser()
        self.CReader.read(path, encoding='utf8')

    def getSection(self):
        return self.CReader.sections()

    def getdic(self, section):
        s = {}
        for k, v in self.CReader.items(section):
            s[k] = v
        return s

