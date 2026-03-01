from wpimath.units import radians_per_second, meters, kilograms, kilogram_square_meters, meters_per_second
from wpilib import Color, Color8Bit
from wpimath.geometry import Translation3d
from smartmechanismsystem.motorcontrollers.smartmotorcontroller import (
    SmartMotorController,
)
from smartmechanismsystem.motorcontrollers.smartmotorcontrollerconfig import SmartMotorControllerConfig
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
    _telemetry_verbosity: SmartMotorControllerConfig.TelemetryVerbosity
    _diameter: meters
    _weight: kilograms
    _moi: kilogram_square_meters
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

        if self._min_velocity > self._max_velocity:
            self._max_velocity, self._min_velocity = self._min_velocity, self._max_velocity
        self._speedometer_max_velocity = max(abs(self._max_velocity), abs(self._min_velocity))
        return self

    def with_upper_soft_limit(self, speed: radians_per_second) -> "FlyWheelConfig":
        self._max_velocity = speed

        if self._min_velocity > self._max_velocity:
            self._max_velocity, self._min_velocity = self._min_velocity, self._max_velocity
        self._speedometer_max_velocity = max(abs(self._max_velocity), abs(self._min_velocity))
        return self

    def with_soft_limit(self, low: radians_per_second, high: radians_per_second) -> "FlyWheelConfig":
        self._min_velocity = low
        self._max_velocity = high

        if self._min_velocity > self._max_velocity:
            self._max_velocity, self._min_velocity = self._min_velocity, self._max_velocity
        self._speedometer_max_velocity = max(abs(self._max_velocity), abs(self._min_velocity))
        return self
    
    def with_speedometer_simulation(self, max_velocity: radians_per_second = _speedometer_max_velocity) -> "FlyWheelConfig":
        if(not self._speedometer_max_velocity):
            raise FlyWheelConfigurationException(
                "Speedometer max velocity not set.",
                "Cannot use speedometer simulation!",
                "Set it with_speedometer_simulation(radians_per_second)",
            )
        self._use_speedometer = True
        self._speedometer_max_velocity = max_velocity
        return self

    def disable_speedometer_simulation(self) -> "FlyWheelConfig":
        self._use_speedometer = False
        return self
    
    def is_using_speedometer_simulation(self) -> bool:
        return self._use_speedometer
    
    def get_speedometer_max_velocity(self) -> radians_per_second:
        return self._speedometer_max_velocity
    
    def with_sim_color(self, color: Color8Bit) -> "FlyWheelConfig":
        self._sim_color = color
        return self
    
    def with_moment_of_inertia(self, moi: kilogram_square_meters) -> "FlyWheelConfig":
        if self._motor:
            self._motor.get_config().with_moment_of_inertia(moi)
        self._moi = moi
        return self
    
    def with_moment_of_inertia_from_length_and_mass(self, length: meters, mass: kilograms) -> "FlyWheelConfig":
        moi = 0.5 * mass * (length / 2) ** 2
        return self.with_moment_of_inertia(moi)
    
    def with_diameter(self, diameter: meters) -> "FlyWheelConfig":
        self._diameter = diameter
        return self
    
    def with_mass(self, mass: kilograms) -> "FlyWheelConfig":
        self._weight = mass
        return self
    
    def with_mechanism_position_config(self, config: MechanismPositionConfig) -> "FlyWheelConfig":
        self._mechanism_position_config = config
        return self
    
    def with_telemetry(self, name: str, verbosity: SmartMotorControllerConfig.TelemetryVerbosity, network_root = _network_table_name) -> "FlyWheelConfig":
        self._telemetry_name = name
        self._telemetry_verbosity = verbosity
        self._network_table_name = network_root
        return self
    
    def apply_config(self) -> bool:
        if not self._motor:
            raise FlyWheelConfigurationException(
                "SmartMotorController not set!",
                "FlyWheel cannot be configured",
                "apply_config()",
            )
        return self._motor.apply_config(self._motor.get_config())
    
    def get_diameter(self) -> meters:
        return self._diameter

    def get_moment_of_inertia(self) -> kilogram_square_meters:
        if self._moi:
            return self._moi
        elif(self._diameter and self._weight):
            return 0.5 * self._weight * (self._diameter / 2) ** 2
        else:
            raise FlyWheelConfigurationException(
                "FlyWheel diameter and weight or MOI must be set!",
                "Cannot get the MOI!",
                "withDiameter(Distance).withMass(Mass) OR FlyWheelConfig.withMOI()"
            )
    
    def get_telemetry_verbosity(self) -> SmartMotorControllerConfig.TelemetryVerbosity:
        return self._telemetry_verbosity
    
    def get_upper_soft_limit(self) -> radians_per_second:
        return self._max_velocity
    
    def get_lower_soft_limit(self) -> radians_per_second:
        return self._min_velocity
    
    def get_telemetry_name(self) -> str:
        return self._telemetry_name
    
    def get_motor(self) -> SmartMotorController:
        if self._motor:
            return self._motor
        raise FlyWheelConfigurationException(
            "SmartMotorController not set!",
            "FlyWheel cannot be configured",
            "get_motor_controller()",
        )
    
    def get_sim_color(self) -> Color8Bit:
        return self._sim_color
    
    def get_mechanism_position_config(self) -> MechanismPositionConfig:
        return self._mechanism_position_config
    
    def get_circumference(self) -> meters:
        if not self._diameter:
            raise FlyWheelConfigurationException(
                "Flywheel diameter is empty",
                "Cannot run speed without diameter.",
                "get_circumference()",
            )
        from math import pi
        return self._diameter * pi
    
    def get_linear_velocity(self, velocity: radians_per_second) -> meters_per_second:
        from math import pi
        return self.get_circumference() * velocity / (2 * pi)
    
    def get_angular_velocity(self, velocity: meters_per_second) -> radians_per_second:
        from math import pi
        return velocity * (2 * pi) / self.get_circumference()