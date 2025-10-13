import asyncio
from viam.module.module import Module
try:
    from models.sensor import UserActivationSensor
except ModuleNotFoundError:
    # when running as local module with run.sh
    from .models.sensor import UserActivationSensor


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())