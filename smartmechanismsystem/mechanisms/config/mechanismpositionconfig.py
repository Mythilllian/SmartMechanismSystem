from wpimath.units import meters
from wpimath.geometry import Translation3d
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