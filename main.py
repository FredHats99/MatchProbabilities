# Esempio di utilizzo
import Squad_n_Matches
import File_manager


# Scrivi una linea nel file
# file_manager.write_line("ATALANTA, [2,0,1]")

# Leggi una linea specifica dal file
# linea_letta = file_manager.read_line(0)  # Legge la prima linea


def match_analysis(team_1, team_2):
    file_manager = File_manager.FileManager("Stats.txt")

    home_index = file_manager.check_name(team_1)
    visitor_index = file_manager.check_name(team_2)
    home_stats = File_manager.parse_scores_lists(file_manager.read_line(home_index))
    visitor_stats = File_manager.parse_scores_lists(file_manager.read_line(visitor_index))

    home_team = Squad_n_Matches.Squad(team_1, home_stats[0], home_stats[1])
    visitor_team = Squad_n_Matches.Squad(team_2, visitor_stats[0], visitor_stats[1])
    return Squad_n_Matches.Match(home_team, visitor_team)


a = match_analysis("MILAN", "INTER")


