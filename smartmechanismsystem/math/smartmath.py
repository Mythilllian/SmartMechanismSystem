import smartmechanismsystem.exceptions.exceptions.NoStagesGivenException

class SmartMath:
    """
    SmartMath class to handle math operations.
    """
    def sensor_to_mechanism_ratio(*stages: float) -> float:
        """
        Create the sensor to mechanism ratio.

        :param stages: Stages between the motor and output shaft.
        :return: Sensor to mechanism ratio.
        """
        if len(stages) == 0:
            raise NoStagesGivenException()
        ratio = 1
        for stage in stages:
            ratio *= stage
        return ratio
    
    def gearbox(*stages: float) -> float:
        """
        Create the gear ratio based off of the stages in the gear box.

        :param stages: Stages between the motor and output shaft.
        :return: Rotor rotations to mechanism ratio in the form of MECHANISM_ROTATIONS/ROTOR_ROTATIONS or ROTOR_ROTATIONS:MECHANISM_ROTATIONS
        """
        if len(stages) == 0:
            raise NoStagesGivenException()
        gearbox = 1
        for stage in stages:
            gearbox *= stage
        return gearbox