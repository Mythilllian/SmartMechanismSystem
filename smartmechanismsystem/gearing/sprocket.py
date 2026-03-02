from smartmechanismsystem.exceptions.exceptions import InvalidStageGivenException, NoStagesGivenException


class Sprocket:
    """
    Sprocket class to handle calculating the conversion factor of a sprocket in your mechanism.
    """
    reduction_stages: list[float]
    """
    Stages in the Sprocket chain.
    """
    sprocket_reduction_ratio: float
    """
    The input to output conversion factor.
    """

    def __init__(self, *sprocket_reduction_stage: float) -> None:
        """
        Create the sprocket given the teeth of each sprocket in the chain.

        :param sprocket_reduction_stage: Sprocket teeth, in the form of "IN:OUT" => IN/OUT
        """
        self.setup_stages(list(sprocket_reduction_stage))

    @staticmethod
    def from_stages(*reduction_stage: str) -> "Sprocket":
        """
        Construct the :class:`Sprocket` with the reduction stages given.
        
        :param reduction_stage: List of stages in the format of "IN:OUT".
        :return: Sprocket representation
        """
        stages: list[float] = []
        for stage in reduction_stage:
            parts = stage.split(":")
            if len(parts) == 0:
                raise InvalidStageGivenException(stage)
            _in = float(parts[0])
            _out = float(parts[1])
            stages.append(_in / _out)
        return Sprocket(*stages)
    
    def setup_stages(self, sprocket_reduction_stage: list[float]) -> None:
        """
        Set up the reduction stages for the :class:`Sprocket`

        :param sprocket_reduction_stage: Reductions in the form of "IN:OUT" => IN/OUT
        """
        self.reduction_stages = sprocket_reduction_stage
        if(len(self.reduction_stages) == 0):
            raise NoStagesGivenException()
        sprocket_ratio = 1
        for reduction_stage in self.reduction_stages:
            sprocket_ratio *= 1 / reduction_stage
        self.sprocket_reduction_ratio = sprocket_ratio

    def times(self, x: float) -> "Sprocket":
        """
        Multiply the sprocket reduction ratio by X.

        :param x: X to multiply by.
        :return: :class:`Sprocket` for chaining.
        """
        self.sprocket_reduction_ratio *= x
        return self

    def div(self, x: float) -> "Sprocket":
        """
        Divide the sprocket reduction ratio by X.

        :param x: X to divide by.
        :return: :class:`Sprocket` for chaining.
        """
        self.sprocket_reduction_ratio /= x
        return self
    
    def get_input_to_output_conversion_factor(self) -> float:
        """
        Get the conversion factor to transform the sprocket input into the sprocket output rotations.

        :return: OUT/IN or OUT:IN
        """
        return 1 / self.sprocket_reduction_ratio
    
    def get_output_to_input_conversion_factor(self) -> float:
        """
        Get the conversion factor to transform the sprocket output value into the sprocket input value.

        :return: IN:OUT or IN/OUT
        """
        return self.sprocket_reduction_ratio

