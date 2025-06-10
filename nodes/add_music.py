# add_music.py implementation
def select_music(state):
    # TODO: Use royalty-free music API or fixed collection
    music_track = "/music/epic_inspiration.mp3"
    return {**state, "music": music_track}