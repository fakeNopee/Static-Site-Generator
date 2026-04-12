class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise
    def props_to_html(self):
        string = ""
        if self.props is None:
            string = " "
            return string
        for thing in self.props:
            string = f'{string} {thing}="{self.props[thing]}"'
        return string
    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props_to_html()})"



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        
        if self.props is None:
            return f'<{self.tag}>{self.value}</{self.tag}>'

        if self.tag == "img":
            return f'<{self.tag}{self.props_to_html()}>'

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'



    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Props: {self.props_to_html()})"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag")
        
        if len(self.children) < 1:
            raise ValueError("no children")

        else:
            inside = ""
            for child in self.children:
                inside = inside + child.to_html()
            if self.props:
                return f'<{self.tag}{self.props_to_html()}>{inside}</{self.tag}>' 

            return f'<{self.tag}>{inside}</{self.tag}>'
        
