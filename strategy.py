from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Strategy(ABC):
    '''
    定义清洗策略
    '''

    @abstractmethod
    def cleaning(self, nps):
        pass



