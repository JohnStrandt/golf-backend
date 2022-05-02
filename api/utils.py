import math

def sort_by_hdcp(tup):
    return sorted(tup, key=lambda x: x[1])


def sort_by_hole(tup):
    return sorted(tup, key=lambda x: x[0])


def calcMatchHDCP(holes, team1_card, team2_card):
    hdcps = []
    for hole in holes:
        hdcps.append((hole.number, hole.handicap))

    num_holes = len(hdcps)
    strokes_given = abs(team1_card.handicap - team2_card.handicap)

    all_holes = math.floor(strokes_given / num_holes)
    some_holes = strokes_given % num_holes

    #  sort holes by handicap so we can easily manage handicaps
    sorted_hdcps = sort_by_hdcp(hdcps)

    # make list of tuples with hole & strokes given
    hdcp_tuples = []
    if some_holes:
        for i in range(num_holes):
            if i < some_holes:
                hdcp_tuples.append((sorted_hdcps[i][0], all_holes + 1))
            else:
                hdcp_tuples.append((sorted_hdcps[i][0], all_holes))
    else:
        # evenly matched - no handicap given
        for i in range(num_holes):
            hdcp_tuples.append((sorted_hdcps[i][0], 0))

    #  sort handicap info by hole number, so it is usable by app
    sorted_hdcp = sort_by_hole(hdcp_tuples)
    hdcp_dict = dict(sorted_hdcp)
    
    if team1_card.handicap > team2_card.handicap:
        team = team1_card.team
        card_id = team1_card.id
    else:
        team = team2_card.team
        card_id = team2_card.id

    # case where teams are equally matched - no strokes given
    match_hdcp = {"team": None, "total_strokes": 0, "hdcp_strokes": hdcp_dict}

    # team is the one given strokes
    if strokes_given:
        match_hdcp = {
            "card_id": str(card_id),
            "team": team.name,
            "team_id": str(team.id),
            "total_strokes": strokes_given,
            "strokes": hdcp_dict,
        }

    return match_hdcp


def listToDictionary (list):

    dictionary = {}

    for item in list:
        dictionary[str(item["number"])] = item

    return dictionary

