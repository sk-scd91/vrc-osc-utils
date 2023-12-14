from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_bundle_builder import OscBundleBuilder

from vrc_osc_utils.avatar_config import AvatarConfig

class OscType:
    int = 'i'
    float = 'f'
    true = 'T'
    false = 'F'

VrcValueType = int | float | bool

def _clamp_value_and_type(value: VrcValueType, osc_type: str):

    # If there is no explicit type, find its matching type.
    if osc_type == None:
        if isinstance(value, float):
            osc_type = OscType.float
        elif isinstance(value, int):
            osc_type = OscType.int
        elif value is True:
            osc_type = OscType.true
        elif value is False:
            osc_type = OscType.false
        else:
            raise TypeError(f"VRChat OSC only supports int, float, or bool values. Found {type(value)}.")
    
    if osc_type == OscType.float:
        # Clamp float value to the range [-1, 1].
        return max(-1.0, min(1.0, float(value))), osc_type
    elif osc_type == OscType.int:
        # Clamp int value to the range [0, 255].
        return max(0, min(255, int(value))), osc_type
    elif osc_type == OscType.true or osc_type == OscType.false:
        return bool(value), OscType.true if value else OscType.false
    else:
        raise TypeError(f"OSC type '{osc_type}' not supported.")

def avatar_param_address(expression: str) -> str:
    """
    Creates an OSC address string that points to an avatar parameter.
    """

    return "/avatar/parameters/" + expression

class AvatarParamFactory(object):

    def __init__(self, schema: AvatarConfig = None) -> None:
        self._parameter_schema = {}
        if schema is not None:
            self._parameter_schema = {p.name: p.input for p in schema.parameters
                if p is not None and p.input is not None}

    def _has_schema(self) -> bool:
        return bool(self._parameter_schema)
    
    def _get_address_and_type_for_expression(self, expression: str):
        if expression in self._parameter_schema:
            exp_output = self._parameter_schema[expression]
            address = exp_output.address
            type = None
            if exp_output.type == "Float":
                type = OscType.float
            elif exp_output.type == "Int":
                type = OscType.int
            elif exp_output.type == "Bool":
                type = OscType.true
            else:
                raise TypeError(f"Type not yet supported '{exp_output.type}'.")
            return address, type
        else:
            raise KeyError(f"Expression '{expression}' not in avatar config.")

    def message(self, expression: str, value: VrcValueType, type: str=None):
        address = None
        if self._has_schema():
            address, type = self._get_address_and_type_for_expression(expression)
        else:
            address = avatar_param_address(expression)
        
        builder = OscMessageBuilder(address)

        value, type = _clamp_value_and_type(value, type)

        builder.add_arg(value, type)
        return builder.build()

    def bundle(self, **expressions):
        """
        Creates an OSC message bundle to atomically change multiple avatar parameter.

        Note: This only creates bundles that execute immediately. VRChat does not currently support delayed
        bundles, and the NTP timetag format it uses is broken after the year 2036.
        """
        
        builder = OscBundleBuilder(0)
        for expression, value in expressions.items():
            builder.add_content(self.message(expression, value))
        return builder.build()

