from typing import Dict, List, Optional
from config import Config

class QueueManager:
    def __init__(self):
        self.queues: Dict[int, List[Dict]] = {}
    
    def add_to_queue(self, chat_id: int, song: Dict):
        """Kuyruğa şarkı ekle"""
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        
        # Maksimum kuyruk boyutunu kontrol et
        if len(self.queues[chat_id]) >= Config.MAX_QUEUE_SIZE:
            return False
        
        self.queues[chat_id].append(song)
        return True
    
    def get_queue(self, chat_id: int) -> List[Dict]:
        """Kuyruğu getir"""
        return self.queues.get(chat_id, [])
    
    def get_current_song(self, chat_id: int) -> Optional[Dict]:
        """Şu anki şarkıyı getir"""
        queue = self.queues.get(chat_id, [])
        return queue[0] if queue else None
    
    def skip_song(self, chat_id: int) -> Optional[Dict]:
        """Şarkıyı atla"""
        if chat_id in self.queues and self.queues[chat_id]:
            self.queues[chat_id].pop(0)
            return self.queues[chat_id][0] if self.queues[chat_id] else None
        return None
    
    def clear_queue(self, chat_id: int):
        """Kuyruğu temizle"""
        if chat_id in self.queues:
            self.queues[chat_id] = []
    
    def get_queue_position(self, chat_id: int, file_path: str) -> int:
        """Kuyruktaki pozisyonu bul"""
        queue = self.queues.get(chat_id, [])
        for i, song in enumerate(queue):
            if song['file_path'] == file_path:
                return i
        return -1
    
    def remove_from_queue(self, chat_id: int, position: int) -> bool:
        """Kuyruktan şarkı çıkar"""
        if chat_id in self.queues and 0 <= position < len(self.queues[chat_id]):
            self.queues[chat_id].pop(position)
            return True
        return False
