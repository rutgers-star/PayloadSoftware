#include <iostream>
#include "FUTEK_USB_DLL.h"

#include <string.h>
#include <stdio.h>
#include <ctime>
#include <ratio>
#include <chrono>
#include <unistd.h>
#include <fstream>


using namespace std;
int main()
{


    _FUTEK_USB_DLL::FUTEK_USB_DLL dll;

    PVOID deviceHandle ;
    BYTE channelNumber = 0;
	
	cout<<"Attempting sensor Initialization"<<endl;
	//Sensor initialization
    string sn = dll.Get_Device_Serial_Number(0);
    char *serialNumber = new char[sn.length() + 1];
    strcpy(serialNumber, sn.c_str());
    dll.Open_Device_Connection(serialNumber);
    deviceHandle = dll.DeviceHandle;

    string boardType = dll.Get_Type_of_Board(deviceHandle);
    string firmVersion = dll.Get_Firmware_Version(deviceHandle);
    string samplingRate = dll.Get_ADC_Sampling_Rate(deviceHandle, channelNumber);
    cout<< samplingRate<< endl;
    cout<<"Initialized Sensor"<<endl;
   
    
    
    //Initialize variables for sensor calibration values
    float offsetValue;
    float fullScaleValue;
    float fullScaleLoad;
    int decimalPoint;
    float unitCode;
    float normalData;
    float calculatedReading;
    string unitChr;
    float motorx;
    float motory;
    float motorz;
    
    cout<<"Starting CSV logging"<<endl;
    //Initialize spreadsheet
    std::ofstream log;
    log.open ("log.csv");
    log << "load (grams) , TimeStamp (sec), MiddleMarker X, MiddleMarker Y, MiddleMarker Z, MotorX,MotorY,MotorZ,ThrustPointX,ThrustPointY,ThrustPointZ \n";
    auto start = std::chrono::steady_clock::now();
    
    while(true)
    {
    
    	//Collect readings and calibration datas, this prob doesnt need to be in the loop
    	offsetValue = stof(dll.Get_Offset_Value(deviceHandle,channelNumber),NULL);
    	fullScaleValue = stof(dll.Get_Fullscale_Value(deviceHandle,channelNumber),NULL);
    	fullScaleLoad = stof(dll.Get_Fullscale_Load(deviceHandle,channelNumber),NULL);
    	decimalPoint = stoi(dll.Get_Decimal_Point(deviceHandle,channelNumber),NULL);
    	unitCode = stof(dll.Get_Decimal_Point(deviceHandle,channelNumber),NULL);
    	normalData = stof(dll.Normal_Data_Request(deviceHandle,channelNumber),NULL);
    	
    	//Use calibration data to get converted reading to grams
    	calculatedReading = normalData - offsetValue;
    	calculatedReading = calculatedReading/(fullScaleValue - offsetValue);
   		calculatedReading = calculatedReading*fullScaleLoad*453.5924;
    	calculatedReading = calculatedReading/(pow(10,decimalPoint));
  	
    	
    	//get time stamp
		auto end = std::chrono::steady_clock::now();
    	std::chrono::duration<double> elapsed_seconds = end-start;
    	
    	//output to spreadsheet
    	cout<<calculatedReading<<endl;
    	std::cout << "elapsed time: " << elapsed_seconds.count() << ",";
    	log << calculatedReading<< " , ";
		log << elapsed_seconds.count() <<",";
		log << 0 <<",";
		log << 1 <<",";
		log << 2 <<",";
		log << 0 <<",";
		log << 9 <<",";
		log << 0<<",";
		log << 0 <<",";
		log << 1 <<",";
		log << 2 <<endl;
    	
        //string adc = dll.Normal_Data_Request(deviceHandle, channelNumber);
        //cout << adc << endl;
        usleep((unsigned int)1000000);
    }
    dll.Close_Device_Connection(serialNumber);

}
