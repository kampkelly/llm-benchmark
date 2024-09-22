from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from database import Metric
from database.session import get_db


class MetricRepository:
    """
    This class handles database operations related to metrics.
    It provides a method to retrieve all metrics from the database.
    """
    def __init__(self, db: Session = Depends(get_db)):
        """
        Initializes the MetricRepository with a database session.
        """
        self.db = db

    def get_metrics(self) -> List[Metric]:
        """
        Retrieves all metrics from the database.
        Returns:
            List[Metric]: A list of all metrics.
        """
        metrics = self.db.query(Metric).all()
        return metrics
