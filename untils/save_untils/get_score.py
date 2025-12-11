def get_scores(*, player_data: tuple, mode: str) -> tuple:
    if player_data:
        if mode == 'cloud':
            user_songdata = player_data["results"][0]["cloudSave"]["data"]["data"]["songs"]["songs"]
        elif mode == 'native':
            user_songdata = player_data["data"]["data"]["songs"]["songs"]
        
        scores = {}
        flags = {}
        for song_id, song in user_songdata.items():
            scores[song_id] = {}
            flags[song_id] = {}
            
            if 'levels' in song:
                for diff, level_data in song['levels'].items():
                    if diff in ['I', 'II', 'III', 'IV', 'IV_Alpha']:
                        score = level_data.get('Score', 0)
                        is_cleared = level_data.get('IsCleared', False)
                        flag = level_data.get('Flag', 'NONE')
                        
                        if not is_cleared:
                            display_flag = 'Fail'
                        elif flag == 'APP':
                            display_flag = 'AP+'
                        elif flag == 'AP':
                            display_flag = 'AP'
                        elif flag == 'FC':
                            display_flag = 'FC'
                        else:
                            display_flag = 'Clear'
                        
                        diff_map = {'I': '0', 'II': '1', 'III': '2', 'IV': '3', 'IV_Alpha': '4'}
                        diff_index = diff_map[diff]
                        scores[song_id][diff_index] = score
                        flags[song_id][diff_index] = display_flag
        return scores, flags
    return {}, {}
