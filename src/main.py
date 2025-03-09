from textnode import TextNode, TextType


def main():
    newTextNode = TextNode(
        text="This is some test text",
        text_type=TextType.NORMAL_TEXT,
        url="https://www.google.com",
    )
    print(newTextNode)


main()
