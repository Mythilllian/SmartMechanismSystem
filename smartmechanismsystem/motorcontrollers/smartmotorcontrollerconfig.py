# pyright: reportAttributeAccessIssue=false

from math import pi
from commands2 import Subsystem
from wpimath.controller import SimpleMotorFeedforwardMeters, ElevatorFeedforward, ArmFeedforward
from wpimath.trajectory import TrapezoidProfile, ExponentialProfileMeterVolts
from wpimath.controller import PIDController
from wpimath.system.plant import DCMotor, LinearSystemId
from wpimath.units import meters, seconds, volts, radians, celsius, kilogram_square_meters, kilograms, amperes, hertz, meters_per_second, radians_per_second, meters_per_second_squared, radians_per_second_squared
from wpilib import RobotBase, reportWarning
# import hal
# from hal import tResourceType
from enum import Enum, auto

from smartmechanismsystem.exceptions.exceptions import SmartMotorControllerConfigurationException
from smartmechanismsystem.motorcontrollers.smartmotorcontroller import SmartMotorController
from smartmechanismsystem.gearing.mechanismgearing import MechanismGearing
from smartmechanismsystem.math.lqr import LQRController
from smartmechanismsystem.telemetry import SmartMotorControllerTelemetryConfig

class SmartMotorControllerConfig:
    class BasicOptions(Enum):
        resetPreviousConfig = auto()
        ControlMode = auto()
        FeedbackSynchronizationThreshold = auto()
        ClosedLoopControllerMaximumVoltage = auto()
        StartingPosition = auto()
        EncoderInverted = auto()
        MotorInverted = auto()
        TemperatureCutoff = auto()
        DiscontinuityPoint = auto()
        ClosedLoopTolerance = auto()
        UpperLimit = auto()
        LowerLimit = auto()
        IdleMode = auto()
        VoltageCompensation = auto()
        Followers = auto()
        LooselyCoupledFollowers = auto()
        StatorCurrentLimit = auto()
        SupplyCurrentLimit = auto()
        ClosedLoopRampRate = auto()
        OpenLoopRampRate = auto()
        ExternalEncoder = auto()
        Gearing = auto()
        ClosedLoopControlPeriod = auto()
        SimpleFeedforward = auto()
        ArmFeedforward = auto()
        ElevatorFeedforward = auto()
        LQR = auto()
        PID = auto()
        TrapezoidProfile = auto()
        ExponentialProfile = auto()

    class ExternalEncoderOptions(Enum):
        ZeroOffset = auto()
        UseExternalFeedbackEncoder = auto()
        ExternalGearing = auto()
        ExternalEncoderInverted = auto()

    class SmartMotorControllerOptions(Enum):
        MOTOR_INVERTED = auto()
        SUPPLY_CURRENT_LIMIT = auto()
        STATOR_CURRENT_LIMIT = auto()

    class TelemetryVerbosity(Enum):
        LOW = auto()
        MEDIUM = auto()
        HIGH = auto()
    
    class MotorMode(Enum):
        BRAKE = auto()
        COAST = auto()
    
    class ControlMode(Enum):
        OPEN_LOOP = auto()
        CLOSED_LOOP = auto()
    
    _reset_previous_config: bool = True
    _vendor_config: object
    _subsystem: Subsystem
    _missing_options: list[SmartMotorControllerOptions] = list(SmartMotorControllerOptions)
    _basic_options: set[BasicOptions] = set(BasicOptions)
    _external_encoder_options: set[ExternalEncoderOptions] = set(ExternalEncoderOptions)
    _external_encoder: object
    _external_encoder_inverted: bool = False
    _followers: list[tuple[object, bool]]
    _simple_feedforward: SimpleMotorFeedforwardMeters
    _elevator_feedforward: ElevatorFeedforward
    _arm_feedforward: ArmFeedforward
    _sim_simple_feedforward: SimpleMotorFeedforwardMeters
    _sim_elevator_feedforward: ElevatorFeedforward
    _sim_arm_feedforward: ArmFeedforward
    _exponential_profile: ExponentialProfileMeterVolts.Constraints
    _trapezoid_profile: TrapezoidProfile.Constraints
    _sim_exponential_profile: ExponentialProfileMeterVolts.Constraints
    _pid: PIDController
    _lqr: LQRController
    _sim_pid: PIDController
    _sim_lqr: LQRController
    _gearing: MechanismGearing
    _external_encoder_gearing: MechanismGearing = MechanismGearing.from_reduction_ratios(1)
    _mechanism_circumference: meters
    _control_period: seconds
    _open_loop_ramp_rate: seconds
    _closed_loop_ramp_rate: seconds
    _stator_stall_current_limit: amperes
    _supply_stall_current_limit: amperes
    _voltage_compensation: volts
    _idle_mode: MotorMode
    _mechanism_lower_limit: radians
    _mechanism_upper_limit: radians
    _telemetry_name: str
    _verbosity: TelemetryVerbosity
    _specified_telemetry_config: SmartMotorControllerTelemetryConfig
    _zero_offset: radians
    _temperature_cutoff: celsius
    _encoder_inverted: bool = False
    _motor_inverted: bool = False
    _use_external_encoder: bool = True
    _starting_position: radians
    _closed_loop_controller_maximum_voltage: volts
    _feedback_synchronization_threshold: radians
    _motor_controller_mode: ControlMode = ControlMode.CLOSED_LOOP
    _max_discontinuity_point: radians
    _min_discontinuity_point: radians
    _closed_loop_tolerance: radians
    _moi: kilogram_square_meters = 0.02
    _loosely_coupled_followers: list[SmartMotorController]
    _linear_closed_loop_controller: bool = False
    _velocity_trapezoidal_profile: bool = False

    def __init__(self, 
                 subsystem: Subsystem = None
                #  , report: bool = True
                 ) -> None:
        # if report:
        #     hal.report(1, 1)
        self._subsystem = subsystem

    def clone(self) -> "SmartMotorControllerConfig":
        new_config = SmartMotorControllerConfig(self._subsystem
                                                # , False
                                                )
        new_config._reset_previous_config = self._reset_previous_config
        new_config._vendor_config = self._vendor_config
        new_config._missing_options = self._missing_options.copy()
        new_config._basic_options = self._basic_options.copy()
        new_config._external_encoder_options = self._external_encoder_options.copy()
        new_config._external_encoder = self._external_encoder
        new_config._external_encoder_inverted = self._external_encoder_inverted
        new_config._followers = self._followers
        new_config._simple_feedforward = self._simple_feedforward
        new_config._elevator_feedforward = self._elevator_feedforward
        new_config._arm_feedforward = self._arm_feedforward
        new_config._sim_simple_feedforward = self._sim_simple_feedforward
        new_config._sim_elevator_feedforward = self._sim_elevator_feedforward
        new_config._sim_arm_feedforward = self._sim_arm_feedforward
        new_config._exponential_profile = self._exponential_profile
        new_config._trapezoid_profile = self._trapezoid_profile
        new_config._sim_exponential_profile = self._sim_exponential_profile
        new_config._pid = self._pid
        new_config._lqr = self._lqr
        new_config._sim_pid = self._sim_pid
        new_config._sim_lqr = self._sim_lqr
        new_config._gearing = self._gearing
        new_config._external_encoder_gearing = self._external_encoder_gearing
        new_config._mechanism_circumference = self._mechanism_circumference
        new_config._control_period = self._control_period
        new_config._open_loop_ramp_rate = self._open_loop_ramp_rate
        new_config._closed_loop_ramp_rate = self._closed_loop_ramp_rate
        new_config._stator_stall_current_limit = self._stator_stall_current_limit
        new_config._supply_stall_current_limit = self._supply_stall_current_limit
        new_config._voltage_compensation = self._voltage_compensation
        new_config._idle_mode = self._idle_mode
        new_config._mechanism_lower_limit = self._mechanism_lower_limit
        new_config._mechanism_upper_limit = self._mechanism_upper_limit
        new_config._telemetry_name = self._telemetry_name
        new_config._verbosity = self._verbosity
        new_config._specified_telemetry_config = self._specified_telemetry_config
        new_config._zero_offset = self._zero_offset
        new_config._temperature_cutoff = self._temperature_cutoff
        new_config._encoder_inverted = self._encoder_inverted
        new_config._motor_inverted = self._motor_inverted
        new_config._use_external_encoder = self._use_external_encoder
        new_config._starting_position = self._starting_position
        new_config._closed_loop_controller_maximum_voltage = self._closed_loop_controller_maximum_voltage
        new_config._feedback_synchronization_threshold = self._feedback_synchronization_threshold
        new_config._motor_controller_mode = self._motor_controller_mode
        new_config._max_discontinuity_point = self._max_discontinuity_point
        new_config._min_discontinuity_point = self._min_discontinuity_point
        new_config._closed_loop_tolerance = self._closed_loop_tolerance
        new_config._moi = self._moi
        new_config._loosely_coupled_followers = self._loosely_coupled_followers.copy()
        new_config._linear_closed_loop_controller = self._linear_closed_loop_controller
        new_config._velocity_trapezoidal_profile = self._velocity_trapezoidal_profile
        return new_config
    
    def with_vendor_config(self, vendor_config: object) -> "SmartMotorControllerConfig":
        self._vendor_config = vendor_config
        return self
    
    def with_subsystem(self, subsystem: Subsystem) -> "SmartMotorControllerConfig":
        if self._subsystem:
            raise SmartMotorControllerConfigurationException("Subsystem has already been set", 
                                                             "Cannot set subsystem", 
                                                             "with_subsystem(Subsystem) should only be called once"
                                                             )
        self._subsystem = subsystem
        return self
    
    def with_external_encoder_inverted(self, inverted: bool) -> "SmartMotorControllerConfig":
        self._external_encoder_inverted = inverted
        return self
    
    def with_control_mode(self, mode: ControlMode) -> "SmartMotorControllerConfig":
        self._motor_controller_mode = mode
        return self
    
    def with_feedback_synchronization_threshold(self, threshold: radians) -> "SmartMotorControllerConfig":
        if self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Auto-synchronization is unavailable when using distance based mechanisms",
                                                              "Cannot set synchronization threshold.",
                                                              "with_mechanism_circumference(meters) should be removed.")
        self._feedback_synchronization_threshold = threshold
        return self
    
    def with_closed_loop_controller_maximum_voltage(self, voltage: volts) -> "SmartMotorControllerConfig":
        self._closed_loop_controller_maximum_voltage = voltage
        return self
    
    def with_starting_position(self, position: radians) -> "SmartMotorControllerConfig":
        self._starting_position = position
        return self
    
    def with_use_external_feedback_encoder(self, use_external: bool) -> "SmartMotorControllerConfig":
        self._use_external_encoder = use_external
        return self
    
    def with_encoder_inverted(self, inverted: bool) -> "SmartMotorControllerConfig":
        self._encoder_inverted = inverted
        return self
    
    def with_motor_inverted(self, inverted: bool) -> "SmartMotorControllerConfig":
        self._motor_inverted = inverted
        return self

    def with_reset_previous_config(self, reset: bool) -> "SmartMotorControllerConfig":
        self._reset_previous_config = reset
        return self
    
    def with_temperature_cutoff(self, cutoff: celsius) -> "SmartMotorControllerConfig":
        self._temperature_cutoff = cutoff
        return self
    
    def with_external_encoder_zero_offset(self, offset: radians) -> "SmartMotorControllerConfig":
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot set zero offset.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        self._zero_offset = offset
        return self
    
    def with_continuous_wrapping(self, bottom: radians, top: radians) -> "SmartMotorControllerConfig":
        if self._mechanism_upper_limit or self._mechanism_lower_limit:
            raise SmartMotorControllerConfigurationException("Soft limits set while configuring continuous wrapping",
                                                           "Cannot set continuous wrapping",
                                                           "with_soft_limit(radians, radians) should be removed")
        if self._linear_closed_loop_controller:
            raise SmartMotorControllerConfigurationException("Distance based mechanism used with continuous wrapping",
                                                           "Cannot set continuous wrapping",
                                                           "with_mechanism_circumference(meters) should be removed")
        if not self._pid:
            raise SmartMotorControllerConfigurationException("No PID controller used",
                                                           "Cannot set continuous wrapping!",
                                                           "with_closed_loop_controller() should be called first.")
        else:
            self._pid.enableContinuousInput(bottom, top)
        
        self._max_discontinuity_point = top
        self._min_discontinuity_point = bottom
        return self

    def with_closed_loop_tolerance_angle(self, tolerance: radians) -> "SmartMotorControllerConfig":
        self._closed_loop_tolerance = tolerance
        if tolerance:
            if not self._pid:
                raise SmartMotorControllerConfigurationException("No PID controller used",
                                                                "Cannot set tolerance!",
                                                                "with_closed_loop_controller() should be called first.")
            else:
                self._pid.setTolerance(self.get_closed_loop_tolerance() if self.get_closed_loop_tolerance() else tolerance) #TODO: convert to rotations?
        return self
    
    def with_closed_loop_tolerance_distance(self, tolerance: meters) -> "SmartMotorControllerConfig":
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Linear closed loop controller used with distance tolerance.",
                                                           "Closed loop tolerance cannot be set.",
                                                           "with_linear_closed_loop_controller(True)")
        if tolerance:
            tolerance_angle = self.convert_distance_to_mechanism(tolerance)
            self._closed_loop_tolerance = tolerance_angle
            if not self._pid:
                raise SmartMotorControllerConfigurationException("No PID controller used",
                                                                "Cannot set tolerance!",
                                                                "with_closed_loop_controller() should be called first.")
            else:
                self._pid.setTolerance(self.convert_angle_from_mechanism(self.get_closed_loop_tolerance() if self.get_closed_loop_tolerance() else tolerance_angle))
        return self

    def get_closed_loop_tolerance(self) -> radians:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ClosedLoopTolerance)
        return self._closed_loop_tolerance

    def with_telemetry(self, verbosity: TelemetryVerbosity, telemetry_name: str = "motor"):
        self._telemetry_name = telemetry_name
        self._verbosity = verbosity
        return self

    def with_telemetry_config(self, telemetry_config: SmartMotorControllerTelemetryConfig, telemetry_name: str = "motor", verbosity: TelemetryVerbosity = TelemetryVerbosity.HIGH):
        self._telemetry_name = telemetry_name
        self._verbosity = verbosity
        self._specified_telemetry_config = telemetry_config
        return self
    
    def get_smart_controller_telemetry_config(self) -> SmartMotorControllerTelemetryConfig:
        return self._specified_telemetry_config
    
    def get_stator_stall_current_limit(self) -> amperes:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.StatorCurrentLimit)
        return self._stator_stall_current_limit
    
    def with_soft_limit_distance(self, low: meters, high: meters):
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot set soft limits.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        self._mechanism_lower_limit = low / self._mechanism_circumference * 2 * pi
        self._mechanism_upper_limit = high / self._mechanism_circumference * 2 * pi
        return self
    
    def with_moment_of_inertia_from_length_and_mass(self, length: meters, mass: kilograms):
        if not length or not mass:
            raise SmartMotorControllerConfigurationException("Length or Weight must be set!",
                                                           "MOI is necessary for standalone SmartMotorController simulation!",
                                                           "with_moment_of_inertia_from_length_and_mass(meters, kilograms) should be called with nonzero values.")
        else:
            moi = mass * length * length / 3
            self._moi = moi
        return self
    
    def with_moment_of_inertia(self, moi: kilogram_square_meters):
        if not moi:
            raise SmartMotorControllerConfigurationException("MOI cannot be zero!",
                                                           "MOI is necessary for standalone SmartMotorController simulation!",
                                                           "with_moment_of_inertia(kilogram_square_meters) should be called with a nonzero value.")
        self._moi = moi
        return self
    
    def with_soft_limit_angle(self, low: radians, high: radians):
        self._mechanism_lower_limit = low
        self._mechanism_upper_limit = high
        return self
    
    def get_supply_stall_current_limit(self) -> amperes:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.SupplyCurrentLimit)
        return self._supply_stall_current_limit
    
    def get_voltage_compensation(self) -> volts:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.VoltageCompensation)
        return self._voltage_compensation
    
    def get_idle_mode(self) -> MotorMode:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.IdleMode)
        return self._idle_mode
    
    def get_moment_of_inertia(self) -> kilogram_square_meters:
        return self._moi
    
    def get_mechanism_lower_limit(self) -> radians:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.LowerLimit)
        return self._mechanism_lower_limit
    
    def get_mechanism_upper_limit(self) -> radians:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.UpperLimit)
        return self._mechanism_upper_limit
    
    def with_idle_mode(self, mode: MotorMode) -> "SmartMotorControllerConfig":
        self._idle_mode = mode
        return self
    
    def with_voltage_compensation(self, voltage: volts) -> "SmartMotorControllerConfig":
        self._voltage_compensation = voltage
        return self
    
    def with_followers(self, *followers: tuple[object, bool]) -> "SmartMotorControllerConfig":
        self._followers = list(followers)
        return self
    
    def with_loosely_coupled_followers(self, *followers: SmartMotorController) -> "SmartMotorControllerConfig":
        self._loosely_coupled_followers = list(followers)
        return self

    def clear_followers(self) -> "SmartMotorControllerConfig":
        self._followers = []
        # self._loosely_coupled_followers = []
        return self

    def with_stator_current_limit(self, stall_current: amperes) -> "SmartMotorControllerConfig":
        self._stator_stall_current_limit = stall_current
        return self

    def with_supply_current_limit(self, stall_current: amperes) -> "SmartMotorControllerConfig":
        self._supply_stall_current_limit = stall_current
        return self
    
    def with_closed_loop_ramp_rate(self, ramp_rate: seconds) -> "SmartMotorControllerConfig":
        self._closed_loop_ramp_rate = ramp_rate
        return self
    
    def with_open_loop_ramp_rate(self, ramp_rate: seconds) -> "SmartMotorControllerConfig":
        self._open_loop_ramp_rate = ramp_rate
        return self
    
    def with_external_encoder(self, encoder: object, gearing: MechanismGearing = _external_encoder_gearing) -> "SmartMotorControllerConfig":
        self._external_encoder = encoder
        self._external_encoder_gearing = gearing
        return self

    def get_followers(self) -> list[tuple[object, bool]]:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.Followers)
        return self._followers
    
    def with_gearing(self, gearing: MechanismGearing) -> "SmartMotorControllerConfig":
        self._gearing = gearing
        return self

    def with_gearing_from_reduction_ratio(self, reduction_ratio: float) -> "SmartMotorControllerConfig":
        self._gearing = MechanismGearing.from_reduction_ratios(reduction_ratio)
        return self
    
    def with_mechanism_circumference(self, circumference: meters) -> "SmartMotorControllerConfig":
        self._mechanism_circumference = circumference
        return self

    def with_wheel_diameter(self, diameter: meters) -> "SmartMotorControllerConfig":
        circumference = diameter * pi
        self._mechanism_circumference = circumference
        return self

    def get_mechanism_circumference(self) -> meters:
        return self._mechanism_circumference
    
    def get_linear_closed_loop_controller_use(self) -> bool:
        return self._linear_closed_loop_controller and self._mechanism_circumference
    
    def with_closed_loop_control_period(self, period: seconds) -> "SmartMotorControllerConfig":
        self._control_period = period
        return self

    def with_closed_loop_control_period_from_frequency(self, frequency: hertz) -> "SmartMotorControllerConfig":
        self._control_period = 1 / frequency
        return self
    
    def get_arm_feedforward(self) -> ArmFeedforward:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ArmFeedforward)
        if RobotBase.isSimulation() and self._sim_arm_feedforward:
            return self._sim_arm_feedforward
        return self._arm_feedforward
    
    def with_sim_arm_feedforward(self, arm_feedforward: ArmFeedforward) -> "SmartMotorControllerConfig":
        if not arm_feedforward:
            self._sim_arm_feedforward = None
        else:
            self._sim_elevator_feedforward = None
            self._sim_simple_feedforward = None
            self._sim_arm_feedforward = arm_feedforward
        return self

    def with_arm_feedforward(self, arm_feedforward: ArmFeedforward) -> "SmartMotorControllerConfig":
        if not arm_feedforward:
            self._arm_feedforward = None
        else:
            self._elevator_feedforward = None
            self._simple_feedforward = None
            self._arm_feedforward = arm_feedforward
        return self
    
    def get_elevator_feedforward(self) -> ElevatorFeedforward:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ElevatorFeedforward)
        if RobotBase.isSimulation() and self._sim_elevator_feedforward:
            return self._sim_elevator_feedforward
        return self._elevator_feedforward
    
    def with_sim_elevator_feedforward(self, elevator_feedforward: ElevatorFeedforward) -> "SmartMotorControllerConfig":
        if not elevator_feedforward:
            self._sim_elevator_feedforward = None
        else:
            self._sim_arm_feedforward = None
            self._sim_simple_feedforward = None
            self._sim_elevator_feedforward = elevator_feedforward
        return self

    def with_elevator_feedforward(self, elevator_feedforward: ElevatorFeedforward) -> "SmartMotorControllerConfig":
        if not elevator_feedforward:
            self._elevator_feedforward = None
        else:
            self._arm_feedforward = None
            self._simple_feedforward = None
            self._elevator_feedforward = elevator_feedforward
        return self
    
    def get_simple_feedforward(self) -> SimpleMotorFeedforwardMeters:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.SimpleFeedforward)
        if RobotBase.isSimulation() and self._sim_simple_feedforward:
            return self._sim_simple_feedforward
        return self._simple_feedforward
    
    def with_sim_simple_feedforward(self, simple_feedforward: SimpleMotorFeedforwardMeters) -> "SmartMotorControllerConfig":
        if not simple_feedforward:
            self._sim_simple_feedforward = None
        else:
            self._sim_arm_feedforward = None
            self._sim_elevator_feedforward = None
            self._sim_simple_feedforward = simple_feedforward
        return self

    def with_simple_feedforward(self, simple_feedforward: SimpleMotorFeedforwardMeters) -> "SmartMotorControllerConfig":
        if not simple_feedforward:
            self._simple_feedforward = None
        else:
            self._arm_feedforward = None
            self._elevator_feedforward = None
            self._simple_feedforward = simple_feedforward
        return self
    
    def with_sim_closed_loop_pid_controller_from_constants(self, kP: float, kI: float, kD: float, max_velocity: meters_per_second | radians_per_second, max_acceleration: meters_per_second_squared | radians_per_second_squared) -> "SmartMotorControllerConfig":
        self._sim_pid = PIDController(kP, kI, kD)
        self._sim_lqr = None
        if max_velocity and max_acceleration:
            self._sim_exponential_profile = None
            self._sim_trapezoid_profile = TrapezoidProfile.Constraints(max_velocity, max_acceleration)
        return self

    def with_sim_closed_loop_lqr_controller(self, lqr_controller: LQRController) -> "SmartMotorControllerConfig":
        self._sim_lqr = lqr_controller
        self._sim_pid = None
        return self

    def with_sim_closed_loop_pid_controller(self, controller: PIDController) -> "SmartMotorControllerConfig":
        self._sim_pid = controller
        self._sim_lqr = None
        return self

    def with_trapezoidal_profile(self, profile: TrapezoidProfile.Constraints) -> "SmartMotorControllerConfig":
        reportWarning("Trapezoidal profile will be given radians/s and radians/s^2 for rotational closed loop controllers.", True)
        reportWarning("Trapezoidal profile will be given meters/s and meters/s^2 for linear closed loop controllers.", True)
        self._trapezoid_profile = profile
        self._exponential_profile = None
        return self
    
    def with_trapezoidal_profile_from_constants(self, max_velocity: meters_per_second | radians_per_second, max_acceleration: meters_per_second_squared | radians_per_second_squared) -> "SmartMotorControllerConfig":
        self._linear_closed_loop_controller = True
        self._trapezoid_profile = TrapezoidProfile.Constraints(max_velocity, max_acceleration)
        self._exponential_profile = None
        return self
    
    def with_exponential_profile(self, profile: ExponentialProfileMeterVolts.Constraints) -> "SmartMotorControllerConfig":
        reportWarning("Exponential profile will be given radians/s and radians/s^2 for rotational closed loop controllers.", True)
        reportWarning("Exponential profile will be given meters/s and meters/s^2 for linear closed loop controllers.", True)
        
        self._exponential_profile = profile
        self._trapezoid_profile = None
        return self

    def with_exponential_profile_arm(self, max_volts: volts, motor: DCMotor, moi: kilogram_square_meters) -> "SmartMotorControllerConfig":        
        self.moi = moi
        sysid = LinearSystemId.singleJointedArmSystem(motor, moi, self._gearing.get_mechanism_to_rotor_ratio())

        A = sysid.A(0,0) # radians
        B = sysid.B(0,0) # radians
        kV = -A / B
        kA = 1 / B
        self._trapezoid_profile = None
        self._exponential_profile = ExponentialProfileMeterVolts.Constraints.fromCharacteristics(max_volts, kV, kA)
        return self

    def with_exponential_profile_elevator(self, max_volts: volts, motor: DCMotor, mass: kilograms, drum_radius: meters) -> "SmartMotorControllerConfig":
        sysid = LinearSystemId.elevatorSystem(motor, mass, drum_radius, self._gearing.get_mechanism_to_rotor_ratio())
        self._circumference = 2 * pi * drum_radius
        
        A = sysid.A(0,0) # meters
        B = sysid.B(0,0) # meters
        kV = -A / B
        kA = 1 / B
        self._trapezoid_profile = None
        self._exponential_profile = ExponentialProfileMeterVolts.Constraints.fromCharacteristics(max_volts, kV, kA)
        self._linear_closed_loop_controller = True
        return self

    def with_exponential_profile_generic(self, max_volts: volts, max_velocity: radians_per_second, max_acceleration: radians_per_second_squared) -> "SmartMotorControllerConfig":
        self._trapezoid_profile = None
        self._exponential_profile = ExponentialProfileMeterVolts.Constraints.fromStateSpace(max_volts, max_volts / (max_velocity/(2*pi)) , max_volts / (max_acceleration/(2*pi)))
        return self

    def with_closed_loop_lqr_controller(self, controller: LQRController) -> "SmartMotorControllerConfig":
        self._lqr = controller
        self._pid = None
        return self
    
    def with_closed_loop_pid_controller(self, controller: PIDController) -> "SmartMotorControllerConfig":   
        self._pid = controller
        self._lqr = None
        return self
    
    def with_closed_loop_pid_controller_from_constants(self, kP: float, kI: float, kD: float, max_velocity: meters_per_second | radians_per_second, max_acceleration: meters_per_second_squared | radians_per_second_squared) -> "SmartMotorControllerConfig":
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Closed loop controller cannot be created.",
                                                           "with_mechanism_circumference(meters)")
        self._pid = PIDController(kP, kI, kD)
        self._lqr = None
        return self.with_trapezoidal_profile_from_constants(max_velocity, max_acceleration)
    
    def get_lqr_closed_loop_controller(self) -> LQRController:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.LQR)
        if RobotBase.isSimulation() and self._sim_lqr:
            return self._sim_lqr
        return self._lqr
    
    def get_pid_closed_loop_controller(self) -> PIDController:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.PID)
        if RobotBase.isSimulation() and self._sim_pid:
            return self._sim_pid
        return self._pid

    def get_exponential_profile(self) -> ExponentialProfileMeterVolts.Constraints:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ExponentialProfile)
        if RobotBase.isSimulation() and self._sim_exponential_profile:
            return self._sim_exponential_profile
        return self._exponential_profile
    
    def get_trapezoidal_profile(self) -> TrapezoidProfile.Constraints:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.TrapezoidProfile)
        if RobotBase.isSimulation() and self._sim_trapezoid_profile:
            return self._sim_trapezoid_profile
        return self._trapezoid_profile
    
    def with_sim_feedforward(self, simple_feedforward: SimpleMotorFeedforwardMeters) -> "SmartMotorControllerConfig":
        return self.with_sim_simple_feedforward(simple_feedforward)

    def with_linear_closed_loop_controller(self, use_linear: bool = True) -> "SmartMotorControllerConfig":
        self._linear_closed_loop_controller = use_linear
        return self
    
    def with_velocity_trapezoidal_profile(self, use_velocity: bool = True) -> "SmartMotorControllerConfig":
        self._velocity_trapezoidal_profile = use_velocity
        return self

    def with_feedforward(self, simple_feedforward: SimpleMotorFeedforwardMeters) -> "SmartMotorControllerConfig":
        return self.with_simple_feedforward(simple_feedforward)
    
    def get_closed_loop_control_period(self) -> seconds:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ClosedLoopControlPeriod)
        return self._control_period
    
    def get_gearing(self) -> MechanismGearing:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.Gearing)
        return self._gearing

    def get_external_encoder(self) -> object:
        self._external_encoder_options.remove(SmartMotorControllerConfig.ExternalEncoderOptions.ExternalGearing)
        return self._external_encoder
    
    def get_open_loop_ramp_rate(self) -> seconds:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.OpenLoopRampRate)
        return self._open_loop_ramp_rate
    
    def get_closed_loop_ramp_rate(self) -> seconds:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ClosedLoopRampRate)
        return self._closed_loop_ramp_rate

    def get_verbosity(self) -> TelemetryVerbosity:
        return self._verbosity

    def get_telemetry_name(self) -> str:
        return self._telemetry_name
    
    def get_subsystem(self) -> Subsystem:
        if not self._subsystem:
            raise SmartMotorControllerConfigurationException("Subsystem is undefined",
                                                             "Subsystem cannot be created",
                                                             "with_subsystem(Subsystem)")
        return self._subsystem
    
    def convert_jerk_to_mechanism(self, jerk: float) -> float:
        """
        :param jerk: Linear jerk to convert. (m/s^3)
        :return: Equivalent angular jerk. (rad/s^3)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert to mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return jerk * 2 * pi / self._mechanism_circumference
    
    def convert_jerk_from_mechanism(self, jerk: float) -> float:
        """
        :param mechanism_jerk: Angular jerk to convert. (rad/s^3)
        :return: Equivalent linear jerk. (m/s^3)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert from mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return jerk * self._mechanism_circumference / (2 * pi)
    
    def convert_velocity_to_mechanism(self, velocity: meters_per_second) -> radians_per_second:
        """
        :param velocity: Linear velocity to convert. (m/s)
        :return: Equivalent angular velocity. (rad/s)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert to mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return velocity * 2 * pi / self._mechanism_circumference
    
    def convert_velocity_from_mechanism(self, velocity: radians_per_second) -> meters_per_second:
        """
        :param mechanism_velocity: Angular velocity to convert. (rad/s)
        :return: Equivalent linear velocity. (m/s)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert from mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return velocity * self._mechanism_circumference / (2 * pi)

    def convert_acceleration_to_mechanism(self, acceleration: meters_per_second_squared) -> radians_per_second_squared:
        """
        :param acceleration: Linear acceleration to convert. (m/s^2)
        :return: Equivalent angular acceleration. (rad/s^2)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert to mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return acceleration * 2 * pi / self._mechanism_circumference
    
    def convert_acceleration_from_mechanism(self, acceleration: radians_per_second_squared) -> meters_per_second_squared:
        """
        :param mechanism_acceleration: Angular acceleration to convert. (rad/s^2)
        :return: Equivalent linear acceleration. (m/s^2)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert from mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return acceleration * self._mechanism_circumference / (2 * pi)
    
    def convert_distance_to_mechanism(self, position: meters) -> radians:
        """
        :param position: Linear position to convert. (m)
        :return: Equivalent angular position. (rad)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert to mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return position * 2 * pi / self._mechanism_circumference
    
    def convert_angle_from_mechanism(self, position: radians) -> meters:
        """
        :param mechanism_position: Angular position to convert. (rad)
        :return: Equivalent linear position. (m)
        """
        if not self._mechanism_circumference:
            raise SmartMotorControllerConfigurationException("Mechanism circumference is undefined",
                                                           "Cannot convert from mechanism units.",
                                                           "with_mechanism_circumference(meters) should be set first.")
        return position * self._mechanism_circumference / (2 * pi)
    
    def get_zero_offset(self) -> radians:
        self._external_encoder_options.remove(SmartMotorControllerConfig.ExternalEncoderOptions.ZeroOffset)
        return self._zero_offset
    
    def get_temperature_cutoff(self) -> celsius:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.TemperatureCutoff)
        return self._temperature_cutoff
    
    def get_encoder_inverted(self) -> bool:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.EncoderInverted)
        return self._encoder_inverted

    def get_motor_inverted(self) -> bool:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.MotorInverted)
        if RobotBase.isSimulation():
            return False
        return self._motor_inverted
    
    def get_use_external_feedback(self) -> bool:
        self._external_encoder_options.remove(SmartMotorControllerConfig.ExternalEncoderOptions.UseExternalFeedbackEncoder)
        return self._use_external_encoder
    
    def get_starting_position(self) -> radians:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.StartingPosition)
        return self._starting_position

    def get_closed_loop_controller_maximum_voltage(self) -> volts:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ClosedLoopControllerMaximumVoltage)
        return self._closed_loop_controller_maximum_voltage
    
    def get_feedback_synchronization_threshold(self) -> radians:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.FeedbackSynchronizationThreshold)
        return self._feedback_synchronization_threshold
    
    def get_motor_controller_mode(self) -> ControlMode:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.MotorControllerMode)
        return self._motor_controller_mode
    
    def get_external_encoder_gearing(self) -> MechanismGearing:
        self._external_encoder_options.remove(SmartMotorControllerConfig.ExternalEncoderOptions.ExternalGearing)
        return self._external_encoder_gearing
    
    def with_external_encoder_gearing(self, gearing: MechanismGearing) -> "SmartMotorControllerConfig":
        if gearing.get_rotor_to_mechanism_ratio() > 1:
            reportWarning("[IMPORTANT] Your gearing's rotor to mechanism ratio exceeds 1, and the external encoder will exceed the maximum reading, which WILL result in multiple angle's being read as the same 'angle.\n\tIgnore this warning IF your mechanism will never travel outside of the slice you are reading, adjust the offset accordingly.\n\tYou have been warned!", True)
        self._external_encoder_gearing = gearing
        return self
    
    def with_external_encoder_gearing_from_reduction_ratio(self, reduction_ratio: float) -> "SmartMotorControllerConfig":
        return self.with_external_encoder_gearing(MechanismGearing.from_reduction_ratios(reduction_ratio))
    
    def get_max_discontinuity_point(self) -> radians:
        if self._max_discontinuity_point and self._min_discontinuity_point and self._min_discontinuity_point != self._max_discontinuity_point - 2 * pi:
            raise SmartMotorControllerConfigurationException("Bounds are not correct!",
                                                           "Cannot get the discontinuity point.",
                                                           "withContinuousWrapping(Rotations.of(" +
                                                           str(self._max_discontinuity_point-2*pi) + "),Rotations.of(" +
                                                           str(self._max_discontinuity_point) + ")) instead ")
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.DiscontinuityPoint)
        return self._max_discontinuity_point
    
    def get_min_discontinuity_point(self) -> radians:
        if self._max_discontinuity_point and self._min_discontinuity_point and self._min_discontinuity_point != self._max_discontinuity_point - 2 * pi:
            raise SmartMotorControllerConfigurationException("Bounds are not correct!",
                                                           "Cannot get the discontinuity point.",
                                                           "withContinuousWrapping(Rotations.of(" +
                                                           str(self._max_discontinuity_point-2*pi) + "),Rotations.of(" +
                                                           str(self._max_discontinuity_point) + ")) instead ")
        # self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.DiscontinuityPoint)
        return self._min_discontinuity_point

    def get_loosely_coupled_followers(self) -> list[SmartMotorController]:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.LooselyCoupledFollowers)
        return self._loosely_coupled_followers
    
    def get_velocity_trapezoidal_profile_in_use(self) -> bool:
        return self._velocity_trapezoidal_profile
    
    def get_vendor_config(self) -> object:
        return self._vendor_config

    def get_reset_previous_config(self) -> bool:
        self._basic_options.remove(SmartMotorControllerConfig.BasicOptions.ResetPreviousConfig)
        return self._reset_previous_config
    
    def reset_validation_check(self) -> None:
        self._basic_options = set(SmartMotorControllerConfig.BasicOptions)
        self._external_encoder_options = set(SmartMotorControllerConfig.ExternalEncoderOptions)

    def validate_basic_options(self) -> None:
        if not self._basic_options:
            raise SmartMotorControllerConfigurationException("Basic options are not applied",
                                                             "Missing required options: " + ", ".join(option.name for option in SmartMotorControllerConfig.BasicOptions),
                                                             "get")
        
    def validate_external_encoder_options(self) -> None:
        if self._use_external_encoder and not self._external_encoder:
            raise SmartMotorControllerConfigurationException("External encoder options are not applied.",
                                                             "Missing required options: " + ", ".join(option.name for option in SmartMotorControllerConfig.ExternalEncoderOptions),
                                                             "get")
    
    def get_external_encoder_inverted(self) -> bool:
        self._external_encoder_options.remove(SmartMotorControllerConfig.ExternalEncoderOptions.EncoderInverted)
        if RobotBase.isSimulation():
            return False
        return self._external_encoder_inverted