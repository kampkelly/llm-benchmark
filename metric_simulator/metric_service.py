from database import LLMRepository, MetricRepository, SimulatorRepository
from metric_simulator.lib import MetricGenerator


class MetricService:
    """
    This class provides methods to simulate data points and remove metrics.
    """
    def __init__(self,
                 llm_repository: LLMRepository,
                 metric_repository: MetricRepository,
                 simulator_repository: SimulatorRepository):
        """
        Initializes the MetricService with the provided repositories.
        """
        self.llm_repository = llm_repository
        self.metric_repository = metric_repository
        self.simulator_repository = simulator_repository

    def simulate_data_points(self):
        """
        Simulates data points for all LLMs and metrics.
        It uses MetricGenerator to generate the data points and stores them with SimulatorRepository
        """
        llms = self.llm_repository.get_llms()
        metrics = self.metric_repository.get_metrics()

        store = {}

        for llm in llms:
            metric_generator = MetricGenerator(llm.company_name, llm.name)
            store[llm.id] = {}
            for metric in metrics:
                generated_metrics = metric_generator.generate_data_points(metric.name)
                store[llm.id] = {metric.id: generated_metrics}

                self.simulator_repository.bulk_add_metrics(llm.id, metric.id, generated_metrics)

    def remove_metrics(self):
        """
        Removes all metrics from the database.
        """
        self.simulator_repository.remove_all_metrics()
