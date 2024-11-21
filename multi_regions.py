from ray import serve
from ray.serve.handle import DeploymentHandle
from typing import List
import random


@serve.deployment
class Model:
    def __call__(self) -> str:
        return "Simple Model"


@serve.deployment
class Router:
    def __init__(self, deploy_list: List[DeploymentHandle]):
        # Store handles to all model deployments
        self.deploy_handles = deploy_list

    async def __call__(self) -> str:
        # Write your load-balancing logic here
        chosen_handle = random.choice(self.deploy_handles)
        return await chosen_handle.remote()


# Create model deployments for different zones
model_us = Model.options(name="model_us").bind()
model_eu = Model.options(name="model_eu").bind()
model_asia = Model.options(name="model_asia").bind()

app = Router.bind([model_us, model_eu, model_asia])

serve.run(app)
