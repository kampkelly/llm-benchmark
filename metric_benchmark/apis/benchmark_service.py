import json
from fastapi import Depends
from redis_client import RedisClient, RedisKeys
from database import LLMRepository, MetricRepository, SimulatorRepository


class BenchmarkService:
    """
    This class provides a service for benchmarking large language models (LLMs)
    based on various metrics and simulations.
    """
    def __init__(self, llm_repository: LLMRepository = Depends(LLMRepository), 
                 metric_repository: MetricRepository = Depends(MetricRepository), 
                 simulator_repository: SimulatorRepository = Depends(SimulatorRepository)):
        self.llm_repository = llm_repository
        self.metric_repository = metric_repository
        self.simulator_repository = simulator_repository

    def get_simulation_and_rankings(self):
        """
        Retrieves all metrics and their corresponding simulations, then ranks them based on their means.
        """
        redis_client = RedisClient()
        if redis_client.redis.exists(RedisKeys.BENCHMARKS.value):
            redis_results = json.loads(redis_client.redis.get(RedisKeys.BENCHMARKS.value))
            return {"data": redis_results}

        metrics = self.metric_repository.get_metrics()
        results = []
        for metric in metrics:
            simulations = self.simulator_repository.get_metric_means_by_llm(metric.name)
            rounded_simulations = [
                {'llm_name': sim[0], 'mean_value': round(sim[1], 2)}
                for sim in simulations
            ]
            results.append({metric.name: rounded_simulations})

        redis_client.redis.set(RedisKeys.BENCHMARKS.value, json.dumps(results))

        return {"data": results}
