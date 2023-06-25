import markdown


def to_html(text: str, images: dict[str, str] = {}):

    html = markdown.markdown(text)
    # for i in
    # html.find("[")

    return html


if __name__ == "__main__":
    with open("../last_data.htnl", "w") as file:
        text = file.read()
    images = generate_images(5, "data/video/video")
    to_html(text, )
