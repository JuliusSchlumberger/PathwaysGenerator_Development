import base64


def image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return 'data:image/png;base64,' + encoded_string

# Define a function to add line breaks to long titles
def add_line_breaks(title, max_length=15):
    lines = []
    while len(title) > max_length:
        break_pos = max_length
        while break_pos < len(title) and title[break_pos] not in [' ', '_']:
            break_pos += 1
        if break_pos == len(title):
            break_pos = len(title)
        lines.append(title[:break_pos])
        title = title[break_pos:].lstrip(' _')
    lines.append(title)
    return '<br>'.join(lines).rstrip('<br>')

