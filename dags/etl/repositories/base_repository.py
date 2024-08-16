from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def fact_exists(self, fact_hash):
        pass

    @abstractmethod
    def save_facts_batch(self, data):
        pass
