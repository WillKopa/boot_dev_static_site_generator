from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if self.tag == None:
            raise ValueError("ParentNode must have tag")
        
        if self.children == None:
            raise ValueError("ParentNode must have children")
        
        html = f"<{self.tag}"

        if self.props:
            for key in self.props.keys():
                html += f' {key}="{self.props[key]}"'
        
        html += ">"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"

        return html