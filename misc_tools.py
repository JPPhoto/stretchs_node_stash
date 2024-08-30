from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import InputField, OutputField
from invokeai.app.services.shared.invocation_context import InvocationContext
import random

SIZE_PAIRS = [
    (1256, 840),
    (1184, 888),
    (1024, 1024),
    (888, 1184),
    (1256, 840)
]


@invocation_output("random_sdxl_dimensions_output")
class RandomSDXLDimensionsOutput(BaseInvocationOutput):
    """Random SDXL Dimensions"""

    width: int = OutputField(title="Width")
    height: int = OutputField(title="Height")

@invocation("random_sdxl_dimensions_invocation", title="Random SDXL Dimensions", tags=["size", "image", "sdxl"], category="size", version="1.0.0")
class RandomSDXLDimensionsInvocation(BaseInvocation):
    """Outputs a random SDXL size."""

    seed: int = InputField(title="Seed", description="A seed for the randomness. Use -1 for non-deterministic.", default=-1)

    def invoke(self, context: InvocationContext) -> RandomSDXLDimensionsOutput:
        random.seed(self.seed)
        selected_pair = random.choice(SIZE_PAIRS)
        return RandomSDXLDimensionsOutput(width=selected_pair[0], height=selected_pair[1])