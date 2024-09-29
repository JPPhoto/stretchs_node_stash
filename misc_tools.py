from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import FieldDescriptions, InputField, OutputField
from invokeai.app.services.shared.invocation_context import InvocationContext
import random
from invokeai.invocation_api import Input
import math
from typing import Tuple
from invokeai.backend.model_manager.config import BaseModelType
from invokeai.app.invocations.model import UNetField
from invokeai.app.invocations.constants import LATENT_SCALE_FACTOR

@invocation_output("random_aspect_ratio")
class RandomAspectRatioOutput(BaseInvocationOutput):
    """Random Aspect Ratio Output"""

    width: int = OutputField(title="Width")
    height: int = OutputField(title="Height")

@invocation("random_aspect_ratio_invocation", title="Random Aspect Ratio", tags=["size", "image", "dimensions"], category="size", version="1.0.0")
class RandomAspectRatioInvocation(BaseInvocation):
    """Outputs a random size for the supplied base model based on specified aspect ratio range."""

    seed: int = InputField(title="Seed", description="A seed for the randomness. Use -1 for non-deterministic.", default=-1)
    unet: UNetField = InputField(default=None, description=FieldDescriptions.unet)
    min_aspect_ratio: str = InputField(default="9:16", title="Minimum Aspect Ratio", description="Minimum aspect ratio in format 'width:height' (e.g., '1:1', '4:3')")
    max_aspect_ratio: str = InputField(default="16:9", title="Maximum Aspect Ratio", description="Maximum aspect ratio in format 'width:height' (e.g., '16:9', '2:1')")

    def parse_aspect_ratio(self, ratio_str: str) -> float:
        try:
            width, height = map(int, ratio_str.split(':'))
            return width / height
        except ValueError:
            raise ValueError(f"Invalid aspect ratio format: {ratio_str}. Please use format like '16:9' or '4:3'.")

    def generate_random_resolution(self, base_width: int, base_height: int, min_aspect_ratio: float, max_aspect_ratio: float) -> tuple[int, int]:
        base_megapixels = (base_width * base_height) / 1000000

        # Ensure min_aspect_ratio <= 1 <= max_aspect_ratio
        min_aspect_ratio = min(min_aspect_ratio, 1)
        max_aspect_ratio = max(max_aspect_ratio, 1)

        while True:
            # Generate a random aspect ratio between 1 and max(max_aspect_ratio, 1/min_aspect_ratio)
            aspect_ratio = random.uniform(1, max(max_aspect_ratio, 1/min_aspect_ratio))
            
            # If the generated ratio is less than 1, invert it to ensure width >= height
            if aspect_ratio < 1:
                aspect_ratio = 1 / aspect_ratio

            new_height = math.sqrt(base_megapixels * 1000000 / aspect_ratio)
            new_width = new_height * aspect_ratio
            
            new_height = round(new_height)
            new_width = round(new_width)
            
            if new_width >= 64 and new_height >= 64:
                return new_width, new_height
    
    # from IdealSize node
    def trim_to_multiple_of(self, *args: int, multiple_of: int = LATENT_SCALE_FACTOR) -> Tuple[int, ...]:
        return tuple((x - x % multiple_of) for x in args)

    def invoke(self, context: InvocationContext) -> RandomAspectRatioOutput:
        if self.seed != -1:
            random.seed(self.seed)

        try:
            min_ratio = self.parse_aspect_ratio(self.min_aspect_ratio)
            max_ratio = self.parse_aspect_ratio(self.max_aspect_ratio)
        except ValueError as e:
            raise ValueError(str(e))

        if max_ratio < min_ratio:
            min_ratio, max_ratio = max_ratio, min_ratio


        # Get size for base model (taken from IdealSize node)
        unet_config = context.models.get_config(self.unet.unet.key)
        dimension: float = 512
        if unet_config.base == BaseModelType.StableDiffusion2:
            dimension = 768
        elif unet_config.base == BaseModelType.StableDiffusionXL:
            dimension = 1024
        elif unet_config.base == BaseModelType.Flux:
            dimension = 1024
        
        # Get random res
        width, height = self.generate_random_resolution(dimension, dimension, min_ratio, max_ratio)

        # Get adjusted size (taken from IdealSize node)
        aspect = width / height
        min_dimension = math.floor(dimension * 0.5)
        model_area = dimension * dimension  # hardcoded for now since all models are trained on square images

        if aspect > 1.0:
            init_height = max(min_dimension, math.sqrt(model_area / aspect))
            init_width = init_height * aspect
        else:
            init_width = max(min_dimension, math.sqrt(model_area * aspect))
            init_height = init_width / aspect

        scaled_width, scaled_height = self.trim_to_multiple_of(
            math.floor(init_width),
            math.floor(init_height),
        )

        return RandomAspectRatioOutput(width=scaled_width, height=scaled_height)