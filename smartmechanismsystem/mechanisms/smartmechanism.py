from commands2 import Command, cmd, Subsystem
from wpilib import Mechanism2d
from wpimath.units import volts, radians
from wpimath.geometry import Translation3d

from smartmechanismsystem.motorcontrollers.smartmotorcontroller import (
    SmartMotorController,
)
from smartmechanismsystem.telemetry.telemetry import MechanismTelemetry

from abc import ABC, abstractmethod


class SmartMechanism(ABC):
    """
    Generic implementation of a mechanism with advanced telemetry.
    """

    _subsystem: Subsystem
    _smc: SmartMotorController
    _telemetry: MechanismTelemetry = MechanismTelemetry()
    _mechanism_window: Mechanism2d

    def set(self, duty_cycle: float) -> Command:
        return (
            cmd.startRun(
                self._smc.stop_closed_loop_controller,
                lambda: self.set_duty_cycle(duty_cycle),
                self._subsystem,
            )
            .finallyDo(self.start_closed_loop_controller)
            .withName(self._subsystem.getName() + " SetDutyCycle")
        )

    def set_voltage(self, volts: volts) -> Command:
        return (
            cmd.startRun(
                self._smc.stop_closed_loop_controller,
                lambda: self._smc.set_voltage(volts),
                self._subsystem,
            )
            .finallyDo(self._smc.start_closed_loop_controller)
            .withName(self._subsystem.getName() + " SetVoltage")
        )

    def set_measurement_velocity_setpoint(self, velocity) -> None:
        self._smc.start_closed_loop_controller()
        self._smc.set_velocity(velocity)

    def set_measurement_position_setpoint(self, distance) -> None:
        self._smc.start_closed_loop_controller()
        self._smc.set_position(distance)

    def set_voltage_setpoint(self, voltage: volts) -> None:
        self._smc.stop_closed_loop_controller()
        self._smc.set_voltage(voltage)

    def set_duty_cycle_setpoint(self, dutycycle: float) -> None:
        self._smc.stop_closed_loop_controller()
        self._smc.set_duty_cycle(dutycycle)

    def get_motor_controller(self) -> SmartMotorController:
        return self._smc

    def get_mechanism_setpoint(self) -> radians:
        return self._smc.get_mechanism_position_setpoint()

    @abstractmethod
    def sim_iterate(self) -> None: ...

    @abstractmethod
    def update_telemetry(self) -> None: ...

    def get_mechanism_window(self) -> Mechanism2d:
        return self._mechanism_window

    @abstractmethod
    def visualization_update() -> None: ...

    @abstractmethod
    def get_relative_mechanism_position() -> Translation3d: ...

    @abstractmethod
    def get_name() -> str: ...
