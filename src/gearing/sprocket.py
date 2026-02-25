from exceptions import InvalidStageGivenException, NoStagesGivenException


class Sprocket:
    reduction_stages: list[float]
    sprocket_reduction_ratio: float

    def __init__(*sprocket_reduction_stage: float) -> None:
        setup_stages(sprocket_reduction_stage)

    def from_stages(*reduction_stage: str) -> "Sprocket":
        stages = []
        for stage in reduction_stage:
            parts = stage.split(":")
            if len(parts) == 0:
                raise InvalidStageGivenException(stage)
            _in = float(parts[0])
            _out = float(parts[1])
            stages.append(_in / _out)
        return Sprocket(stages)
    
    def setup_stages(self, sprocket_reduction_stage: list[float]) -> None:
        self.reduction_stages = sprocket_reduction_stage
        if(len(self.reduction_stages) == 0)
            raise NoStagesGivenException()
        sprocket_ratio = 1
        for reduction_stage in self.reduction_stages:
            sprocket_ratio *= 1 / reduction_stage
        self.sprocket_reduction_ratio = sprocket_ratio

    def times(self, x: float) -> "GearBox":
        self.gear_reduction_ratio *= x
        return self

    def div(self, x: float) -> "GearBox":
        self.gear_reduction_ratio /= x
        return self
    
    def get_input_to_output_conversion_factor(self) -> float:
        return 1 / self.sprocket_reduction_ratio
    
    def get_output_to_input_conversion_factor(self) -> float:
        return self.sprocket_reduction_ratio

