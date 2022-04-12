import math

SIDE_CHOICES = (("Front", "Front"), ("Back", "Back"), ("Both", "Both"))


FORMAT_CHOICES = (
    ("two-man-comb-matchplay", "Two Man Combined Matchplay"),
    ("two-man-mp-scramble", "Two Man Matchplay Scramble"),
    ("four-ball", "Four-Ball"),
    ("foursomes", "Foursomes"),
)


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
    hole_hdcp = sort_by_hole(hdcp_tuples)
    
    hdcp_list = []
    for hole in hole_hdcp:
        hdcp_list.append(hole[1])

    if team1_card.handicap > team2_card.handicap:
        team = team1_card.team
    else:
        team = team2_card.team

    # case where teams are equally matched - no strokes given
    match_hdcp = {"team": None, "strokes_given": 0, "strokes_per_hole": hole_hdcp}

    # team is the one given strokes
    if strokes_given:
        match_hdcp = {
            "team": team.name,
            "team_id": str(team.id),
            "strokes_given": strokes_given,
            "strokes_per_hole": hdcp_list,
        }

    return match_hdcp
