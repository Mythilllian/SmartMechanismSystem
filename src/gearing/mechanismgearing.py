from .gearbox import GearBox
from .sprocket import Sprocket


class MechanismGearing:
    GEARBOX: GearBox
    sprockets: Sprocket

    def __init__(gearbox: GearBox, sprocket: Sprocket = None):
        GEARBOX = gearbox
        sprockets = sprocket

    def get_rotor_to_mechanism_ratio(self) -> float:
        ratio = self.GEARBOX.get_input_to_output_conversion_factor()
        if self.sprockets:
            ratio *= self.sprockets.get_input_to_output_conversion_factor()
        return ratio

    def get_mechanism_to_rotor_ratio(self) -> float:
        ratio = self.GEARBOX.get_output_to_input_conversion_factor()
        if self.sprockets:
            ratio *= self.sprockets.get_output_to_input_conversion_factor()
        return ratio

    def div(self, i: float) -> "MechanismGearing":
        self.GEARBOX.div(i)
        return self
