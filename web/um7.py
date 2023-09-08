from rsl_comm_py import UM7Serial
from rsl_comm_py.rsl_xml_svd.rsl_svd_parser import Register
import json
import dataclasses

class UM7Communication:
    def __init__(self, port_name="/dev/ttyUSB0", baudrate=115200):
        self.um7 = UM7Serial(port_name=port_name)
        self.set_baudrate(baudrate)
        # self.change_rates()
        # self.change_settings()

    """
    This sets the baudrate of the serial port
    """
    def set_baudrate(self, baudrate):
        self.um7.port.close()
        self.um7.port.baudrate = baudrate
        self.um7.port.open()
        if not self.um7.port.is_open:
            exit(-1)

    """
    This changes the value of chosen register on device
    """
    def set_register_var_value(self, register_name, variable, value):
        working_register = getattr(self.um7, register_name)[0]
        set_args = {variable: value}
        if len(working_register.fields) > 1:
            working_register.set_field_value(**set_args)
            setattr(self.um7, register_name, working_register.raw_value)
        else:
            setattr(self.um7, register_name, value)

    """
    This returns last raw log message from the device
    """
    def get_raw_data(self):
        return next(self.um7.recv_broadcast(num_packets=1, flush_buffer_on_start=True))

    """
    This returns last log message formatted as JSON from the device
    """
    def get_json_data(self):
        broadcast = next(self.um7.recv_broadcast(num_packets=1, flush_buffer_on_start=True))
        broadcast_dict = dataclasses.asdict(broadcast)
        broadcast_dict["packet_type"] = type(broadcast).__name__
        return json.dumps(broadcast_dict)

    """
    This sets the baudrate of the device (default is 115200)
    """
    def set_device_baudrate(self, baudrate_option=5):
        creg_com_settings, *_ = self.um7.creg_com_settings
        creg_com_settings.set_field_value(BAUD_RATE=baudrate_option)
        self.um7.creg_com_settings = creg_com_settings.raw_value

    """
    This gets all the registers containing settings
    """
    def get_cregs(self):
        creg_register_values = []
        for reg in self.um7.svd_parser.cregs:
            name = reg.name.lower()
            reg, *_ = getattr(self.um7, name)
            creg_register_values.append(reg)

        return creg_register_values

    def get_cregs_dict(self):
        return [x.as_dict() for x in self.get_cregs()]

if __name__ == "__main__":
    com = UM7Communication()
    com.set_register_var_value("creg_accel_cal3_2", "ACCEL_CAL3_2", 0)
