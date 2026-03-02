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
