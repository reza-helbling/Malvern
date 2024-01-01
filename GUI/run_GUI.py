import GUI
from tkinter import * 
import config.motor_1 as Motor1
import config.motor_Linear as Motor_VG
import config.Pump as P
import time
import u6
import threading
import config.MeerstetterTEC as TEC
import json
import logging

#------------------- Constants -----------------------------------------
BS1_THRESHOLD = 2.5  #Threshold value for bubble sensor 1
BS2_THRESHOLD = 2.5  #Threshold value for bubble sensor 2
BS3_THRESHOLD = 2.5  #Threshold value for bubble sensor 3
BS4_THRESHOLD = 2.5  #Threshold value for bubble sensor 4
BS5_THRESHOLD = 2.5  #Threshold value for bubble sensor 5
BS6_THRESHOLD = 2.5  #Threshold value for bubble sensor 6
BS7_THRESHOLD = 2.5  #Threshold value for bubble sensor 7
BS8_THRESHOLD = 2.5  #Threshold value for bubble sensor 8
BS9_THRESHOLD = 2.5  #Threshold value for bubble sensor 9
BS10_THRESHOLD = 2.5  #Threshold value for bubble sensor 10
BS11_THRESHOLD = 2.5  #Threshold value for bubble sensor 11
BS12_THRESHOLD = 2.5  #Threshold value for bubble sensor 12
BS13_THRESHOLD = 2.5  #Threshold value for bubble sensor 13
BS14_THRESHOLD = 2.5  #Threshold value for bubble sensor 14
#---------------------------------------------------------------------------



class run_GUI(GUI.GUI):

    def __init__(self,root):
        super().__init__( root)
        # logging.basicConfig(level=logging.INFO)
        logging.basicConfig(
            level=logging.DEBUG,
            #format="%(asctime)s %(levelname)s %(message)s",
            format="%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            #filename="basic.log"
        )
        
        logging.info("Initializing hardware -------------------------------------")
        self.PortAssignment()
        self.InitMixerMotor()
        self.InitGantryVertical()            
        self.InitPump1()
        self.InitLabjack()
        self.InitTecController()
        self.InitTimer()
        logging.info("Hardware initialiation done")        

        #------------ Setting the inital states/values of the hardware ----------------------
        # # self.scalefactor = 1
        # # # self.microstep = False         
        # # # self.pump_scale_factor(1)
        # # # logging.info('mircostep off')
        # # # self.set_step_mode(False)
        # # self.BS= 1        

        
        # logging.info(self.mc.set_temp(35.3))
        # logging.info("----------------------------------------------")

        # # # # #-------- set the motor1 speed to 0
        # # # valid = self.motor1.set_speed(0)
        # # # time.sleep(.25)
        # # # if (valid == True):
        # # #     self.m1_cur_spd.config(text="0")        

        # # # #------ init valve 1 to 'E' 
        # # # self.pump1.set_valve(1, 'E')
        # # # time.sleep(.75)
        # # # self.v1_cur_pos.config(text = "Pump to Air (P1)")
        
        logging.info("------------------------------------------------------------------")
        logging.info('System started successfully.')
        logging.info("Please use the GUI to enter a commamnd ...")
        

    def timerCallback_1(self):  
        global BS1_THRESHOLD, BS2_THRESHOLD, BS3_THRESHOLD, BS4_THRESHOLD, BS5_THRESHOLD
        global BS6_THRESHOLD, BS7_THRESHOLD, BS8_THRESHOLD, BS9_THRESHOLD, BS10_THRESHOLD
        global BS11_THRESHOLD, BS12_THRESHOLD, BS13_THRESHOLD, BS14_THRESHOLD
        # logging.info('--->timer tick')
        #------------------------------- update pump 1 position
        # p1_cur_pos = self.pump1.get_plunger_position(1)            
        # p1_cur_pos = int(p1_cur_pos / self.scalefactor)
        # self.p1_cur_pos.config(text = str(p1_cur_pos))
        # # logging.info('cur pos:', p1_cur_pos)
    
        # #------------------------------- update  of TEC controller parameters
        # # logging.info(self.mc.get_data())
        # tec_dic =  self.mc.get_data()
        # obj_temp = round(tec_dic['object temperature'][0], 1)
        # target_temp = round(tec_dic['target object temperature'][0], 1)
        # TEC_cur_status = tec_dic['loop status'][0]
        # # logging.info('--->', float(obj_temp), '   ,  ', target_temp, ' status:',TEC_cur_status)
        # # 1: ON, 0:OFF, 
        # if (TEC_cur_status== 1):            
        #     self.t_status.config(text = "ON")                        
        # else:
        #     self.t_status.config(text = "OFF")        
        # self.tec_cur_tmp.config(text=str(obj_temp))
        # self.tec_desired_tmp.config(text=str(target_temp))
        
        #-------- update Gantry vertical motor position on GUI ------------------
        p= self.motor_gv.read_actual_position()
        self.m3_cur_spd.config(text = p)  

        #-------- read bubble sensor and update the GUI -------------------------
        self.read_BubbleSensors()      
        self.update_BubbleSensorLEDs()                  

        #-------- repeat the timer ----------------------------------------------
        self.timer = threading.Timer(1.0, self.timerCallback_1)
        self.timer.start()


    def InitPump1(self):        
        # # #------ init. Pump 1
        # # # logging.info(" Initializing Pumps/Valves.....")
        # # # self.pump1 = P.Pump("COM6")
        # # # logging.info("\tPumps initialized")
        # # # self.pump1.pump_Zinit(1)
        pass


    def InitLabjack(self):
        # # initialize labjack
        logging.info("Initializing Labjack.....")
        self.labjack = u6.U6()
        self.labjack.writeRegister(50590, 15)        
        logging.info('\tlabjack initialized')
        # pass

    def InitTimer(self):
        # #------ Starts timer
        logging.info('starting internal timer')
        self.timer = threading.Timer(1.0, self.timerCallback_1)
        self.timer.start()
        logging.info('\tInternal timer started')
        #pass

    def InitTecController(self):
        # ------create object of TEC5 
        logging.info("Initialzing TEC Temperature Controller---------------------")
        # self.mc = TEC.MeerstetterTEC("COM5")
        self.mc = TEC.MeerstetterTEC(self.TEC_PORT)
        # logging.info(self.mc.get_data())
        logging.info("\tTEC controller initialized ")



    def read_BubbleSensors(self):
        # read bubble sensor and update the LEDs
        self.BS0 = (self.labjack.getAIN(0))
        self.BS1 = (self.labjack.getAIN(1))
        self.BS2 = (self.labjack.getAIN(2))
        self.BS3 = (self.labjack.getAIN(3))
        self.BS4 = (self.labjack.getAIN(4))
        self.BS5 = (self.labjack.getAIN(5))
        self.BS6 = (self.labjack.getAIN(6))
        self.BS7 = (self.labjack.getAIN(7))
        self.BS8 = (self.labjack.getAIN(8))
        self.BS9 = (self.labjack.getAIN(9))
        self.BS10 = (self.labjack.getAIN(10))
        self.BS11 = (self.labjack.getAIN(11))
        self.BS12 = (self.labjack.getAIN(12))
        self.BS13 = (self.labjack.getAIN(13))


    def update_BubbleSensorLEDs(self):
        # Update The GUI with current value of bubble sensors
        X3 = 1050
        Y1 = 100
        dY1 = 40
        dd=50

        if (self.BS0 < BS1_THRESHOLD):
            self.led_on_1.place_forget()
            self.led_off_1.pack()
            self.led_off_1.place(x = X3+50,y = Y1 + 0*dY1)
        else:
            self.led_off_14.place_forget()
            self.led_on_1.pack()            
            self.led_on_1.place(x = X3+50,y = Y1 + 0*dY1)

        if (self.BS1 < BS2_THRESHOLD):
            self.led_on_2.place_forget()
            # self.led_off_14.pack()
            self.led_off_2.place(x = X3+50,y = Y1 + 1*dY1)
        else:
            self.led_off_2.place_forget()
            # self.led_on_14.pack()            
            self.led_on_2.place(x = X3+50,y = Y1 + 1*dY1)

        if (self.BS2 < BS3_THRESHOLD):
            self.led_on_3.place_forget()
            # self.led_off_14.pack()
            self.led_off_3.place(x = X3+50,y = Y1 + 2*dY1)
        else:
            self.led_off_3.place_forget()
            # self.led_on_14.pack()            
            self.led_on_3.place(x = X3+50,y = Y1 + 2*dY1)

        if (self.BS3 < BS4_THRESHOLD):
            self.led_on_4.place_forget()
            # self.led_off_14.pack()
            self.led_off_4.place(x = X3+50,y = Y1 + 3*dY1)
        else:
            self.led_off_4.place_forget()
            # self.led_on_14.pack()            
            self.led_on_4.place(x = X3+50,y = Y1 + 3*dY1)

        if (self.BS4 < BS5_THRESHOLD):
            self.led_on_5.place_forget()
            # self.led_off_14.pack()
            self.led_off_5.place(x = X3+50,y = Y1 + 4*dY1)
        else:
            self.led_off_5.place_forget()
            # self.led_on_14.pack()            
            self.led_on_5.place(x = X3+50,y = Y1 + 4*dY1)
            
        if (self.BS5 < BS6_THRESHOLD):
            self.led_on_6.place_forget()
            # self.led_off_14.pack()
            self.led_off_6.place(x = X3+50,y = Y1 + 5*dY1)
        else:
            self.led_off_6.place_forget()
            # self.led_on_14.pack()            
            self.led_on_6.place(x = X3+50,y = Y1 + 5*dY1)

        if (self.BS6 < BS7_THRESHOLD):
            self.led_on_7.place_forget()
            # self.led_off_14.pack()
            self.led_off_7.place(x = X3+50,y = Y1 + 6*dY1)
        else:
            self.led_off_7.place_forget()
            # self.led_on_14.pack()            
            self.led_on_7.place(x = X3+50,y = Y1 + 6*dY1)
        
        if (self.BS7 < BS8_THRESHOLD):
            self.led_on_8.place_forget()
            # self.led_off_14.pack()
            self.led_off_8.place(x = X3+50,y = Y1 + 7*dY1)
        else:
            self.led_off_8.place_forget()
            # self.led_on_14.pack()            
            self.led_on_8.place(x = X3+50,y = Y1 + 7*dY1)

        if (self.BS8 < BS9_THRESHOLD):
            self.led_on_9.place_forget()
            # self.led_off_14.pack()
            self.led_off_9.place(x = X3+50,y = Y1 + 8*dY1)
        else:
            self.led_off_9.place_forget()
            # self.led_on_14.pack()            
            self.led_on_9.place(x = X3+50,y = Y1 + 8*dY1)

        if (self.BS9< BS10_THRESHOLD):
            self.led_on_10.place_forget()
            # self.led_off_14.pack()
            self.led_off_10.place(x = X3+50,y = Y1 + 9*dY1)
        else:
            self.led_off_10.place_forget()
            # self.led_on_14.pack()            
            self.led_on_10.place(x = X3+50,y = Y1 + 9*dY1)

        if (self.BS10 < BS11_THRESHOLD):
            self.led_on_11.place_forget()
            # self.led_off_14.pack()
            self.led_off_11.place(x = X3+50,y = Y1 + 10*dY1)
        else:
            self.led_off_11.place_forget()
            # self.led_on_14.pack()            
            self.led_on_11.place(x = X3+50,y = Y1 + 10*dY1)

        if (self.BS11 < BS12_THRESHOLD):
            self.led_on_12.place_forget()
            # self.led_off_14.pack()
            self.led_off_12.place(x = X3+50,y = Y1 + 11*dY1)
        else:
            self.led_off_12.place_forget()
            # self.led_on_14.pack()            
            self.led_on_12.place(x = X3+50,y = Y1 + 11*dY1)

        if (self.BS13 < BS13_THRESHOLD):
            self.led_on_13.place_forget()
            # self.led_off_14.pack()
            self.led_off_13.place(x = X3+50,y = Y1 + 12*dY1)
        else:
            self.led_off_13.place_forget()
            # self.led_on_14.pack()            
            self.led_on_13.place(x = X3+50,y = Y1 + 12*dY1)

        if (self.BS13 < BS14_THRESHOLD):
            self.led_on_14.place_forget()
            self.led_off_14.pack()
            self.led_off_14.place(x = X3+50,y = Y1 + 13*dY1)
        else:
            self.led_off_14.place_forget()
            self.led_on_14.pack()
            self.led_on_14.place(x = X3+50,y = Y1 + 13*dY1)  




    def PortAssignment(self):
        logging.info("Assigning Ports -------------------------------------------")
        # #---- extract port numbers for config.json
        with open('./config/config.json') as json_file:
            ports = json.load(json_file)
        #assign port numbers to the hardware
        # logging.info('ports:', ports)
        self.TEC_PORT = ports['TEC']
        self.PUMP1_PORT = ports['PUMP1']
        self.TECHNOSOFT_PORT = ports['TECHNOSOFT']
        # self.GANTRY_VER_AXIS_ID = 255
        self.GANTRY_VER_AXIS_ID = int(ports['GANTRY_VER_AXIS_ID'])        
        # str1 = '   TEC port:'+ self.TEC_PORT+ 'Technosoft port:',self.TECHNOSOFT_PORT +'   pump1:', self.PUMP1_PORT + '   Gantry Vertical Axis ID:'+ str(self.GANTRY_VER_AXIS_ID)
        # logging.info(str1)
        logging.info('\tTEC port:'+ self.TEC_PORT)
        logging.info('\tTechnosoft port:'+self.TECHNOSOFT_PORT )
        logging.info('\tpump1:'+ self.PUMP1_PORT)
        logging.info('\tGantry Vertical Axis ID:'+ str(self.GANTRY_VER_AXIS_ID))
        logging.info("\tPort Assignment done")
        # # Display port numbers on the GUI (config tab)
        self.Ltecport.config(text=self.TEC_PORT)
        self.Lpump1port.config(text=self.PUMP1_PORT)
        self.Ltechnosoftport.config(text=self.TECHNOSOFT_PORT)
        self.Lver_gant_axis_id.config(text=self.GANTRY_VER_AXIS_ID)



    def gantry_vertical_set_rel_click(self):
        s = self.ent_gnt_ver_rel.get()
        # logging.info('child-->'+s)
        if (is_float(s) == True):
            # logging.info('it\'s a number:', float(s))
            #logging.info("----------MOVE Relative-----------------")
            speed = 15.0;	
            acceleration = 1.0#
            rel_pos =int(s)
            self.motor_gv.set_POSOKLIM(1)

            self.motor_gv.move_relative_position(rel_pos, speed, acceleration)

        else:
            logging.info("not a number")



    def gantry_vertical_set_abs_click(self):

        s = self.ent_gnt_ver_abs.get()
        # logging.info('child-->'+s)
        if (is_float(s) == True):
            # logging.info('it\'s a number:', float(s))
            #logging.info("----------MOVE Absolute-----------------")
            speed = 15.0;	
            acceleration = 1.0#
            abs_pos =int(s)
            self.motor_gv.set_POSOKLIM(1)

            self.motor_gv.move_absolute_position(abs_pos, speed, acceleration)

        else:
            logging.info("not a number")        
        



    def InitGantryVertical(self):
        logging.info("Initializing Gantry Vertical Actuator.....")        
        self.motor_gv = Motor_VG.motor_Linear(self.TECHNOSOFT_PORT.encode('ascii'),
                                              self.GANTRY_VER_AXIS_ID, b"LEFS25")    
        #/*	Setup and initialize the axis */	
        if (self.motor_gv.InitAxis()==False):
            logging.error("Failed to start up the drive")    
        logging.info("\tGantry Vertical Actuator Initialized")        
        tt =self.motor_gv.set_position()
        if (tt==True):
            logging.info("\tcurrent position is set as referece for Gantry Vertical")
        else:
            logging.error("\t Failed to set position")



    def InitMixerMotor(self):
        # # #------ init. motor 1
        # # logging.info("Initializing Motors.....")
        # # self.motor1 = Motor1.motor_1(0,1.5)
        # # logging.info("\tMotors Initialized")

        # #------ init. motors: Gantry vertical 
        pass


    def tec_b_tmpset_click(self):
        logging.info("child: TECt new tmp:")
        s =   self.ent_tmp.get()
        if (is_float(s) == True):
            # logging.info(s)
            self.mc.set_temp(float(s))
        else:
            logging.info("invalid input")



    def tec_b_start_click(self):
        logging.info("child: TEC start")
        self.mc.enable()
        pass

    def tec_b_stop_click(self):
        logging.info("child: TEC stop")
        self.mc.disable()
        pass


    def checkComboCfg1(self, event):
        # def option_selected(event):
        s = self.comboCfg1.get()
        logging.info('child :', s)
        ss=s.partition(')')
        # index = self.comboCfg1.get(0, "end") 
        index = ss[0]
        logging.info('int number:', int(index))        
        # logging.info("INDEX = ", index)
        self.pump_scale_factor(int(index))
        if (self.microstep == False):
            logging.info('mircostep off')
            self.set_step_mode(False)            
        else:  #self.microstep = True
            logging.info('mircostep on')
            self.set_step_mode(True)
            

    def p1_b_pickup_pos_click(self):
        logging.info("child: p1_pickup ")
        s =   self.ent_pickup_pos.get()
        logging.info(int(s))
        self.pump1.set_pickup(1, int(s))

    def p1_b_dispense_pos_click(self):
        logging.info("child: p1_dispense ")
        s =   self.ent_dispemse_pos.get()
        logging.info(int(s))
        self.pump1.set_dispense(1, int(s))


    def checkComboCfg2(self, event):
        # def option_selected(event):
        logging.info('child:', self.comboCfg1.get())






    def m1_b_abs_pos_click(self):
        logging.info("child: m1_new_spd")
        s =   self.ent_m1_spd_.get()
        logging.info(s)
        if (is_float(s) == True):
            logging.info('it\'s a number:', float(s))
            m1_speed = float(s)
            motor1_speed = float(m1_speed)
            logging.info("motor 1 speed: ", motor1_speed)
            valid = self.motor1.set_speed(motor1_speed)
            if (valid == True):
                 self.m1_cur_spd.config(text=s)            
        else:
            logging.info("not a number")
            
    
    # def p1_b_Zinit_click(self):
    #      logging.info("child: p1 Z initialized")
    #      self.pump1.pump_Zinit(1)

    # def p1_b_Yinit_click(self):
    #      logging.info("child: p1 Y initialized")
    #      self.pump1.pump_Yinit(1)



    # def p1_b_abs_pos_click(self):
    #     logging.info("----> p1_abs pos")
    #     s =   self.ent_abs_pos.get()
    #     logging.info(s)
    #     self.p1_cur_pos["text"]=  s


    def p1_b_abs_pos_click(self):
        logging.info("child: p1_abs pos")
        s =   self.ent_abs_pos.get()
        logging.info(s)
        if (is_float(s) == True):
            val = int(s)
            abs_pos = int(val * self.scalefactor)
            logging.info('position is:', abs_pos)
            self.pump1.set_pos_absolute(1, abs_pos)
            ####===============to be moved to the timer thread
            # time.sleep(.25)
            # cur_plunger_pos = self.pump1.get_plunger_position(1)            
            # self.p1_cur_pos.config(text = str(cur_plunger_pos))


    def p1_b_dispenseUntillbubble(self):
        logging.info(' dispense until bubble: to be completed later')
        pass


    def p1_b_teminateP1(self):
        logging.info('child: termnate p1')
        self.pump1.stop(1)



    def p1_b_pickupUntillbubble(self):
        logging.info("child: pickup until bubble")
        # send pump1 to 0 position
        # self.pump1.set_pos_absolute(1, 0)
        prev_speed = self.pump1.get_peakspeed(1)
        # change to high speed for retraction
        if (self.microstep == False):
            logging.info('micro step is off')
            self.pump1.set_speed(1,1000)
        else:
            logging.info('micro step is on')
            self.pump1.set_speed(1,1000*8)

        a =self.pump1.get_peakspeed(1)
        time.sleep(.25)
        logging.info('peak speed:', a)
        self.pump1.set_pos_absolute(1, 0)

        cur_pos = 24000
        logging.info('going to 0 pos')
        while (cur_pos > 0):
            # logging.info('cur pos:', cur_pos)
            cur_pos = self.pump1.get_plunger_position(1)            
            time.sleep(1)

        # change to low speed for forward motion
        if (self.microstep == False):
            logging.info('micro step is off')
            self.pump1.set_speed(1,48)
        else:
            logging.info('micro step is on')
            self.pump1.set_speed(1,48*8)

        logging.info('going to final pos')
        self.pump1.set_pos_absolute(1, 10000)

        # continue until a bubble detected or reaching end of travel
        input0 = (self.labjack.getAIN(0))
        while (cur_pos < 2000 and  input0>2.5):
            input0 = (self.labjack.getAIN(0))
            logging.info('        selcted BS',self.BS, ' , reading: ',self.labjack.getAIN(self.BS-1))
            logging.info('bubble sensor output:', input0)
            # time.sleep(1)
            logging.info('cur pos ==', cur_pos)
            cur_pos = self.pump1.get_plunger_position(1)            
        self.pump1.stop(1)
        time.sleep(.25)
        self.pump1.set_speed(1, prev_speed)


    def p1_b_top_spd_click(self):
        logging.info("p1_top speed")
        s =   self.ent_top_spd.get()
        logging.info(s)
        if (is_float(s) == True):
            max_spd = int(s)
            self.pump1.set_speed(1,max_spd)
             ####===============to be moved to the timer thread
            time.sleep(.25)
            self.p1_cur_spd.config(text = s)

    def checkCombo1(self,event):
        s = self.combo1.get()
        logging.info('child -->'+s)
        ("Pump to Air (P1)","Air to Gas (P2)","Gas to Line (P3)",
                                 "Line to Pump (P4)")
        if (s == "Pump to Air (P1)"):
            # logging.info(" P1   --- E ")
            new_valve_pos = 'E'
        elif (s == "Air to Gas (P2)"):
            # logging.info(" P2 ---- O")
            new_valve_pos = 'O'
        elif (s == "Gas to Line (P3)"):
            # logging.info(" P3 --- I")
            new_valve_pos = 'I'
        elif (s == "Line to Pump (P4)"):
            # logging.info(" P4 ---- B ")
            new_valve_pos = 'B'
        else:
            logging.info(' invalid valve selection')
            new_valve_pos = 'E'
        self.pump1.set_valve(1, new_valve_pos)
        time.sleep(1)
        s = self.pump1.get_valve(1)
        # logging.info("-----> ",s)
        cur_valve = "----"
        if (s=='e'):
            cur_valve = "Pump to Air (P1)"
            # logging.info('EEEE')
        elif(s=='o'):
            cur_valve = "Air to Gas (P2)"
            # logging.info('OOOO')
        elif(s=="i"):
            cur_valve = "Gas to Line (P3)"
            # logging.info("IIII")
        elif(s=="b"):
            cur_valve = "Line to Pump (P4)"
            # logging.info("BBBB")
        else:
            cur_valve = "error"

        self.v1_cur_pos.config(text=cur_valve)


    def checkCombo0(self,event):        
        s = self.combo0.get()        
        ss=s.partition('S')
        index = int(ss[2])
        logging.info('bubble sensor number:', index)
        X3 = 1050
        Y1 = 100
        dY1 = 40
        # Label(self.tab1, text = "     ",font=("Arial", 15) , bg='#D9D9D9',fg='red').place(x = X3-40,y = Y1 + 0*dY1)         
        self.lbs1.place_forget()
        self.lbs2.place_forget()
        self.lbs3.place_forget()
        self.lbs4.place_forget()
        self.lbs5.place_forget()
        self.lbs6.place_forget()
        self.lbs7.place_forget()
        self.lbs8.place_forget()
        self.lbs9.place_forget()
        self.lbs10.place_forget()
        self.lbs11.place_forget()
        self.lbs12.place_forget()
        self.lbs13.place_forget()
        self.lbs14.place_forget()

        if (index == 1):
            self.lbs2.pack()
            self.lbs2.place(x = X3-40,y = Y1 + 0*dY1)
            self.BS = 1
        elif (index == 2):
            self.lbs2.pack()
            self.lbs2.place(x = X3-40,y = Y1 + 1*dY1)
            self.BS = 2
        elif (index == 3):
            self.lbs3.pack()
            self.lbs3.place(x = X3-40,y = Y1 + 2*dY1)  
            self.BS = 3
        elif (index == 4):
            self.lbs4.pack()
            self.lbs4.place(x = X3-40,y = Y1 + 3*dY1)
            self.BS = 4
        elif (index == 5):
            self.lbs5.pack()
            self.lbs5.place(x = X3-40,y = Y1 + 4*dY1)
            self.BS = 5
        elif (index == 6):
            self.lbs6.pack()
            self.lbs6.place(x = X3-40,y = Y1 + 5*dY1)
            self.BS = 6
        elif (index == 7):
            self.lbs7.pack()
            self.lbs7.place(x = X3-40,y = Y1 + 6*dY1)
            self.BS = 7
        elif (index == 8):
            self.lbs8.pack()
            self.lbs8.place(x = X3-40,y = Y1 + 7*dY1)
            self.BS = 8
        elif (index == 9):
            self.lbs9.pack()
            self.lbs9.place(x = X3-40,y = Y1 + 8*dY1)
            self.BS = 9
        elif (index == 10):
            self.lbs10.pack()
            self.lbs10.place(x = X3-40,y = Y1 + 9*dY1)
            self.BS = 10
        elif (index == 11):
            self.lbs11.pack()
            self.lbs11.place(x = X3-40,y = Y1 + 10*dY1)
            self.BS = 11
        elif (index == 12):
            self.lbs12.pack()
            self.lbs12.place(x = X3-40,y = Y1 + 11*dY1)
            self.BS = 12
        elif (index == 13):
            self.lbs13.pack()
            self.lbs13.place(x = X3-40,y = Y1 + 12*dY1)  
            self.BS = 13
        elif (index == 14):
            self.lbs14.pack()
            self.lbs14.place(x = X3-40,y = Y1 + 13*dY1)
            self.BS = 14



    def checkCombob1(self,event):        
        s = self.combob1.get()        
        ss=s.partition('S')
        index = int(ss[2])
        logging.info('bubble sensor number:', index)
        X3 = 1050
        Y1 = 100
        dY1 = 40
        # Label(self.tab1, text = "     ",font=("Arial", 15) , bg='#D9D9D9',fg='red').place(x = X3-40,y = Y1 + 0*dY1)         
        self.lbs1.place_forget()
        self.lbs2.place_forget()
        self.lbs3.place_forget()
        self.lbs4.place_forget()
        self.lbs5.place_forget()
        self.lbs6.place_forget()
        self.lbs7.place_forget()
        self.lbs8.place_forget()
        self.lbs9.place_forget()
        self.lbs10.place_forget()
        self.lbs11.place_forget()
        self.lbs12.place_forget()
        self.lbs13.place_forget()
        self.lbs14.place_forget()

        if (index == 1):
            self.lbs2.pack()
            self.lbs2.place(x = X3-40,y = Y1 + 0*dY1)
            self.BS = 1
        elif (index == 2):
            self.lbs2.pack()
            self.lbs2.place(x = X3-40,y = Y1 + 1*dY1)
            self.BS = 2
        elif (index == 3):
            self.lbs3.pack()
            self.lbs3.place(x = X3-40,y = Y1 + 2*dY1)  
            self.BS = 3
        elif (index == 4):
            self.lbs4.pack()
            self.lbs4.place(x = X3-40,y = Y1 + 3*dY1)
            self.BS = 4
        elif (index == 5):
            self.lbs5.pack()
            self.lbs5.place(x = X3-40,y = Y1 + 4*dY1)
            self.BS = 5
        elif (index == 6):
            self.lbs6.pack()
            self.lbs6.place(x = X3-40,y = Y1 + 5*dY1)
            self.BS = 6
        elif (index == 7):
            self.lbs7.pack()
            self.lbs7.place(x = X3-40,y = Y1 + 6*dY1)
            self.BS = 7
        elif (index == 8):
            self.lbs8.pack()
            self.lbs8.place(x = X3-40,y = Y1 + 7*dY1)
            self.BS = 8
        elif (index == 9):
            self.lbs9.pack()
            self.lbs9.place(x = X3-40,y = Y1 + 8*dY1)
            self.BS = 9
        elif (index == 10):
            self.lbs10.pack()
            self.lbs10.place(x = X3-40,y = Y1 + 9*dY1)
            self.BS = 10
        elif (index == 11):
            self.lbs11.pack()
            self.lbs11.place(x = X3-40,y = Y1 + 10*dY1)
            self.BS = 11
        elif (index == 12):
            self.lbs12.pack()
            self.lbs12.place(x = X3-40,y = Y1 + 11*dY1)
            self.BS = 12
        elif (index == 13):
            self.lbs13.pack()
            self.lbs13.place(x = X3-40,y = Y1 + 12*dY1)  
            self.BS = 13
        elif (index == 14):
            self.lbs14.pack()
            self.lbs14.place(x = X3-40,y = Y1 + 13*dY1)
            self.BS = 14



    def set_step_mode(self, flag):

        if (flag == False):
            logging.info('switch to normal mode')
            self.pump1.set_microstep_position(1,0)
        else:
            logging.info(" switched to p&v  ")
            self.pump1.set_microstep_position(1,2)



    def pump_scale_factor(self, N):        
        if (N == 1):
            STEP_RANGE = 48000.
            VOLUME = 1000.
            self.microstep = False
        elif (N == 2):
            STEP_RANGE = 48000.
            VOLUME = 1000.
            self.microstep = True
        elif (N == 3):
            STEP_RANGE = 48000.
            VOLUME = 500.
            self.microstep = False
        elif (N == 4):
            STEP_RANGE = 48000.
            VOLUME = 500.
            self.microstep = True
        elif (N == 5):
            STEP_RANGE = 48000.
            VOLUME = 250.
            self.microstep = False
        elif (N == 6):
            STEP_RANGE = 48000.
            VOLUME = 250.
            self.microstep = True
        elif (N == 7):
            STEP_RANGE = 24000.
            VOLUME = 2500.
            self.microstep = False
        elif (N == 8):
            STEP_RANGE = 24000.
            VOLUME = 2500.
            self.microstep = True
        elif (N == 9):
            STEP_RANGE = 1
            VOLUME = 1
            self.microstep = False
            pass
        elif (N == 10):
            STEP_RANGE = 1
            VOLUME = 1
            self.microstep = True
            pass
        else:
            logging.info("invalid scale factor")
            self.scalefactor = 1

        self.scalefactor = STEP_RANGE / VOLUME
        logging.info('scale factor:', self.scalefactor)



    ###------------------- END OF CLASS DEFINITION ------------------------------------------------------








def is_float(element: any) -> bool:
    #If you expect None to be passed:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False
    



def main(): #run mianloop 
    
    root = Tk()
    # app = GUI.GUI(root)
    run_GUI(root)

    root.mainloop()

if __name__ == '__main__':
    main()