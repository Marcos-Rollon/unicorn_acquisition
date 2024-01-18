import UnicornPy
import numpy as np
from typing import Callable, Dict, Any, Optional

class UnicornManager:
    """ A class to encapsulate the functionality of UnicornPy"""
    def __init__(self, show_logs : bool = True, frame_length : int = 1) -> None:
        """
            Constructor for the Unicorn Manager class

            Parameters:
        
            - show_logs (bool) : Show logging information. Default True
            - frame_lenght (int) : Select the number of samples in between 1 and 25 acquired per acquisition cycle

        """
        self._device_list = []
        self._connectedDevice : UnicornPy.Unicorn = None
        self._frame_length = max(1, min(frame_length, 25))
        self._is_acquiring_data : bool = False
        self._show_logs = show_logs

    def get_device_list(self) -> [str]:
        """Tries to get the device list for ALREADY connected devices. Can rise an error"""
        self._deviceList = UnicornPy.GetAvailableDevices(True) #Param True -> only look for already paired devices
        return self._device_list
    
    def connect_to_device(self, device :str)-> None:
        """Tries to connect to the device. Can rise an error"""
        self._connectedDevice = UnicornPy.Unicorn(device)
    
    def stop_adquisition(self,):
        if self._connectedDevice == None:
            if self._show_logs:
                print("Cannot stop adquisition because there is no connected device")
            return
        self._is_acquiring_data = False
        self._connectedDevice.StopAcquisition()
    def start_adquisition(self,
                           on_new_data : Callable[[[float]], None], 
                           test_signal_enabled : bool = False):
        """
            Starts the data adquisition. Can raise an error.
            test_signal_enabled -> if true, a square test signal will be returned from the
            device. If false, the electrodes output will be returned.
        """
        numberOfAcquiredChannels= self._connectedDevice.GetNumberOfAcquiredChannels()
        configuration = self._connectedDevice.GetConfiguration()

        # We need to set the known lenght of the adquisition buffer, and the best thing to do
        # is to reuse that buffer. 
        # Allocate memory for the acquisition buffer.
        receiveBufferBufferLength = self._frame_length * numberOfAcquiredChannels * 4
        receiveBuffer = bytearray(receiveBufferBufferLength)

       ####### PRETTY SURE THIS NEEDS TO BE ASYNC OR SOMETHING LIKE THAT 
        try:
            self._connectedDevice.StartAcquisition(test_signal_enabled)
            self._is_acquiring_data = True
            while self._is_acquiring_data:
                self._connectedDevice.GetData(self._frame_length,receiveBuffer,receiveBufferBufferLength)
                #convert the data to a numpy float array
                # Convert receive buffer to numpy float array 
                data = np.frombuffer(receiveBuffer, dtype=np.float32, count=numberOfAcquiredChannels * self._frame_length)
                data = np.reshape(data, (self._frame_length, numberOfAcquiredChannels))
                # Execute callback
                on_new_data(data)
        except Exception as e:
            print(e)
