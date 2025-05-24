import logging
from emulator.hardware import epd_hardware
from emulator.config import RST_PIN, DC_PIN, BUSY_PIN, CS_PIN, SCREEN_HEIGHT, SCREEN_WIDTH


class EPD:
    def __init__(self):
        self.reset_pin = RST_PIN
        self.dc_pin = DC_PIN
        self.busy_pin = BUSY_PIN
        self.cs_pin = CS_PIN
        self.width = 128
        self.height = 296

    lut_full_update = [
        0x50, 0xAA, 0x55, 0xAA, 0x11, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0xFF, 0xFF, 0x1F, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]

    lut_partial_update  = [
        0x10, 0x18, 0x18, 0x08, 0x18, 0x18,
        0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x13, 0x14, 0x44, 0x12,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
        
    # Hardware reset
    def reset(self):
        epd_hardware.digital_write(self.reset_pin, 1)
        epd_hardware.delay_ms(200) 
        epd_hardware.digital_write(self.reset_pin, 0)
        epd_hardware.delay_ms(10)
        epd_hardware.digital_write(self.reset_pin, 1)
        epd_hardware.delay_ms(200)   

    def send_command(self, command):
        epd_hardware.digital_write(self.dc_pin, 0)
        epd_hardware.digital_write(self.cs_pin, 0)
        epd_hardware.spi_writebyte([command])
        epd_hardware.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epd_hardware.digital_write(self.dc_pin, 1)
        epd_hardware.digital_write(self.cs_pin, 0)
        epd_hardware.spi_writebyte([data])
        epd_hardware.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        while(epd_hardware.digital_read(self.busy_pin) == 1):      #  0: idle, 1: busy
            epd_hardware.delay_ms(200) 

    def TurnOnDisplay(self):
        self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xC4)
        self.send_command(0x20) # MASTER_ACTIVATION
        self.send_command(0xFF) # TERMINATE_FRAME_READ_WRITE
        
        #logging.debug("e-Paper busy")
        self.ReadBusy()
        #logging.debug("e-Paper busy release")  

    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start >> 3) & 0xFF)
        self.send_data((x_end >> 3) & 0xFF)
        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def SetCursor(self, x, y):
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x >> 3) & 0xFF)
        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.ReadBusy()
        
    def init(self, lut):
        if (epd_hardware.module_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()
        
        self.send_command(0x01) # DRIVER_OUTPUT_CONTROL
        self.send_data((296 - 1) & 0xFF)
        self.send_data(((296 - 1) >> 8) & 0xFF)
        self.send_data(0x00) # GD = 0 SM = 0 TB = 0
        
        self.send_command(0x0C) # BOOSTER_SOFT_START_CONTROL 
        self.send_data(0xD7)
        self.send_data(0xD6)
        self.send_data(0x9D)
        
        self.send_command(0x2C) # WRITE_VCOM_REGISTER
        self.send_data(0xA8) # VCOM 7C
        
        self.send_command(0x3A) # SET_DUMMY_LINE_PERIOD
        self.send_data(0x1A) # 4 dummy lines per gate
        
        self.send_command(0x3B) # SET_GATE_TIME
        self.send_data(0x08) # 2us per line
        
        self.send_command(0x11) # DATA_ENTRY_MODE_SETTING
        self.send_data(0x03) # X increment Y increment
        
        self.send_command(0x32) # WRITE_LUT_REGISTER
        for i in range(0, len(lut)):
            self.send_data(lut[i])
        # EPD hardware init end
        return 0
    
    def set_refresh_mode_partial(self):
        self.init(self.lut_partial_update)

    def set_refresh_mode_full(self):
        self.init(self.lut_full_update)

    def getbuffer(self, image):
        # logging.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width/8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logging.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if(imwidth == self.width and imheight == self.height):
            #logging.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif(imwidth == self.height and imheight == self.width):
            #logging.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buf

    def display(self, img):
        image = self.getbuffer(img)
        if (image == None):
            return            
        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        for j in range(0, self.height):
            self.SetCursor(0, j)
            self.send_command(0x24) # WRITE_RAM
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])   
        self.TurnOnDisplay()
        
    def clear(self, color=0xFF):
        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        for j in range(0, self.height):
            self.SetCursor(0, j)
            self.send_command(0x24) # WRITE_RAM
            for i in range(0, int(self.width / 8)):
                self.send_data(color)   
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10) # DEEP_SLEEP_MODE
        self.send_data(0x01)
        
    def Dev_exit(self):
        epd_hardware.module_exit()
### END OF FILE ###

