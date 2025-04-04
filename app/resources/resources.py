def read_text_file_shortest(filepath):
    with open(filepath, 'r') as file:
        return file.read().splitlines()

CHARACTERS = read_text_file_shortest("app/resources/characters.txt")
