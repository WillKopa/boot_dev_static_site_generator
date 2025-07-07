class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop_string_list = []
        for key in self.props.keys():
            prop_string_list.append(f'{key}="{self.props[key]}"')
        return " ".join(prop_string_list)
    
    def __repr__(self):
        return f"HTMLNode\n{'=' * 20}\nTag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}\n{'=' * 20}"