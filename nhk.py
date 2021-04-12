import xml.etree.ElementTree as ET


class NHK:
    def __init__(self, xml_path):
        self.tree = ET.parse(xml_path)
        self.root = self.tree.getroot()

    def find_items(self, query):
        for item in self.root.iter('dic-item'):
            if item.get('type'):
                # filters 凡例 and 外字一覧 items
                continue
            keys = item.find('keys')
            for key in keys.iter('key'):
                if key.text == query:
                    yield item


def lookup(query):
    return f"result for {query}"
