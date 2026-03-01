from abc import ABC, abstractmethod
from smartmechanismsystem.telemetry.telemetryfields import BooleanTelemetryField, DoubleTelemetryField

#TODO: expand stub

class SmartMotorController(ABC):
    @abstractmethod
    def get_unsupported_telemetry_fields(self) -> tuple[list[BooleanTelemetryField], list[DoubleTelemetryField]]:
        """
        Get a list of unsupported telemetry fields if any exist.

        :return: Optional list of unsupported telemetry fields.
        """
        pass
