from textnode import TextNode, TextType


def main():
    newTextNode = TextNode(
        text="This is some test text",
        text_type=TextType.TEXT,
        url="https://www.google.com",
    )
    print(newTextNode)


main()
