__all__ = ["ArmConfigurationException", "DifferentialMechanismConfigurationException", "DoubleJointedArmConfigurationException", "ElevatorConfigurationException", "FlyWheelConfigurationException", "InvalidStageGivenException", "MotorNotPresentException", "NoStagesGivenException", "PivotConfigurationException", "SmartMotorControllerConfigurationException", "SwerveDriveConfigurationException"]

class ArmConfigurationException(RuntimeError):
    """
    Exception for when the Arm is configured incorrectly
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        Arm configuration exception.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use ArmConfig." + remedy_function + " to fix this error."
        super().__init__(self.message)

class DifferentialMechanismConfigurationException(RuntimeError):
    """
    Exception for when the Differential Mechanism is configured incorrectly.
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        Arm configuration exception.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use DifferentialMechanism." + remedy_function + " to fix this error."
        super().__init__(self.message)

class DoubleJointedArmConfigurationException(RuntimeError):
    """
    Exception for when the Arm is configured incorrectly.
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        Arm configuration exception.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use ArmConfig." + remedy_function + " to fix this error."
        super().__init__(self.message)

class ElevatorConfigurationException(RuntimeError):
    """
    Exception for when the Elevator is configured incorrectly.
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        Elevator configuration exception.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use ElevatorConfig." + remedy_function + " to fix this error."
        super().__init__(self.message)

class FlyWheelConfigurationException(RuntimeError):
    """
    Exception for when the FlyWheel is configured incorrectly.
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        FlyWheel configuration exception.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use FlyWheelConfig." + remedy_function + " to fix this error."
        super().__init__(self.message)

class InvalidStageGivenException(RuntimeError):
    """
    Exception for math errors when trying to find the sensor to mechanism ratio.
    """
    def __init__(self, stage: str):
        """
        Constructs exception for failure to provide stages.

        :param stage: Stage given.
        """
        self.message = "Invalid stage given! '" + stage + "'; should be in the format of 'IN:OUT'!"
        super().__init__(self.message)

class MotorNotPresentException(RuntimeError):
    """
    Custom exception for when there is no motor in the mechanism.
    """
    def __init__(self, mechanism_type: str):
        """
        Constructs exception for SmartMechanism.

        :param mechanism_type: Name of the mechanism
        """
        self.message = mechanism_type + " primary motor not present! Please set one using `setMotor(SmartMotorController.create(MOTOR_CONTROLLER, DCMotor.getNEO(1))`"
        super().__init__(self.message)

class NoStagesGivenException(RuntimeError):
    """
    Exception for math errors when trying to find the sensor to mechanism ratio.
    """
    def __init__(self):
        """
        Constructs exception for failure to provide stages.
        """
        self.message = "No stages given!"
        super().__init__(self.message)

class PivotConfigurationException(RuntimeError):
    """
    Exception for when the Pivot is configured incorrectly.
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        Pivot configuration exception.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use PivotConfig." + remedy_function + " to fix this error."
        super().__init__(self.message)

class SmartMotorControllerConfigurationException(RuntimeError):
    """
    Exception for when the SmartMotorController is configured incorrectly.
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        SmartMotorControllerConfigurationException constructor.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use SmartMotorControllerConfig." + remedy_function + " to fix this error."
        super().__init__(self.message)

class SwerveDriveConfigurationException(RuntimeError):
    """
    SwerveDrive Config Exception
    """
    def __init__(self, message: str, result: str, remedy_function: str):
        """
        SwerveDrive configuration exception.

        :param message: Message to display.
        :param result: Result of the configuration.
        :param remedy_function: Remedy function to use.
        """
        self.message = message + "!\n" + result + "\nPlease use SwerveDriveConfig." + remedy_function + " to fix this error."
        super().__init__(self.message)