from .gearbox import GearBox
from .sprocket import Sprocket


class MechanismGearing:
    """
    Mechanism gearing for conversions from the motor output to the mechanism output.
    """
    _GEARBOX: GearBox
    """
    Mechanism gearbox attached to the motor.
    """
    _sprocket: Sprocket
    """
    Mechanism sprockets attached to the gearbox.
    """

    def __init__(self, gearbox: GearBox, sprocket: Sprocket = None):
        """
        Initialize the :class:`MechanismGearing` with a :class:`GearBox` and :class:`Sprocket`
        
        :param gearbox: :class:`GearBox` attached to the motor.
        :param sprocket: :class:`Sprocket` attached to the gearbox.
        """
        self._GEARBOX = gearbox
        self._sprocket = sprocket

    def get_rotor_to_mechanism_ratio(self) -> float:
        """
        Get the sensor to the mechanism ratio for the motor to the mechanism.

        :return: OUT:IN or OUT/IN ratio to use for sensor to mechanism calculations.
        """
        ratio = self._GEARBOX.get_input_to_output_conversion_factor()
        if self._sprocket:
            ratio *= self._sprocket.get_input_to_output_conversion_factor()
        return ratio

    def get_mechanism_to_rotor_ratio(self) -> float:
        """
        Get the mechanism rotation to sensor rotation ratio for the mechanism. AKA THE REDUCTION!

        :return: IN:OUT or IN/OUT to use for mechanism to sensor calculations.
        """
        ratio = self._GEARBOX.get_output_to_input_conversion_factor()
        if self._sprocket:
            ratio *= self._sprocket.get_output_to_input_conversion_factor()
        return ratio

    def div(self, i: float) -> "MechanismGearing":
        """
        Divide the gearbox reduction ratio by i.

        :param i: Numerator.
        :return: :class:`MechanismGearing` for chaining.
        """
        self._GEARBOX.div(i)
        return self
