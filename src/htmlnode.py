class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""

        html_props = ""
        for key in self.props.keys():
            html_props += f' {key}="{self.props[key]}"'
        return html_props
    
    def __repr__(self):
        return f"HTMLNode\n{'=' * 20}\nTag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}\n{'=' * 20}"