import pytz

from datetime import datetime
from .xp_calc import xp_calc

def score_rank(score: int):
    if 0 <= score <= 499999:
        rank = "F"
    elif 500000 <= score <= 599999:
        rank = "E"
    elif 600000 <= score <= 699999:
        rank = "D"
    elif 700000 <= score <= 799999:
        rank = "C"
    elif 800000 <= score <= 849999:
        rank = "B"
    elif 850000 <= score <= 899999:
        rank = "A"
    elif 900000 <= score <= 949999:
        rank = "A+"
    elif 950000 <= score <= 979999:
        rank = "S"
    elif 980000 <= score <= 999999:
        rank = "S+"
    elif 1000000 <= score <= 1007999:
        rank = "EX"
    elif 1008000 <= score <= 1010000:
        rank = "EX+"
    else:
        rank = "none"
    return rank


def parse_playtime(time_str):
    time_str = time_str.lstrip('-')

    parts = time_str.split(':')
    if len(parts) != 3:
        raise ValueError()
    
    hours = float(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])

    if minutes >= 60 or seconds >= 60:
        raise ValueError()

    total_seconds = hours * 3600 + minutes * 60 + seconds

    hours = int(total_seconds // 3600)
    total_seconds %= 3600
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60

    return f"{hours}小时{minutes}分{int(seconds)}秒"


def get_profile(*, player_name: str, player_rating, player_data: tuple, mode: str) -> dict:
    if player_data:
        if mode == 'cloud':
            user_songdata = player_data["results"][0]["cloudSave"]["data"]["data"]["songs"]["songs"]
            xp = str(xp_calc(int(player_data["results"][0]["cloudSave"]["data"]["data"]["PlayerLevel"]["AccumXp"]))[0])
            xp_percent = float(xp_calc(int(player_data["results"][0]["cloudSave"]["data"]["data"]["PlayerLevel"]["AccumXp"]))[1] / xp_calc(int(player_data["results"][0]["cloudSave"]["data"]["data"]["PlayerLevel"]["AccumXp"]))[2])
            badge = player_data["results"][0]["cloudSave"]["data"]["data"]["badges"]["EquippedBadgeId"]
            char = player_data["results"][0]["cloudSave"]["data"]["data"]["collectable-character"]["EquippedCharacterId"]
            backgroud = player_data["results"][0]["cloudSave"]["data"]["data"]["collectable-background"]["EquippedBackgroundId"]
            play_records = player_data["results"][0]["cloudSave"]["data"]["data"]["playRecords"]
            create = player_data["results"][0]["createdAt"]
            playtime = player_data["results"][0]["cloudSave"]["TotalPlayTime"]
        elif mode == 'native':
            user_songdata = player_data["data"]["data"]["songs"]["songs"]
            xp = str(xp_calc(int(player_data["data"]["data"]["PlayerLevel"]["AccumXp"]))[0])
            xp_percent = float(xp_calc(int(player_data["data"]["data"]["PlayerLevel"]["AccumXp"]))[1] / xp_calc(int(player_data["data"]["data"]["PlayerLevel"]["AccumXp"]))[2])
            badge = player_data["data"]["data"]["badges"]["EquippedBadgeId"]
            char = player_data["data"]["data"]["collectable-character"]["EquippedCharacterId"]
            backgroud = player_data["data"]["data"]["collectable-background"]["EquippedBackgroundId"]
            play_records = player_data["data"]["data"]["playRecords"]
            create = False
            playtime = player_data["TotalPlayTime"]

    song_counts = str(len(user_songdata))
    
    e_diff_chart_counts = {'I': 0, 'II': 0, 'III': 0, 'IV': 0, 'IV_Alpha': 0}
    totle_chart_counts = 0
    e_diff_cleared_counts = {'I': 0, 'II': 0, 'III': 0, 'IV': 0, 'IV_Alpha': 0}
    totle_cleared_counts = 0
    e_diff_score_counts = {'I': 0, 'II': 0, 'III': 0, 'IV': 0, 'IV_Alpha': 0}
    totle_score_counts = 0
    e_diff_clear_score_counts = {'I': 0, 'II': 0, 'III': 0, 'IV': 0, 'IV_Alpha': 0}
    totle_clear_score_counts = 0
    totle_score_rank_counts = {'F': 0, 'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'A+': 0, 'S': 0, 'S+': 0, 'EX': 0, 'EX+': 0}
    e_diff_score_rank_counts = {
        'I': {'F': 0, 'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'A+': 0, 'S': 0, 'S+': 0, 'EX': 0, 'EX+': 0},
        'II': {'F': 0, 'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'A+': 0, 'S': 0, 'S+': 0, 'EX': 0, 'EX+': 0},
        'III': {'F': 0, 'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'A+': 0, 'S': 0, 'S+': 0, 'EX': 0, 'EX+': 0},
        'IV': {'F': 0, 'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'A+': 0, 'S': 0, 'S+': 0, 'EX': 0, 'EX+': 0},
        'IV_Alpha': {'F': 0, 'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'A+': 0, 'S': 0, 'S+': 0, 'EX': 0, 'EX+': 0}
    }
    e_diff_flag_counts = {
        'I': {'FC': 0, 'AP': 0, 'APP': 0},
        'II': {'FC': 0, 'AP': 0, 'APP': 0},
        'III': {'FC': 0, 'AP': 0, 'APP': 0},
        'IV': {'FC': 0, 'AP': 0, 'APP': 0},
        'IV_Alpha': {'FC': 0, 'AP': 0, 'APP': 0}
    }
    flag_counts = {'FC': 0, 'AP': 0, 'APP': 0}
    
    for song_name, song in user_songdata.items():
        if 'levels' in song:
            for level, data in song['levels'].items():
                if level in e_diff_chart_counts:
                    e_diff_chart_counts[level] += 1
                    totle_chart_counts += 1
                    score = data.get('Score', 0)
                    e_diff_score_counts[level] += score
                    totle_score_counts += score
                    is_cleared = data.get('IsCleared')
                    if is_cleared is True:
                        e_diff_cleared_counts[level] += 1
                        e_diff_clear_score_counts[level] += score
                        totle_clear_score_counts += score
                        totle_cleared_counts += 1
                        rank = score_rank(score)
                        totle_score_rank_counts[rank] += 1
                        e_diff_score_rank_counts[level][rank] += 1
                        flag = data.get('Flag', 'NONE')
                        if flag in flag_counts:
                            if flag == 'APP':
                                flag_counts['FC'] += 1
                                flag_counts['AP'] += 1
                                flag_counts['APP'] += 1
                                e_diff_flag_counts[level]['FC'] += 1
                                e_diff_flag_counts[level]['AP'] += 1
                                e_diff_flag_counts[level]['APP'] += 1
                            elif flag == 'AP':
                                flag_counts['FC'] += 1
                                flag_counts['AP'] += 1
                                e_diff_flag_counts[level]['FC'] += 1
                                e_diff_flag_counts[level]['AP'] += 1
                            elif flag == 'FC':
                                flag_counts['FC'] += 1
                                e_diff_flag_counts[level]['FC'] += 1

    grand_total_score = totle_chart_counts * 1010000
    grand_i_score = e_diff_chart_counts['I'] * 1010000
    grand_ii_score = e_diff_chart_counts['II'] * 1010000
    grand_iii_score = e_diff_chart_counts['III'] * 1010000
    grand_iv_score = e_diff_chart_counts['IV'] * 1010000
    grand_iv_alpha_score = e_diff_chart_counts['IV_Alpha'] * 1010000

    # Play Counts
    TotalPlayCount = play_records["TotalPlayCount"]
    PlayCountI = play_records["PlayCountI"]
    PlayCountIi = play_records["PlayCountIi"]
    PlayCountIii = play_records["PlayCountIii"]
    PlayCountIv = play_records["PlayCountIv"]

    # Judgement Counts
    PerfectPlus = play_records["PerfectPlus"]
    Perfect = play_records["Perfect"]
    Good = play_records["Good"]
    Early = play_records["Early"]
    Late = play_records["Late"]
    Miss = play_records["Miss"]

    # Note Counts
    Tap = play_records["Tap"]
    Slide = play_records["Slide"]
    Flick = play_records["Flick"]
    Catch = play_records["Catch"]
    Rotate = play_records["Rotate"]

    # Totel Score Rank Counts
    TotalF = play_records['TotalF']
    TotalE = play_records['TotalE']
    TotalD = play_records['TotalD']
    TotalC = play_records['TotalC']
    TotalB = play_records['TotalB']
    TotalA = play_records['TotalA']
    TotalAPlus = play_records['TotalAPlus']
    TotalS = play_records['TotalS']
    TotalSPlus = play_records['TotalSPlus']
    TotalEx = play_records['TotalEx']
    TotalExPlus = play_records['TotalExPlus']


    return {
        'user_name': player_name,
        'user_rating': player_rating,
        'xp': xp,
        'xp_percent': xp_percent,
        'badge': badge,
        'char': char,
        'backgroud': backgroud,
        'create': (datetime.fromisoformat(create.replace('Z', '+00:00')).astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S') + '(UTC+8)') if create else "NONE",
        'playtime': parse_playtime(playtime),
        'song_counts': song_counts,
        'chart_counts': {
            'I': e_diff_chart_counts['I'],
            'II': e_diff_chart_counts['II'],
            'III': e_diff_chart_counts['III'],
            'IV': e_diff_chart_counts['IV'],
            'IV_Alpha': e_diff_chart_counts['IV_Alpha'],
            'Total': totle_chart_counts
        },
        'user_chart_counts': {
            'I': e_diff_cleared_counts['I'],
            'II': e_diff_cleared_counts['II'],
            'III': e_diff_cleared_counts['III'],
            'IV': e_diff_cleared_counts['IV'],
            'IV_Alpha': e_diff_cleared_counts['IV_Alpha'],
            'Total': totle_cleared_counts
        },
        'score_counts': {
            'I': e_diff_score_counts['I'],
            'II': e_diff_score_counts['II'],
            'III': e_diff_score_counts['III'],
            'IV': e_diff_score_counts['IV'],
            'IV_Alpha': e_diff_score_counts['IV_Alpha'],
            'I_average': e_diff_score_counts['I'] // e_diff_chart_counts['I'] if e_diff_chart_counts['I'] else 0,
            'II_average': e_diff_score_counts['II'] // e_diff_chart_counts['II'] if e_diff_chart_counts['II'] else 0,
            'III_average': e_diff_score_counts['III'] // e_diff_chart_counts['III'] if e_diff_chart_counts['III'] else 0,
            'IV_average': e_diff_score_counts['IV'] // e_diff_chart_counts['IV'] if e_diff_chart_counts['IV'] else 0,
            'IV_Alpha_average': e_diff_score_counts['IV_Alpha'] // e_diff_chart_counts['IV_Alpha'] if e_diff_chart_counts['IV_Alpha'] else 0,
            'Total': e_diff_score_counts['I'] + e_diff_score_counts['II'] + e_diff_score_counts['III'] + e_diff_score_counts['IV'] + e_diff_score_counts['IV_Alpha'],
            'Total_average': (e_diff_score_counts['I'] + e_diff_score_counts['II'] + e_diff_score_counts['III'] + e_diff_score_counts['IV'] + e_diff_score_counts['IV_Alpha']) // (e_diff_chart_counts['I'] + e_diff_chart_counts['II'] + e_diff_chart_counts['III'] + e_diff_chart_counts['IV'] + e_diff_chart_counts['IV_Alpha'])
        },
        'acc_score': {
            'I': e_diff_clear_score_counts['I'] // e_diff_cleared_counts['I'] if e_diff_cleared_counts['I'] > 0 else 0,
            'II': e_diff_clear_score_counts['II'] // e_diff_cleared_counts['II'] if e_diff_cleared_counts['II'] > 0 else 0,
            'III': e_diff_clear_score_counts['III'] // e_diff_cleared_counts['III'] if e_diff_cleared_counts['III'] > 0 else 0,
            'IV': e_diff_clear_score_counts['IV'] // e_diff_cleared_counts['IV'] if e_diff_cleared_counts['IV'] > 0 else 0,
            'IV_Alpha': e_diff_clear_score_counts['IV_Alpha'] // e_diff_cleared_counts['IV_Alpha'] if e_diff_cleared_counts['IV_Alpha'] > 0 else 0,
            'Total': totle_clear_score_counts // totle_cleared_counts if totle_cleared_counts > 0 else 0
        },
        'totle_score_counts': {
            'I': grand_i_score,
            'II': grand_ii_score,
            'III': grand_iii_score,
            'IV': grand_iv_score,
            'IV_Alpha': grand_iv_alpha_score,
            'Total': grand_total_score
        },
        'score_rank_counts': e_diff_score_rank_counts,
        'total_score_rank_counts': {
            'F': TotalF,
            'E': TotalE,
            'D': TotalD,
            'C': TotalC,
            'B': TotalB,
            'A': TotalA,
            'A+': TotalAPlus,
            'S': TotalS,
            'S+': TotalSPlus,
            'EX': TotalEx,
            'EX+': TotalExPlus
        },
        'flag_counts': {
            'I': {
                'FC': e_diff_flag_counts['I']['FC'],
                'AP': e_diff_flag_counts['I']['AP'],
                'APP': e_diff_flag_counts['I']['APP']
            },
            'II': {
                'FC': e_diff_flag_counts['II']['FC'],
                'AP': e_diff_flag_counts['II']['AP'],
                'APP': e_diff_flag_counts['II']['APP']
            },
            'III': {
                'FC': e_diff_flag_counts['III']['FC'],
                'AP': e_diff_flag_counts['III']['AP'],
                'APP': e_diff_flag_counts['III']['APP']
            },
            'IV': {
                'FC': e_diff_flag_counts['IV']['FC'],
                'AP': e_diff_flag_counts['IV']['AP'],
                'APP': e_diff_flag_counts['IV']['APP']
            },
            'IV_Alpha': {
                'FC': e_diff_flag_counts['IV_Alpha']['FC'],
                'AP': e_diff_flag_counts['IV_Alpha']['AP'],
                'APP': e_diff_flag_counts['IV_Alpha']['APP']
            },
            'grand_total': {
                'FC': flag_counts['FC'],
                'AP': flag_counts['AP'],
                'APP': flag_counts['APP']
            }
        },
        'play_counts': {
            'Total': TotalPlayCount,
            'I': PlayCountI,
            'II': PlayCountIi,
            'III': PlayCountIii,
            'IV': PlayCountIv
        },
        'judgement_counts': {
            'PerfectPlus': PerfectPlus,
            'Perfect': Perfect,
            'Good': Good,
            'Early': Early,
            'Late': Late,
            'Miss': Miss
        },
        'note_counts': {
            'Tap': Tap,
            'Slide': Slide,
            'Flick': Flick,
            'Catch': Catch,
            'Rotate': Rotate
        },
    }