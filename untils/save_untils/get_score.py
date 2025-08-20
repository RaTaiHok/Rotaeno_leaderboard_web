def get_scores(*, player_data: tuple, mode: str) -> dict:
    if player_data:
        if mode == 'cloud':
            user_songdata = player_data["results"][0]["cloudSave"]["data"]["data"]["songs"]["songs"]
        elif mode == 'native':
            user_songdata = player_data["data"]["data"]["songs"]["songs"]
        
        scores = {}
        for song_id, song in user_songdata.items():
            scores[song_id] = {}
            
            if 'levels' in song:
                for diff, level_data in song['levels'].items():
                    if diff in ['I', 'II', 'III', 'IV', 'IV_Alpha']:
                        score = level_data.get('Score', 0)
                        diff_map = {'I': '0', 'II': '1', 'III': '2', 'IV': '3', 'IV_Alpha': '4'}
                        diff_index = diff_map[diff]
                        scores[song_id][diff_index] = score
        return scores
    return {}
