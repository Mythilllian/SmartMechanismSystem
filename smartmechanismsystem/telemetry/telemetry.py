from wpilib import Timer
from ntcore import NetworkTable, NetworkTableInstance, DoubleTopic, DoublePublisher, DoubleSubscriber, BooleanTopic, BooleanPublisher, BooleanSubscriber, PubSubOptions
from enum import Enum, auto
from smartmechanismsystem.motorcontrollers.smartmotorcontroller import SmartMotorController
from smartmechanismsystem.motorcontrollers.smartmotorcontrollerconfig import SmartMotorControllerConfig
from smartmechanismsystem.telemetry.telemetryfields import BooleanTelemetryField, DoubleTelemetryField


class MechanismTelemetry:
    """
    Mechanism telemetry.
    """

    _network_table: NetworkTable
    """
    Telemetry SmartNT.
    """
    _tuning_network_table: NetworkTable
    """
    Tuning SmartNT.
    """

    _loop_time_publisher: DoublePublisher
    """
    Loop time publisher.
    """

    _prev_timestamp: float = 0
    """
    Loop time timer.
    """

    def setup_loop_time(self) -> None:
        """
        Setup loop time publisher.
        """
        loop_time_publisher_topic: DoubleTopic = self._network_table.getDoubleTopic(
            "loopTime"
        )
        loop_time_publisher_topic.setProperties('{"unit":"second"}')
        self._loop_time_publisher = loop_time_publisher_topic.publish()

    def setup_telemetry(
        self,
        mechanism_telemetry_name: str,
        motor_controller: SmartMotorController = None,
    ) -> None:
        """
        Setup telemetry for the Mechanism and motor controller.

        :param mechanism_telemetry_name: Mechanism telemetry name.
        :param motor_controller: :class:`SmartMotorController`: to setup telemetry for optionally.
        """
        self._tuning_network_table = (
            NetworkTableInstance.getDefault()
            .getTable("Tuning")
            .getSubTable(mechanism_telemetry_name)
        )
        self._network_table = (
            NetworkTableInstance.getDefault()
            .getTable("Mechanisms")
            .getSubTable(mechanism_telemetry_name)
        )
        if motor_controller:
            motor_controller.setup_telemetry(
                self._network_table, self._tuning_network_table
            )
        self.setup_loop_time()

    def get_data_table(self) -> NetworkTable:
        """
        Get the telemetry NetworkTable.

        :return: Telemetry NetworkTable
        """
        return self._network_table

    def get_tuning_table(self) -> NetworkTable:
        """
        Get the tuning NetworkTable.

        :return: Tuning NetworkTable.
        """
        return self._tuning_network_table

    def update_loop_time(self) -> None:
        """
        Update the loop time.
        """
        if self._loop_time_publisher:
            if self._prev_timestamp != 0:
                self._loop_time_publisher.set(
                    Timer.getFPGATimestamp() - self._prev_timestamp
                )
            self._prev_timestamp = Timer.getFPGATimestamp()

class BooleanTelemetry:
    _field: BooleanTelemetryField
    _key: str
    _tunable: bool
    _enabled: bool = False
    _default_value: bool
    _cached_value: bool
    _publisher: BooleanPublisher
    _subscriber: BooleanSubscriber
    _topic: BooleanTopic
    _tuning_table: NetworkTable
    _data_table: NetworkTable

    def __init__(self, key: str, default_value: bool, field: BooleanTelemetryField, tunable: bool):
        self._key = key
        self._default_value = default_value
        self._field = field
        self._tunable = tunable
    
    def setup_network_tables(self, data_table: NetworkTable, tuning_table: NetworkTable = _tuning_table) -> None:
        self._data_table = data_table
        self._tuning_table = tuning_table
        if tuning_table and self._tunable:
            self._topic = self._tuning_table.getBooleanTopic(self._key)
            self._publisher = self._topic.publish()
            self._subscriber = self._topic.subscribe(self._default_value, PubSubOptions.kKeepSubscribers)
        else:
            self._topic = self._data_table.getBooleanTopic(self._key)
            self._publisher = self._topic.publish()
            self._publisher.setDefault(self._default_value)

    def set(self, value: bool) -> bool:
        if self._subscriber:
            tuning_value: bool = self._subscriber.get(self._default_value)
            if tuning_value != value:
                return False
        if self._publisher:
            self._publisher.set(value)
        return True
    
    def get(self) -> bool:
        if self._subscriber:
            return self._subscriber.get(self._default_value)
        raise RuntimeError("Tuning table not configured for " + self._key + "!")
    
    def tunable(self) -> bool:
        if self._subscriber and self._tunable and self._enabled:
            if self._subscriber.get(self._default_value) != self._cached_value:
                self._cached_value = self._subscriber.get(self._default_value)
                return True
            return False
        return False
    
    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def display(self, state: bool) -> None:
        self._enabled = state

    def get_field(self) -> BooleanTelemetryField:
        return self._field
    
    def set_default_value(self, value: bool) -> None:
        self._default_value = value
        self._cached_value = value

    def close(self) -> None:
        if self._subscriber:
            self._subscriber.close()
        if self._publisher:
            self._publisher.close()
        self._data_table.getEntry(self._key).unpublish()
        self._tuning_table.getEntry(self._key).unpublish()

class DoubleTelemetry:
    _field: DoubleTelemetryField
    _key: str
    _tunable: bool
    _enabled: bool = False
    _unit: str
    _default_value: float
    _cached_value: float
    _publisher: DoublePublisher
    _subscriber: DoubleSubscriber
    _topic: DoubleTopic
    _tuning_table: NetworkTable
    _data_table: NetworkTable

    def __init__(self, key: str, default_value: float, field: DoubleTelemetryField, tunable: bool, unit: str):
        self._key = key
        self._default_value = default_value
        self._field = field
        self._tunable = tunable
        self._unit = unit

    def set_default_value(self, value: float) -> None:
        self._default_value = value
        self._cached_value = value

    def setup_network_tables(self, data_table: NetworkTable, tuning_table: NetworkTable = _tuning_table) -> None:
        self._data_table = data_table
        self._tuning_table = tuning_table
        if not self._enabled:
            return
        
        if tuning_table and self._tunable:
            self._topic = self._tuning_table.getDoubleTopic(self._key)
            if self._publisher:
                self._publisher = self._topic.publishEx("double", "{\"units\": \"" + self._unit + "\"}")
            else:
                self._publisher = self._topic.publish()
            self._subscriber = self._topic.subscribe(self._default_value, PubSubOptions.kKeepSubscribers)
        elif data_table:
            self._topic = self._data_table.getDoubleTopic(self._key)
            self._publisher = self._topic.publish()
            self._publisher.setDefault(self._default_value)
    
    def transform_unit(self, cfg: SmartMotorControllerConfig) -> "DoubleTelemetry":
        match(self._unit):
            case "tunable_position":
                self._unit = "meter" if cfg.get_linear_cloed_loop_controller_use() else "degrees"
            case "position":
                self._unit = "meter" if cfg.get_linear_cloed_loop_controller_use() else "rotations"
            case "tunable_velocity":
                self._unit = "meter_per_second" if cfg.get_linear_cloed_loop_controller_use() else "rotations_per_minute"
            case "velocity":
                self._unit = "meter_per_second" if cfg.get_linear_cloed_loop_controller_use() else "rotation_per_second"
            case "tunable_acceleration":
                self._unit = "meter_per_second_per_second" if cfg.get_linear_cloed_loop_controller_use() else "rotations_per_minute_per_second"
            case "acceleration":
                self._unit = "meter_per_second_per_second" if cfg.get_linear_cloed_loop_controller_use() else "rotation_per_second_per_second"
        return self
    
    def setup_network_table(self, data_table: NetworkTable) -> None:
        self.setup_network_tables(data_table, None)

    def set(self, value: float) -> bool:
        if not self._enabled:
            return False
        if self._subscriber:
            tuning_value: float = self._subscriber.get(self._default_value)
            if tuning_value != value:
                return False
        if self._publisher:
            self._publisher.set(value)
        return True

    def get(self) -> float:
        if not self._enabled:
            return self._default_value
        if self._subscriber:
            return self._subscriber.get(self._default_value)
        raise RuntimeError("Tuning table not configured for " + self._key + "!")

    def tunable(self) -> bool:
        if self._subscriber and self._tunable and self._enabled:
            if self._subscriber.get(self._default_value) != self._cached_value:
                self._cached_value = self._subscriber.get(self._default_value)
                return True
            return False
        return False
    
    def enable(self) -> None:
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def display(self, state: bool) -> None:
        self._enabled = state

    def get_field(self) -> DoubleTelemetryField:
        return self._field
    
    def close(self) -> None:
        if self._subscriber:
            self._subscriber.close()
        if self._publisher:
            self._publisher.close()
        self._data_table.getEntry(self._key).unpublish()
        self._tuning_table.getEntry(self._key).unpublish()

class SmartMotorControllerTelemetryConfig:
    _bool_fields: dict[BooleanTelemetryField, BooleanTelemetry] = {
        field:field.create() for field in BooleanTelemetryField
    }
    _double_fields: dict[DoubleTelemetryField, DoubleTelemetry] = {
        field:field.create() for field in DoubleTelemetryField
    }

    def with_telemetry_verbosity(self, verbosity: SmartMotorControllerConfig.TelemetryVerbosity) -> "SmartMotorControllerTelemetryConfig":
        # this should include every telemetry field, and should be continuously updated as new fields are added (a RuntimeError will be thrown on HIGH verbosity if not updated)
        use_all = verbosity == SmartMotorControllerConfig.TelemetryVerbosity.HIGH
        if verbosity == SmartMotorControllerConfig.TelemetryVerbosity.HIGH:
            self._bool_fields[BooleanTelemetryField.MechanismLowerLimit].enable()
            self._bool_fields[BooleanTelemetryField.MechanismUpperLimit].enable()
            self._bool_fields[BooleanTelemetryField.TemperatureLimit].enable()
            self._bool_fields[BooleanTelemetryField.VelocityControl].enable()
            self._bool_fields[BooleanTelemetryField.ElevatorFeedForward].enable()
            self._bool_fields[BooleanTelemetryField.ArmFeedForward].enable()
            self._bool_fields[BooleanTelemetryField.SimpleMotorFeedForward].enable()
            self._bool_fields[BooleanTelemetryField.MotionProfile].enable()
            self._bool_fields[BooleanTelemetryField.MotorInversion].enable()
            self._bool_fields[BooleanTelemetryField.EncoderInversion].enable()

            self._double_fields[DoubleTelemetryField.TunableSetpointPosition].enable()
            self._double_fields[DoubleTelemetryField.TunableSetpointVelocity].enable()
            self._double_fields[DoubleTelemetryField.MotorTemperature].enable()
            self._double_fields[DoubleTelemetryField.MechanismLowerLimit].enable()
            self._double_fields[DoubleTelemetryField.MechanismUpperLimit].enable()
            self._double_fields[DoubleTelemetryField.StatorCurrentLimit].enable()
            self._double_fields[DoubleTelemetryField.SupplyCurrentLimit].enable()
            self._double_fields[DoubleTelemetryField.OpenloopRampRate].enable()
            self._double_fields[DoubleTelemetryField.ClosedloopRampRate].enable()
            self._double_fields[DoubleTelemetryField.MeasurementLowerLimit].enable()
            self._double_fields[DoubleTelemetryField.MeasurementUpperLimit].enable()
            self._double_fields[DoubleTelemetryField.kS].enable()
            self._double_fields[DoubleTelemetryField.kV].enable()
            self._double_fields[DoubleTelemetryField.kG].enable()
            self._double_fields[DoubleTelemetryField.kA].enable()
            self._double_fields[DoubleTelemetryField.kP].enable()
            self._double_fields[DoubleTelemetryField.kI].enable()
            self._double_fields[DoubleTelemetryField.kD].enable()
            # fall through to MID
            verbosity = SmartMotorControllerConfig.TelemetryVerbosity.MID
        if verbosity == SmartMotorControllerConfig.TelemetryVerbosity.MID:
            self._double_fields[DoubleTelemetryField.OutputVoltage].enable()
            self._double_fields[DoubleTelemetryField.StatorCurrent].enable()
            self._double_fields[DoubleTelemetryField.SupplyCurrent].enable()
            # fall through to LOW
            verbosity = SmartMotorControllerConfig.TelemetryVerbosity.LOW
        if verbosity == SmartMotorControllerConfig.TelemetryVerbosity.LOW:
            self._double_fields[DoubleTelemetryField.SetpointPosition].enable()
            self._double_fields[DoubleTelemetryField.SetpointVelocity].enable()
            self._double_fields[DoubleTelemetryField.MeasurementPosition].enable()
            self._double_fields[DoubleTelemetryField.MeasurementVelocity].enable()
            self._double_fields[DoubleTelemetryField.MechanismPosition].enable()
            self._double_fields[DoubleTelemetryField.MechanismVelocity].enable()
            self._double_fields[DoubleTelemetryField.RotorPosition].enable()
            self._double_fields[DoubleTelemetryField.RotorVelocity].enable()

        if use_all:
            for dt in self._double_fields.values():
                if(not dt.enabled):
                    # this indicates that this function needs to be updated to include new telemetry fields
                    raise RuntimeError("DoubleTelemetry " + dt.get_field().name + " is disabled at HIGH verbosity!")
            for bt in self._bool_fields.values():
                if(not bt.enabled):
                    # this indicates that this function needs to be updated to include new telemetry fields
                    raise RuntimeError("BooleanTelemetry " + bt.get_field().name + " is disabled at HIGH verbosity!")        
                
        return self
    
    def get_double_fields(self, smc: SmartMotorController) -> dict[DoubleTelemetryField, DoubleTelemetry]:
        config = smc.get_config()
        unsup_telemetry = smc.get_unsupported_telemetry_fields()
        if(unsup_telemetry):
            for bt in unsup_telemetry[0]:
                if bt in self._bool_fields:
                    self._bool_fields[bt].disable()
            for dt in unsup_telemetry[1]:
                if dt in self._double_fields:
                    self._double_fields[dt].disable()
        
        if not smc.get_supply_current():
            self._double_fields[DoubleTelemetryField.SupplyCurrent].disable()
            self._double_fields[DoubleTelemetryField.SupplyCurrentLimit].disable()
        if not config.get_simple_feedforward():
            self._double_fields[DoubleTelemetryField.kG].disable()
        if not config.get_mechanism_circumference():
            self._double_fields[DoubleTelemetryField.MeasurementLowerLimit].disable()
            self._double_fields[DoubleTelemetryField.MeasurementUpperLimit].disable()
            self._double_fields[DoubleTelemetryField.MeasurementPosition].disable()
            self._double_fields[DoubleTelemetryField.MeasurementVelocity].disable()
        else:
            if config.get_mechanism_upper_limit():
                self._double_fields[DoubleTelemetryField.MeasurementUpperLimit].set_default_value(config.convert_from_mechanism(config.get_mechanism_upper_limit()))
            if config.get_mechanism_lower_limit():
                self._double_fields[DoubleTelemetryField.MeasurementLowerLimit].set_default_value(config.convert_from_mechanism(config.get_mechanism_lower_limit()))
        if config.get_mechanism_upper_limit():
            self._double_fields[DoubleTelemetryField.MechanismUpperLimit].set_default_value(config.get_mechanism_upper_limit())
        if config.get_mechanism_lower_limit():
            self._double_fields[DoubleTelemetryField.MechanismLowerLimit].set_default_value(config.get_mechanism_lower_limit())
        if config.get_supply_stall_current_limit():
            self._double_fields[DoubleTelemetryField.SupplyCurrentLimit].set_default_value(config.get_supply_stall_current_limit())
        if config.get_stator_stall_current_limit():
            self._double_fields[DoubleTelemetryField.StatorCurrentLimit].set_default_value(config.get_stator_stall_current_limit())
        if(config.get_pid()):
            self._double_fields[DoubleTelemetryField.kP].set_default_value(config.get_p())
            self._double_fields[DoubleTelemetryField.kI].set_default_value(config.get_i())
            self._double_fields[DoubleTelemetryField.kD].set_default_value(config.get_d())
        if(config.get_trapezoid_profile()):
            e = config.get_trapezoid_profile()
            self._double_fields[DoubleTelemetryField.ExponentialProfileMaxInput].disable()
            self._double_fields[DoubleTelemetryField.ExponentialProfileKA].disable()
            self._double_fields[DoubleTelemetryField.ExponentialProfileKV].disable()

            self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxAcceleration].enable()
            if config.get_velocity_trapezoidal_proifle_in_use():
                max_jerk = e.max_acceleration # TODO: ????? what
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxJerk].set_default_value(max_jerk)
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxJerk].enable()
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxVelocity].disable()
            elif config.get_linear_closed_loop_controller_use():
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxAcceleration].set_default_value(e.max_acceleration)
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxVelocity].set_default_value(e.max_velocity)
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxVelocity].enable()
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxJerk].disable()
            else:
                #TODO: how do I do the unit conversations???
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxAcceleration].set_default_value(e.max_acceleration)
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxVelocity].set_default_value(e.max_velocity)
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxVelocity].enable()
                self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxJerk].disable()
        if(config.get_exponential_profile()):
            e = config.get_exponential_profile()
            self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxAcceleration].disable()
            self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxVelocity].disable()
            self._double_fields[DoubleTelemetryField.TrapezoidalProfileMaxJerk].disable()

            self._double_fields[DoubleTelemetryField.ExponentialProfileKA].enable()
            self._double_fields[DoubleTelemetryField.ExponentialProfileKV].enable()
            self._double_fields[DoubleTelemetryField.ExponentialProfileMaxInput].enable()
            #TODO: more conversions wdid
            kV = config.convert_to_mechanism(-e.A / e.B) if config.get_linear_closed_loop_controller_use() else -e.A / e.B
            kA = 1.0 / e.B if config.get_linear_closed_loop_controller_use() else 1.0 / e.B
            self._double_fields[DoubleTelemetryField.ExponentialProfileKV].set_default_value(kV)
            self._double_fields[DoubleTelemetryField.ExponentialProfileKA].set_default_value(kA)
            self._double_fields[DoubleTelemetryField.ExponentialProfileMaxInput].set_default_value(e.max_input)
        if(config.get_lqr_closed_loop_controller()):
            self._double_fields[DoubleTelemetryField.kP].disable()
            self._double_fields[DoubleTelemetryField.kV].disable()
            self._double_fields[DoubleTelemetryField.kA].disable()
        if(config.get_arm_feedforward()):
            e = config.get_arm_feedforward()
            self._double_fields[DoubleTelemetryField.kG].enable()
            self._double_fields[DoubleTelemetryField.kS].set_default_value(e.getKs())
            self._double_fields[DoubleTelemetryField.kV].set_default_value(e.getKv())
            self._double_fields[DoubleTelemetryField.kA].set_default_value(e.getKa())
            self._double_fields[DoubleTelemetryField.kG].set_default_value(e.getKg())
        if(config.get_elevator_feedforward()):
            e = config.get_elevator_feedforward()
            self._double_fields[DoubleTelemetryField.kG].enable()
            self._double_fields[DoubleTelemetryField.kS].set_default_value(e.getKs())
            self._double_fields[DoubleTelemetryField.kV].set_default_value(e.getKv())
            self._double_fields[DoubleTelemetryField.kA].set_default_value(e.getKa())
            self._double_fields[DoubleTelemetryField.kG].set_default_value(e.getKg())
        if(config.get_simple_feedforward()):
            e = config.get_simple_feedforward()
            self._double_fields[DoubleTelemetryField.kG].disable()
            self._double_fields[DoubleTelemetryField.kS].set_default_value(e.getKs())
            self._double_fields[DoubleTelemetryField.kV].set_default_value(e.getKv())
            self._double_fields[DoubleTelemetryField.kA].set_default_value(e.getKa())
        return self._double_fields
    
    def get_boolean_fields(self, smc: SmartMotorController) -> dict[BooleanTelemetryField, BooleanTelemetry]:
        config = smc.get_config()
        if not config.get_arm_feedforward():
            self._bool_fields[BooleanTelemetryField.ArmFeedForward].disable()
        if not config.get_elevator_feedforward():
            self._bool_fields[BooleanTelemetryField.ElevatorFeedForward].disable()
        if not config.get_simple_feedforward():
            self._bool_fields[BooleanTelemetryField.SimpleMotorFeedForward].disable()
        self._bool_fields[BooleanTelemetryField.MotorInversion].set_default_value(config.get_motor_inverted())
        self._bool_fields[BooleanTelemetryField.EncoderInversion].set_default_value(config.get_encoder_inverted())
        return self._bool_fields
    
    def with_mechanism_lower_limit(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.MechanismLowerLimit].enable()
        return self
    
    def with_mechanism_upper_limit(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.MechanismUpperLimit].enable()
        return self
    
    def with_temperature_limit(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.TemperatureLimit].enable()
        return self
    
    def with_velocity_control(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.VelocityControl].enable()
        return self
    
    def with_elevator_feedforward(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.ElevatorFeedForward].enable()
        return self
    
    def with_arm_feedforward(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.ArmFeedForward].enable()
        return self
    
    def with_simple_feedforward(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.SimpleMotorFeedForward].enable()
        return self
    
    def with_motion_profile(self) -> "SmartMotorControllerTelemetryConfig":
        self._bool_fields[BooleanTelemetryField.MotionProfile].enable()
        return self
    
    def with_setpoint_position(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.SetpointPosition].enable()
        return self
    
    def with_output_voltage(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.OutputVoltage].enable()
        return self
    
    def with_stator_current(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.StatorCurrent].enable()
        return self
    
    def with_temperature(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.MotorTemperature].enable()
        return self
    
    def with_measurement_position(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.MeasurementPosition].enable()
        return self
    
    def with_measurement_velocity(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.MeasurementVelocity].enable()
        return self
    
    def with_mechanism_position(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.MechanismPosition].enable()
        return self
    
    def with_mechanism_velocity(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.MechanismVelocity].enable()
        return self
    
    def with_rotor_position(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.RotorPosition].enable()
        return self
    
    def with_rotor_velocity(self) -> "SmartMotorControllerTelemetryConfig":
        self._double_fields[DoubleTelemetryField.RotorVelocity].enable()
        return self
        

class SmartMotorControllerTelemetry:
    verbosity: SmartMotorControllerConfig.TelemetryVerbosity = SmartMotorControllerConfig.TelemetryVerbosity.HIGH
    double_fields = dict[DoubleTelemetryField, DoubleTelemetry]
    bool_fields = dict[BooleanTelemetryField, BooleanTelemetry]
    data_network_table: NetworkTable
    tuning_network_table: NetworkTable
    config: SmartMotorControllerTelemetryConfig
