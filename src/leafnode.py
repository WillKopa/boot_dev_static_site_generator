from src.htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("LeadNode must have value")
        
        if self.tag == None:
            return self.value
        
        html = f"<{self.tag}"
        
        if self.props:
            for key in self.props.keys():
                html += f' {key}="{self.props[key]}"'

        html += f">{self.value}</{self.tag}>"
        
        return html