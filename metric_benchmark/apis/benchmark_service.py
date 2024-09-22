from database import LLMRepository, MetricRepository, SimulatorRepository


class BenchmarkService:
    """
    This class provides a service for benchmarking large language models (LLMs)
    based on various metrics and simulations.
    It utilizes repositories for managing LLMs, metrics, and simulations to facilitate the benchmarking process.
    """
    def __init__(self,
                 llm_repository: LLMRepository,
                 metric_repository: MetricRepository,
                 simulator_repository: SimulatorRepository):
        """
        Initializes the BenchmarkService with the provided repositories for managing large language models,
        metrics, and simulations.
        """
        self.llm_repository = llm_repository
        self.metric_repository = metric_repository
        self.simulator_repository = simulator_repository

    def get_simulation_and_rankings(self):
        """
        Retrieves all metrics and their corresponding simulations, then ranks them based on their means.
        """
        metrics = self.metric_repository.get_metrics()
        results = []
        for metric in metrics:
            simulations = self.simulator_repository.get_metric_means_by_llm(metric.name)
            results.append({metric.name: simulations})

        return results
