from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if self.value == None:
            raise ValueError("LeafNode must have value set")
        
        if self.tag == None:
            return self.value
        
        html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        return html