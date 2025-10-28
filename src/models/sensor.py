from typing import Any, ClassVar, Dict, Mapping, Optional, Sequence, Tuple
from datetime import datetime, timezone

from typing_extensions import Self
from viam.components.sensor import Sensor
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes


class UserActivationSensor(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(ModelFamily("viam-soleng", "user-activation"), "sensor")
    
    # Internal state
    activation_date: Optional[str] = None  # ISO 8601 timestamp or None
    delete_flag: bool = False  # Whether account is marked for deletion

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this Sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both required and optional)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any required dependencies or optional dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Tuple[Sequence[str], Sequence[str]]: A tuple where the
                first element is a list of required dependencies and the
                second element is a list of optional dependencies
        """
        # No dependencies needed for this sensor
        return [], []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both required and optional)
        """
        # Load attributes from config
        attrs = dict(config.attributes.fields)
        
        # Load activation_date (defaults to None)
        if "activation_date" in attrs:
            value = attrs["activation_date"]
            if value.HasField("null_value"):
                self.activation_date = None
            elif value.HasField("string_value"):
                self.activation_date = value.string_value
            else:
                self.activation_date = None
        else:
            self.activation_date = None
        
        # Load delete_flag (defaults to False)
        if "delete_flag" in attrs:
            value = attrs["delete_flag"]
            if value.HasField("bool_value"):
                self.delete_flag = value.bool_value
            else:
                self.delete_flag = False
        else:
            self.delete_flag = False
        
        self.logger.info(
            f"Reconfigured: activation_date={self.activation_date}, delete_flag={self.delete_flag}"
        )

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:
        """Returns current activation state as sensor readings.
        
        Returns:
            Mapping[str, SensorReading]: Dictionary with activation_date and delete_flag
        """
        return {
            "activation_date": self.activation_date,
            "delete_flag": self.delete_flag
        }

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        """Handles DoCommand requests for activation state management.
        
        Supported commands:
        - get_activation_state: Returns current state
        
        Args:
            command (Mapping[str, ValueTypes]): The command to execute
            
        Returns:
            Mapping[str, ValueTypes]: Command response
        """
        cmd = command.get("command")
        
        if cmd == "get_activation_state":
            return self._get_activation_state()
        
        else:
            error_msg = f"Unknown command: {cmd}"
            self.logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def _get_activation_state(self) -> Dict[str, Any]:
        """Returns current activation state."""
        self.logger.debug("Getting activation state")
        return {
            "activation_date": self.activation_date,
            "delete_flag": self.delete_flag
        }

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> Sequence[Geometry]:
        self.logger.error("`get_geometries` is not implemented")
        raise NotImplementedError()