from collections import deque

class MusicQueue:
    def __init__(self):
        self.queues = {}
        self.now_playing = {}
    
    def add_song(self, server_id, song_info):
        """Aggiunge una canzone alla coda"""
        if server_id not in self.queues:
            self.queues[server_id] = deque()

        self.queues[server_id].append(song_info)
        
        return len(self.queues[server_id])
    
    def get_next_song(self, server_id):
        """Prende la prossima canzone dalla coda"""
        if server_id in self.queues and self.queues[server_id]:
            return self.queues[server_id].popleft()
        return None
    
    def clear_queue(self, server_id):
        """Pulisce la coda di un server"""
        if server_id in self.queues:
            self.queues[server_id].clear()
    
    def is_empty(self, server_id):
        """Controlla se la coda è vuota"""
        return server_id not in self.queues or len(self.queues[server_id]) == 0
    
    def show_queue(self, server_id):
        """Mostra le canzoni in coda"""
        if server_id not in self.queues:
            return []
        
        songs = list(self.queues[server_id])
        return songs[:10]