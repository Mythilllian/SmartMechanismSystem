from smartmechanismsystem.telemetry.telemetry import BooleanTelemetry, DoubleTelemetry
from enum import Enum

class BooleanTelemetryField(Enum):
    MechanismUpperLimit = ("limits/Mechanism Upper Limit", False, False)
    MechanismLowerLimit = ("limits/Mechanism Lower Limit", False, False)
    TemperatureLimit = ("limits/Temperature Limit", False, False)
    VelocityControl = ("control/Velocity Control", False, False)
    ElevatorFeedForward = ("control/Elevator Feedforward", False, False)
    ArmFeedForward = ("control/Arm Feedforward", False, False)
    SimpleMotorFeedForward = ("control/Simple Motor Feedforward", False, False)
    MotionProfile = ("control/Motion Profile", False, False)
    MotorInversion = ("motor/inverted", False, True)
    EncoderInversion = ("encoder/inverted", False, True)

    def __init__(self, key: str, default_value: bool, tunable: bool):
        self.key = key
        self.default_value = default_value
        self.tunable = tunable
    
    def create(self) -> BooleanTelemetry:
        return BooleanTelemetry(self.key, self.default_value, self, self.tunable)


class DoubleTelemetryField(Enum):
    ExponentialProfileKV = ("closedloop/motionprofile/kV", 0.0, True, "none")
    ExponentialProfileKA = ("closedloop/motionprofile/kA", 0.0, True, "none")
    ExponentialProfileMaxInput = ("closedloop/motionprofile/maxInput", 12.0, True, "volts")
    TrapezoidalProfileMaxVelocity = ("closedloop/motionprofile/maxVelocity", 0.0, True, "tunable_velocity")
    TrapezoidalProfileMaxAcceleration = ("closedloop/motionprofile/maxAcceleration", 0.0, True, "tunable_acceleration")
    TrapezoidalProfileMaxJerk = ("closedloop/motionprofile/maxJerk", 0.0, True, "rotations_per_minute_per_second_per_second")
    kS = ("closedloop/feedforward/kS", 0.0, True, "none")
    kV = ("closedloop/feedforward/kV", 0.0, True, "none")
    kA = ("closedloop/feedforward/kA", 0.0, True, "none")
    kG = ("closedloop/feedforward/kG", 0.0, True, "none")
    kP = ("closedloop/feedback/kP", 0.0, True, "none")
    kI = ("closedloop/feedback/kI", 0.0, True, "none")
    kD = ("closedloop/feedback/kD", 0.0, True, "none")
    TunableSetpointPosition = ("closedloop/setpoint/position", 0.0, True, "tunable_position")
    SetpointPosition = ("closedloop/setpoint/position", 0.0, False, "position")
    TunableSetpointVelocity = ("closedloop/setpoint/velocity", 0.0, True, "tunable_velocity")
    SetpointVelocity = ("closedloop/setpoint/velocity", 0.0, False, "velocity")
    OutputVoltage = ("motor/outputVoltage", 0.0, False, "volts")
    StatorCurrent = ("current/stator", 0.0, False, "amps")
    StatorCurrentLimit = ("current/limit/stator", 0.0, True, "amps")
    SupplyCurrent = ("current/supply", 0.0, False, "amps")
    SupplyCurrentLimit = ("current/limit/supply", 0.0, True, "amps")
    MotorTemperature = ("motor/temperature", 0.0, False, "fahrenheit")
    MeasurementPosition = ("measurement/position", 0.0, False, "meters")
    MeasurementVelocity = ("measurement/velocity", 0.0, False, "meters_per_second")
    MeasurementLowerLimit = ("measurement/limit/lower", 0.0, True, "meters")
    MeasurementUpperLimit = ("measurement/limit/upper", 0.0, True, "meters")
    MechanismPosition = ("mechanism/position", 0.0, False, "rotations")
    MechanismVelocity = ("mechanism/velocity", 0.0, False, "rotations_per_second")
    MechanismLowerLimit = ("mechanism/limit/lower", 0.0, True, "degrees")
    MechanismUpperLimit = ("mechanism/limit/upper", 0.0, True, "degrees")
    RotorPosition = ("rotor/position", 0.0, False, "rotations")
    RotorVelocity = ("rotor/velocity", 0.0, False, "rotations_per_second")
    ClosedloopRampRate = ("rampratet Python /dutycycle/closedloop", 0.0, True, "seconds")
    OpenloopRampRate = ("ramprate/dutycycle/openloop", 0.0, True, "seconds")

    def __init__(self, key: str, default_value: float, tunable: bool, unit: str):
        self.key = key
        self.default_value = default_value
        self.tunable = tunable
        self.unit = unit

    def create(self) -> DoubleTelemetry:
        return DoubleTelemetry(self.key, self.default_value, self, self.tunable, self.unit)