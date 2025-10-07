"""
Watchdog and safety features for hardware operations
"""
import asyncio
from typing import Callable, Any, Tuple
from backend.config import get_settings

settings = get_settings()


class PositionValidator:
    """Validates stage positions before movement"""

    @staticmethod
    def validate_position(x: float = None, y: float = None, z: float = None) -> Tuple[bool, str]:
        """
        Validate position against safety limits.

        Returns:
            (is_valid, error_message)
        """
        if x is not None:
            if x < settings.MIN_X_POSITION or x > settings.MAX_X_POSITION:
                return False, f"X position {x} out of range [{settings.MIN_X_POSITION}, {settings.MAX_X_POSITION}]"

        if y is not None:
            if y < settings.MIN_Y_POSITION or y > settings.MAX_Y_POSITION:
                return False, f"Y position {y} out of range [{settings.MIN_Y_POSITION}, {settings.MAX_Y_POSITION}]"

        if z is not None:
            if z < settings.MIN_Z_POSITION or z > settings.MAX_Z_POSITION:
                return False, f"Z position {z} out of range [{settings.MIN_Z_POSITION}, {settings.MAX_Z_POSITION}]"

        return True, ""

    @staticmethod
    def validate_relative_move(current_x: float, current_y: float, current_z: float,
                                dx: float = 0, dy: float = 0, dz: float = 0) -> Tuple[bool, str]:
        """Validate relative movement"""
        target_x = current_x + dx
        target_y = current_y + dy
        target_z = current_z + dz

        return PositionValidator.validate_position(target_x, target_y, target_z)


class Watchdog:
    """Timeout protection for hardware operations"""

    @staticmethod
    async def execute_with_timeout(
        coro: Callable,
        timeout: float,
        operation_name: str
    ) -> Any:
        """
        Execute async operation with timeout.

        Args:
            coro: Async function to execute
            timeout: Timeout in seconds
            operation_name: Name for error messages

        Returns:
            Result of the operation

        Raises:
            TimeoutError: If operation exceeds timeout
        """
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(
                f"{operation_name} timed out after {timeout} seconds. "
                "Check hardware connection."
            )
