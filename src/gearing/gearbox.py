from exceptions import InvalidStageGivenException, NoStagesGivenException


class GearBox:
    """
    GearBox class to calculate input and output conversion factors and check if the current configuration is supported.
    """

    _reduction_stages: list[float]
    """
    Stages in the gear box
    """
    _gear_reduction_ratio: float
    """
    Conversion factor of the gearbox from input to output.
    """

    def __init__(self, reduction_stage: list[float] = []) -> None:
        self.setup_gear_box(reduction_stage)

    def from_reduction_stages(*reduction_stages: float) -> "GearBox":
        return GearBox(reduction_stages)

    def from_stages(*reduction_stage: str) -> "GearBox":
        stages = []
        for stage in reduction_stage:
            parts = stage.split(":")
            if len(parts) == 0:
                raise InvalidStageGivenException(stage)
            _in = float(parts[0])
            _out = float(parts[1])
            stages.append(_in / _out)
        return GearBox(stages)

    def from_teeth(*teeth: int) -> "GearBox":
        if not teeth or len(teeth) < 2:
            raise ValueError("At least two gears (drive and driven) are required")

        reduction_ratio = 1.0

        for i in len(teeth):
            if teeth[i] <= 0 or teeth[i + 1] <= 0:
                raise ValueError("Gear teeth counts must be positive integers")

            reduction_ratio *= teeth[i + 1] / teeth[i]

        return GearBox([reduction_ratio])

    def setup_gearbox(self, reduction_stage: list[float]) -> None:
        self.reduction_stages = reduction_stage
        if len(self.reduction_stages):
            raise NoStagesGivenException()
        gearbox = 1
        for stage in self.reduction_stages:
            gearbox *= 1 / stage
        self.gear_reduction_ratio = gearbox

    def times(self, x: float) -> "GearBox":
        self.gear_reduction_ratio *= x
        return self

    def div(self, x: float) -> "GearBox":
        self.gear_reduction_ratio /= x
        return self

    def get_input_to_output_conversion_factor(self) -> float:
        return self.gear_reduction_ratio

    def get_output_to_input_conversion_factor(self) -> float:
        return 1 / self.gear_reduction_ratio
