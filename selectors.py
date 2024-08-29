from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.fields import InputField, OutputField
from invokeai.app.services.shared.invocation_context import InvocationContext


@invocation_output("int_selector_output")
class IntSelectorOutput(BaseInvocationOutput):
    """Int Selector Output"""

    output_int: int = OutputField(description="Selected Integer", title="Selected Int")


@invocation("int_selector", title="Integer Selector", tags=["int, integer"], category="integer", version="1.0.0")
class IntSelectorInvocation(BaseInvocation):
    """Allows boolean selection between two separate integer inputs"""

    use_second: bool = InputField(default=False, description="Use 2nd Input")
    int1: int = InputField(default=0, description="First Integer Input")
    int2: int = InputField(default=0, description="Second Integer Input")

    def invoke(self, context: InvocationContext) -> IntSelectorOutput:
        return IntSelectorOutput(output_int=(self.int2 if self.use_second else self.int1))


@invocation_output("string_selector_output")
class StringSelectorOutput(BaseInvocationOutput):
    """String Selector Output"""

    output_str: str = OutputField(description="Selected String", title="Selected String")


@invocation("string_selector", title="String Selector", tags=["str, string"], category="string", version="1.0.0")
class StringSelectorInvocation(BaseInvocation):
    """Allows boolean selection between two separate string inputs"""

    use_second: bool = InputField(default=False, description="Use 2nd Input")
    str1: str = InputField(default=0, description="First String Input")
    str2: str = InputField(default=0, description="Second String Input")

    def invoke(self, context: InvocationContext) -> StringSelectorOutput:
        return StringSelectorOutput(output_str=(self.str2 if self.use_second else self.str1))