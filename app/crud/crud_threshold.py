from sqlalchemy.orm import Session
from typing import Optional
from app.orm.models import AlgorithmThreshold, StretchingThreshold


class CRUDStretchingThresholds:
    def __init__(self, db: Session):
        self.db = db

    def get_stretching_thresholds(self) -> Optional[StretchingThreshold]:
        return self.db.query(StretchingThreshold).first()

    def add__stretching_thresholds(self, stretching_thresholds: StretchingThreshold):
        self.db.add(stretching_thresholds)
        self.db.commit()
        self.db.refresh(stretching_thresholds)

    def update_stretching_thresholds(self, stretching_thresholds: StretchingThreshold, new_values: dict):
        # 遍历 new_values 并将其设置为 thresholds 对象的属性
        for key, value in new_values.items():
            setattr(stretching_thresholds, key, value)
        self.db.commit()
        self.db.refresh(stretching_thresholds)

    def create_stretching_thresholds(self) -> StretchingThreshold:
        stretching_thresholds = StretchingThreshold()
        self.db.add(stretching_thresholds)
        self.db.commit()
        self.db.refresh(stretching_thresholds)
        return stretching_thresholds



class CRUDAlgorithmThresholds:
    def __init__(self, db: Session):
        self.db = db

    def get_algorithm_thresholds(self) -> Optional[AlgorithmThreshold]:
        return self.db.query(AlgorithmThreshold).first()

    def add_algorithm_thresholds(self, algorithm_thresholds: AlgorithmThreshold):
        self.db.add(algorithm_thresholds)
        self.db.commit()
        self.db.refresh(algorithm_thresholds)

    def update_algorithm_thresholds(self, algorithm_thresholds: AlgorithmThreshold, new_values: dict):
        # 遍历 new_values 并将其设置为 thresholds 对象的属性
        for key, value in new_values.items():
            setattr(algorithm_thresholds, key, value)
        self.db.commit()
        self.db.refresh(algorithm_thresholds)

    def create_algorithm_thresholds(self) -> AlgorithmThreshold:
        algorithm_thresholds = AlgorithmThreshold()
        self.db.add(algorithm_thresholds)
        self.db.commit()
        self.db.refresh(algorithm_thresholds)
        return algorithm_thresholds
