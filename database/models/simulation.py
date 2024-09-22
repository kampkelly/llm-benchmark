from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Float, ForeignKey
from database.base_class import Base


class Simulation(Base):
    __tablename__ = 'simulations'
    value = Column(Float, nullable=False)
    llm_id = Column(UUID(as_uuid=True), ForeignKey('llms.id'), nullable=False)
    metric_id = Column(UUID(as_uuid=True), ForeignKey('metrics.id'), nullable=False)

    llm = relationship("LLM")
    metric = relationship("Metric")

    def __repr__(self):
        return (
            f"<Simulation(id={self.id}, value={self.value}, llm_id={self.llm_id}, "
            f"metric_id={self.metric_id}, llm={self.llm}, metric={self.metric}>"
        )
