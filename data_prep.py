from typing import List, Tuple
import numpy as np
import pandas as pd
import json

tracks = tracks = pd.read_csv('zapocet/data/tracks.csv', index_col=0, header=[0, 1])
echonest = pd.read_csv('zapocet/data/echonest.csv', index_col=0, header=[0, 1, 2])
genres = pd.read_csv('zapocet/data/genres.csv', index_col=0).sort_values(by=['parent'], ascending=True)

# Create song data:
    # song_tempo  = echonest[('audio_features', 'tempo')].copy()
    # song_genres = tracks[('track', 'genres')].copy()
song_data = pd.DataFrame(
    data = {
        'bpm': echonest[('echonest', 'audio_features', 'tempo')].copy(),
        'genres': tracks[('track', 'genres')].copy()
    }
)
song_data.dropna(inplace=True)

def contains_genre(genre_list:str, genre_id: int) -> bool:
    genres: List[int] = eval(genre_list)
    return (genre_id in genres)

def get_genre_data(genre_id: int) -> Tuple[int, float]:
    songs_filter = song_data['genres'].apply(lambda g_list: contains_genre(g_list, genre_id))
    songs_filtered = song_data[songs_filter]

    song_count = songs_filtered['bpm'].count()
    bpm_sum = songs_filtered['bpm'].agg('sum')

    return (int(song_count), float(bpm_sum))

def process_node(idx, parent_idx):
    id = idx
    name = genres.loc[idx, 'title']
    
    children_nodes = genres[genres['parent'] == idx]
    children = [process_node(child_id, idx) for child_id in children_nodes.index]
    children = [child for child in children if child != None]

    track_count, bpm_sum = get_genre_data(id)
    if track_count > 0 and len(children) > 0:
        children.append(
            {
                'name': name,
                'id' : id*1000,
                'parentId': id,
                'children': [],
                'track_count': track_count,
                'track_count_agg': track_count,
                'bpm_sum': bpm_sum,
                'bpm_sum_agg': bpm_sum
            }
        )

    children_count = sum(child['track_count_agg'] for child in children)
    children_bpm   = sum(child['bpm_sum_agg'] for child in children)
    

   

    if track_count + children_count > 0:
        return {
            'name': name,
            'id' : id,
            'parentId': parent_idx,
            'children': children,
            'track_count': 0,
            'track_count_agg': children_count,
            'bpm_sum': 0,
            'bpm_sum_agg': children_bpm
        }

    return None


if __name__ == '__main__':

    

    # print(song_data.info())
    # get_genre_data(514)

    # Create hierarchy
    top_nodes = genres[genres['parent'] == 0]
    children = [process_node(child_id, 0) for child_id in top_nodes.index]
    children = [child for child in children if child != None]

    children_count = sum(child['track_count_agg'] for child in children)
    children_bpm   = sum(child['bpm_sum_agg'] for child in children)
    


    print(f'tracks = {children_count}[{type(children_count)}]')
    print(f'bpm  = {children_bpm}[{type(children_bpm)}]')

    genre_data = {
        'name': 'all_genres',
        'id': 0,
        'children': children,
        'track_count': 0,
        'track_count_agg': children_count,
        'bpm_sum': 0,
        'bpm_sum_agg': children_bpm
    }

    # # Fill hierarchy with songs

    # # Save data
    with open('genre_data.json', 'w') as file:
        json.dump(genre_data, file)

