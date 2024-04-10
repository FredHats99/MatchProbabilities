import re


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def write_line(self, line):
        try:
            with open(self.filename, 'a') as file:
                file.write(line + '\n')
            print(f"Line '{line}' scritta su '{self.filename}' con successo.")
        except IOError as e:
            print(f"Errore durante la scrittura su '{self.filename}': {e}")

    def read_line(self, line_number):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                if 0 <= line_number < len(lines):
                    return lines[line_number].strip()
                else:
                    return None  # Linea non presente nel file
        except IOError as e:
            print(f"Errore durante la lettura da '{self.filename}': {e}")
            return None

    def check_name(self, team_name):
        index = 0
        team_not_found = True
        while team_not_found:
            line = self.read_line(index)
            if parse_team_name(line) == team_name:
                return index
            if index > 20:
                return None
            index += 1


def parse_team_name(input_string):
    # Definisci il pattern regex per estrarre il nome della squadra
    pattern = r"^([a-zA-Z\s]+)\s*,\s*\[([0-9,\s]+)\](?:\s*,\s*\[([0-9,\s]+)\])*$"

    # Cerca il match con il pattern regex nella stringa di input
    match = re.match(pattern, input_string)

    if match:
        team_name = match.group(1).strip()  # Estrai il nome della squadra
        return team_name
    else:
        return None


def parse_scores_lists(input_string):
    # Definisci il pattern regex per estrarre le liste di numeri
    pattern = r"\[([0-9,\s]+)\]"

    # Trova tutte le corrispondenze con il pattern regex nella stringa di input
    scores_lists = re.findall(pattern, input_string)

    # Estrai ciascuna lista di numeri come lista di interi
    parsed_lists = []
    for scores_str in scores_lists:
        scores = [int(num) for num in re.findall(r'\d+', scores_str)]
        parsed_lists.append(scores)

    return parsed_lists

