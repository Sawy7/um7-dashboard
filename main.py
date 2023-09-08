from rsl_comm_py import UM7Serial
from rsl_comm_py.rsl_xml_svd.rsl_svd_parser import Register
from time import sleep

# VARIABLES ###########
PORT_BAUD = 9600
ALL_RAW_RATE = 20
EULER_RATE = 20
ALL_PROC_RATE = 20
POSITION_RATE = 20
#######################

class UM7Communication:
    def __init__(self, port_name="/dev/ttyUSB0", baudrate=115200):
        self.um7 = UM7Serial(port_name=port_name)
        self.set_baudrate(baudrate)
        self.change_rates()
        self.change_settings()
    
    def set_baudrate(self, baudrate):
        print(f"Setting port baud rate to {baudrate}...", end="", flush=True)
        self.um7.port.close()
        self.um7.port.baudrate = baudrate
        self.um7.port.open()
        if self.um7.port.is_open:
            print("Success")
        else:
            print("Error")
            exit(-1)
        sleep(1)

    def set_device_baudrate(self, baudrate_option=5):
        print(f"Setting UM7 baudrate to option {baudrate_option}")
        creg_com_settings, *_ = self.um7.creg_com_settings
        creg_com_settings.set_field_value(BAUD_RATE=baudrate_option)
        self.um7.creg_com_settings = creg_com_settings.raw_value
        sleep(1)

    def set_register_var_value(self, register_name, variable, value):
        # print(f"Setting '{variable}' to {value}...", end="", flush=True)
        print(f"Setting '{variable}' to {value}...")
        working_register = getattr(self.um7, register_name)[0]
        set_args = {variable: value}
        working_register.set_field_value(**set_args)
        setattr(self.um7, register_name, working_register.raw_value)
        sleep(1)

        # actual_state = getattr(self.um7, register_name)
        # if actual_state[-1] == value:
        #     print("Success")
        # else:
        #     print("Error")
        #     exit(-1)
        # sleep(1)

    def change_rates(self):
        # self.set_register_var_value("creg_com_rates2", "ALL_RAW_RATE", 0)
        # self.set_register_var_value("creg_com_rates4", "ALL_PROC_RATE", 10)
        # self.set_register_var_value("creg_com_rates5", "POSITION_RATE", 0)
        # self.set_register_var_value("creg_com_rates5", "VELOCITY_RATE", 0)
        # self.set_register_var_value("creg_com_rates6", "POSE_RATE", 1)

        # self.set_register_var_value("creg_com_rates7", "NMEA_GPS_POSE_RATE", 0)
        # self.set_register_var_value("creg_com_rates7", "NMEA_HEALTH_RATE", 0)
        # self.set_register_var_value("creg_com_rates7", "NMEA_POSE_RATE", 0)
        # self.set_register_var_value("creg_com_rates7", "NMEA_RATES_RATE", 0)
        # self.set_register_var_value("creg_com_rates7", "NMEA_QUAT_RATE", 0)
        pass

    def change_settings(self):
        # self.set_register_var_value("creg_com_settings", "GPS", 1)
        # self.set_register_var_value("creg_com_settings", "SAT", 0)
        # self.set_register_var_value("creg_com_settings", "GPS_BAUD", 0)
        pass

    def print_data(self):
        print(f"Printing all broadcasts:")
        for packet in self.um7.recv_broadcast(flush_buffer_on_start=True):
            print(packet)

    def get_register_values(self, register):
        values = [x for x in register if not isinstance(x, Register)]
        return values

    def print_config(self):
        # reg, baud_rate_enum, gps_baud_enum, gps_enum, sat_enum = self.um7.creg_com_settings
        # print("gps_baud_enum", gps_baud_enum)

        # reg, pps_enum, zg_enum, q_enum, mag_enum = self.um7.creg_misc_settings
        # print("pps", pps_enum)
        # return
        
        print(f"\n========== CONFIG REGISTERS ===================================")
        print(f"creg_com_settings             : {self.get_register_values(self.um7.creg_com_settings)}")
        print(f"creg_com_rates1               : {self.get_register_values(self.um7.creg_com_rates1)}")
        print(f"creg_com_rates2               : {self.get_register_values(self.um7.creg_com_rates2)}")
        print(f"creg_com_rates3               : {self.get_register_values(self.um7.creg_com_rates3)}")
        print(f"creg_com_rates4               : {self.get_register_values(self.um7.creg_com_rates4)}")
        print(f"creg_com_rates5               : {self.get_register_values(self.um7.creg_com_rates5)}")
        print(f"creg_com_rates6               : {self.get_register_values(self.um7.creg_com_rates6)}")
        print(f"creg_com_rates7               : {self.get_register_values(self.um7.creg_com_rates7)}")
        print(f"creg_misc_settings            : {self.get_register_values(self.um7.creg_misc_settings)}")
        print(f"creg_home_north               : {self.get_register_values(self.um7.creg_home_north)}")
        print(f"creg_home_east                : {self.get_register_values(self.um7.creg_home_east)}")
        print(f"creg_home_up                  : {self.get_register_values(self.um7.creg_home_up)}")
        print(f"creg_gyro_trim_x              : {self.get_register_values(self.um7.creg_gyro_trim_x)}")
        print(f"creg_gyro_trim_y              : {self.get_register_values(self.um7.creg_gyro_trim_y)}")
        print(f"creg_gyro_trim_z              : {self.get_register_values(self.um7.creg_gyro_trim_z)}")
        print(f"creg_mag_cal1_1               : {self.get_register_values(self.um7.creg_mag_cal1_1)}")
        print(f"creg_mag_1_cal1_2             : {self.get_register_values(self.um7.creg_mag_cal1_2)}")
        print(f"creg_mag_cal1_3               : {self.get_register_values(self.um7.creg_mag_cal1_3)}")
        print(f"creg_mag_cal2_1               : {self.get_register_values(self.um7.creg_mag_cal2_1)}")
        print(f"creg_mag_cal2_2               : {self.get_register_values(self.um7.creg_mag_cal2_2)}")
        print(f"creg_mag_cal2_3               : {self.get_register_values(self.um7.creg_mag_cal2_3)}")
        print(f"creg_mag_cal3_1               : {self.get_register_values(self.um7.creg_mag_cal3_1)}")
        print(f"creg_mag_cal3_2               : {self.get_register_values(self.um7.creg_mag_cal3_2)}")
        print(f"creg_mag_cal3_3               : {self.get_register_values(self.um7.creg_mag_cal3_3)}")
        print(f"creg_mag_bias_x               : {self.get_register_values(self.um7.creg_mag_bias_x)}")
        print(f"creg_mag_1_bias_y             : {self.get_register_values(self.um7.creg_mag_bias_y)}")
        print(f"creg_mag_bias_z               : {self.get_register_values(self.um7.creg_mag_bias_z)}")
        print(f"creg_accel_cal1_1             : {self.get_register_values(self.um7.creg_accel_cal1_1)}")
        print(f"creg_accel_cal1_2             : {self.get_register_values(self.um7.creg_accel_cal1_2)}")
        print(f"creg_accel_cal1_3             : {self.get_register_values(self.um7.creg_accel_cal1_3)}")
        print(f"creg_accel_cal2_1             : {self.get_register_values(self.um7.creg_accel_cal2_1)}")
        print(f"creg_accel_cal2_2             : {self.get_register_values(self.um7.creg_accel_cal2_2)}")
        print(f"creg_accel_cal2_3             : {self.get_register_values(self.um7.creg_accel_cal2_3)}")
        print(f"creg_accel_cal3_1             : {self.get_register_values(self.um7.creg_accel_cal3_1)}")
        print(f"creg_accel_cal3_2             : {self.get_register_values(self.um7.creg_accel_cal3_2)}")
        print(f"creg_accel_cal3_3             : {self.get_register_values(self.um7.creg_accel_cal3_3)}")
        print(f"creg_accel_bias_x             : {self.get_register_values(self.um7.creg_accel_bias_x)}")
        print(f"creg_accel_bias_y             : {self.get_register_values(self.um7.creg_accel_bias_y)}")
        print(f"creg_accel_bias_z             : {self.get_register_values(self.um7.creg_accel_bias_z)}")

    def print_data_registers(self):
        print(f"\n========== DATA REGISTERS ===================================")
        print(f"dreg_health                   : {self.um7.dreg_health}")
        print(f"dreg_gyro_raw_xy              : {self.um7.dreg_gyro_raw_xy}")
        print(f"dreg_gyro_raw_z               : {self.um7.dreg_gyro_raw_z}")
        print(f"dreg_gyro_raw_time            : {self.um7.dreg_gyro_raw_time}")
        print(f"dreg_accel_raw_xy             : {self.um7.dreg_accel_raw_xy}")
        print(f"dreg_accel_raw_z              : {self.um7.dreg_accel_raw_z}")
        print(f"dreg_accel_raw_time           : {self.um7.dreg_accel_raw_time}")
        print(f"dreg_mag_raw_xy               : {self.um7.dreg_mag_raw_xy}")
        print(f"dreg_mag_raw_z                : {self.um7.dreg_mag_raw_z}")
        print(f"dreg_mag_raw_time             : {self.um7.dreg_mag_raw_time}")
        print(f"dreg_temperature              : {self.um7.dreg_temperature}")
        print(f"dreg_temperature_time         : {self.um7.dreg_temperature_time}")
        print(f"dreg_gyro_proc_x              : {self.um7.dreg_gyro_proc_x}")
        print(f"dreg_gyro_proc_y              : {self.um7.dreg_gyro_proc_y}")
        print(f"dreg_gyro_proc_z              : {self.um7.dreg_gyro_proc_z}")
        print(f"dreg_gyro_proc_time           : {self.um7.dreg_gyro_proc_time}")
        print(f"dreg_accel_proc_x             : {self.um7.dreg_accel_proc_x}")
        print(f"dreg_accel_proc_y             : {self.um7.dreg_accel_proc_y}")
        print(f"dreg_accel_proc_z             : {self.um7.dreg_accel_proc_z}")
        print(f"dreg_accel_proc_time          : {self.um7.dreg_accel_proc_time}")
        print(f"dreg_mag_proc_x               : {self.um7.dreg_mag_proc_x}")
        print(f"dreg_mag_proc_y               : {self.um7.dreg_mag_proc_y}")
        print(f"dreg_mag_proc_z               : {self.um7.dreg_mag_proc_z}")
        print(f"dreg_mag_proc_time            : {self.um7.dreg_mag_proc_time}")
        print(f"dreg_quat_ab                  : {self.um7.dreg_quat_ab}")
        print(f"dreg_quat_cd                  : {self.um7.dreg_quat_cd}")
        print(f"dreg_quat_time                : {self.um7.dreg_quat_time}")
        print(f"dreg_euler_phi_theta          : {self.um7.dreg_euler_phi_theta}")
        print(f"dreg_euler_psi                : {self.um7.dreg_euler_psi}")
        print(f"dreg_euler_phi_theta_dot      : {self.um7.dreg_euler_phi_theta_dot}")
        print(f"dreg_euler_psi_dot            : {self.um7.dreg_euler_psi_dot}")
        print(f"dreg_euler_time               : {self.um7.dreg_euler_time}")
        print(f"dreg_position_north           : {self.um7.dreg_position_north}")
        print(f"dreg_position_east            : {self.um7.dreg_position_east}")
        print(f"dreg_position_up              : {self.um7.dreg_position_up}")
        print(f"dreg_position_time            : {self.um7.dreg_position_time}")
        print(f"dreg_velocity_north           : {self.um7.dreg_velocity_north}")
        print(f"dreg_velocity_east            : {self.um7.dreg_velocity_east}")
        print(f"dreg_velocity_up              : {self.um7.dreg_velocity_up}")
        print(f"dreg_velocity_time            : {self.um7.dreg_velocity_time}")
        print(f"dreg_gps_latitude             : {self.um7.dreg_gps_latitude}")
        print(f"dreg_gps_longitude            : {self.um7.dreg_gps_longitude}")
        print(f"dreg_gps_altitude             : {self.um7.dreg_gps_altitude}")
        print(f"dreg_gps_course               : {self.um7.dreg_gps_course}")
        print(f"dreg_gps_speed                : {self.um7.dreg_gps_speed}")
        print(f"dreg_gps_time                 : {self.um7.dreg_gps_time}")
        print(f"dreg_gps_sat_1_2              : {self.um7.dreg_gps_sat_1_2}")
        print(f"dreg_gps_sat_3_4              : {self.um7.dreg_gps_sat_3_4}")
        print(f"dreg_gps_sat_5_6              : {self.um7.dreg_gps_sat_5_6}")
        print(f"dreg_gps_sat_7_8              : {self.um7.dreg_gps_sat_7_8}")
        print(f"dreg_gps_sat_9_10             : {self.um7.dreg_gps_sat_9_10}")
        print(f"dreg_gps_sat_11_12            : {self.um7.dreg_gps_sat_11_12}")
        print(f"dreg_gyro_bias_x              : {self.um7.dreg_gyro_bias_x}")
        print(f"dreg_gyro_bias_y              : {self.um7.dreg_gyro_bias_y}")
        print(f"dreg_gyro_bias_z              : {self.um7.dreg_gyro_bias_z}")

    def commit_settings(self):
        self.um7.flash_commit = 1
        print("Settings commited to flash...")

    def factory_reset(self):
        self.um7.reset_to_factory = 1
        print("Module reset to factory defaults...")

    def zero_gyros(self):
        self.um7.zero_gyros = 1
        print("Module gyros calibrated...")

if __name__ == "__main__":
    com = UM7Communication(port_name="/dev/ttyUSB0")
    # com.factory_reset()
    # com.commit_settings()
    # com.print_config()
    # com.print_data_registers()
    com.print_data()
    # com.zero_gyros()

    # print("Packets:")
    # flush_on_start = True  # <-- optional, set to true if you want to reset input buffer when starting reception
    # for packet in um7.recv_euler_broadcast(num_packets=100, flush_buffer_on_start=flush_on_start):
    #     print(packet)

    # print("Getting broadcast packets: ")
    # for packet in um7.recv_broadcast(num_packets=10):
    #     print(packet)

    # print(f"Setting baud rate to 115200")
    # creg_com_settings, *_ = um7.creg_com_settings
    # creg_com_settings.set_field_value(BAUD_RATE=5)
    # um7.creg_com_settings = creg_com_settings.raw_value

    # print(f"Setting baud rate to 921600")
    # creg_com_settings, *_ = um7.creg_com_settings
    # creg_com_settings.set_field_value(BAUD_RATE=11)
    # um7.creg_com_settings = creg_com_settings.raw_value