from wpilib import Timer
from ntcore import NetworkTable, NetworkTableInstance, DoubleTopic, DoublePublisher
from smartmechanismsystem.motorcontrollers import SmartMotorController


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
