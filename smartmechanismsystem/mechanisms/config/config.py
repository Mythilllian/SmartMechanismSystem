from wpimath.units import radians_per_second, meters, kilograms
from wpilib import Color, Color8Bit
from wpimath.geometry import Translation3d
from smartmechanismsystem.motorcontrollers.smartmotorcontroller import (
    SmartMotorController,
)
from smartmechanismsystem.motorcontrollers.smartmotorcontrollerconfig import (
    TelemetryVerbosity,
)
from smartmechanismsystem.exceptions.exceptions import FlyWheelConfigurationException
from enum import Enum, auto


class MechanismPositionConfig:
    class Plane(Enum):
        XZ = auto()
        YZ = auto()
        XY = auto()

    _robot_to_mechanism: Translation3d
    _max_robot_length: meters
    _max_robot_height: meters
    _plane: Plane = Plane.XZ

    def with_relative_position(
        self, robot_to_mechanism: Translation3d
    ) -> "MechanismPositionConfig":
        self._robot_to_mechanism = robot_to_mechanism
        return self

    def with_max_robot_length(self, robot_length: meters) -> "MechanismPositionConfig":
        self._max_robot_length = robot_length
        return self

    def with_max_robot_height(self, robot_height: meters) -> "MechanismPositionConfig":
        self._max_robot_height = robot_height
        return self

    def with_movement_plane(self, plane: Plane) -> "MechanismPositionConfig":
        self._plane = plane
        return self

    def get_mechanism_x(self, length: meters) -> meters:
        if (
            self.plane == MechanismPositionConfig.Plane.YZ
            or self.plane == MechanismPositionConfig.Plane.XY
        ):
            return (
                self._robot_to_mechanism.Y() + self.get_window_x_dimension(length) / 2
                if self._robot_to_mechanism
                else length
            )
        return (
            self._robot_to_mechanism.X() + self.get_window_x_dimension(length) / 2
            if self._robot_to_mechanism
            else length
        )

    def get_mechanism_y(self, y: meters):
        return self._robot_to_mechanism.Z() if self._robot_to_mechanism else y

    def get_window_x_dimension(self, length: meters) -> meters:
        return self._max_robot_length if self._max_robot_length else length * 2

    def get_window_y_dimension(self, length: meters) -> meters:
        return self._max_robot_height if self._max_robot_height else length * 2

    def get_relative_position(self) -> Translation3d:
        return self._robot_to_mechanism

    def get_movement_plane(self) -> Plane:
        return self._plane


class FlyWheelConfig:
    _motor: SmartMotorController
    _network_table_name: str
    _min_velocity: radians_per_second
    _max_velocity: radians_per_second
    _telemetry_name: str
    _telemetry_verbosity: TelemetryVerbosity
    _diameter: meters
    _weight: kilograms
    _moi: float
    _sim_color: Color8Bit = Color8Bit(Color.kOrange)
    _mechanism_position_config: MechanismPositionConfig = MechanismPositionConfig()
    _use_speedometer: bool = False
    _speedometer_max_velocity: radians_per_second

    def __init__(self, motor_controller: SmartMotorController = None) -> None:
        self._motor = motor_controller

    def clone(self) -> "FlyWheelConfig":
        new_config = FlyWheelConfig()
        new_config._motor = self._motor
        new_config._network_table_name = self._network_table_name
        new_config._min_velocity = self._min_velocity
        new_config._max_velocity = self._max_velocity
        new_config._telemetry_name = self._telemetry_name
        new_config._telemetry_verbosity = self._telemetry_verbosity
        new_config._diameter = self._diameter
        new_config._weight = self._weight
        new_config._moi = self._moi
        new_config._sim_color = self._sim_color
        new_config._mechanism_position_config = self._mechanism_position_config
        new_config._use_speedometer = self._use_speedometer
        new_config._speedometer_max_velocity = self._speedometer_max_velocity
        return new_config

    def with_smart_motor_controller(
        self, motor_controller: SmartMotorController
    ) -> "FlyWheelConfig":
        if self._motor:
            raise FlyWheelConfigurationException(
                "FlyWheel SmartMotorController already set!",
                "FlyWheel cannot be set",
                "withSmartMotorController(SmartMotorController)",
            )
        self._motor = motor_controller
        if self._moi:
            self.with_moi()
        return self

    def with_lower_soft_limit(self, speed: radians_per_second) -> "FlyWheelConfig":
        self._min_velocity = speed
        if not self._min_velocity:
            self._speedometer_max_velocity = self._max_velocity
        elif not self._max_velocity:
            self._speedometer_max_velocity = self._min_velocity
        elif self._min_velocity > self._max_velocity:
            self._speedometer_max_velocity = self._min_velocity
            temp = self._min_velocity
            self._min_velocity = self._max_velocity
            self._max_velocity = temp
        return self

    # TODO finish FlyWheelConfig
