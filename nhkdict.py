import xml.etree.ElementTree as ET
from copy import copy
from dataclasses import dataclass


@dataclass
class NHKResult:
    title: str
    summary: str
    head: str
    body: str

    @classmethod
    def from_xml_element(cls, element):
        title = element.find("title").text
        summary = element.find("summary").text
        head_element = copy(element.find("head"))
        head_element.tag = "div"
        head = "".join([ET.tostring(e, encoding="unicode") for e in list(head_element)])
        body_element = copy(element.find("body"))
        body_element.tag = "div"
        body = "".join([ET.tostring(e, encoding="unicode") for e in list(body_element)])
        return cls(title, summary, head, body)


class NHKDict:
    def __init__(self, xml_path):
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()

    def find_items(self, query):
        for item in self.root.iter("dic-item"):
            if item.get("type"):
                # filters 凡例 and 外字一覧 items
                continue
            keys = item.find("keys")
            for key in keys.iter("key"):
                if key.text == query:
                    yield item

    def lookup(self, query):
        results = []
        for item in self.find_items(query):
            results.append(NHKResult.from_xml_element(item))
        return results
