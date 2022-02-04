#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: menghanliu
This is the file defining objects and tool functions.
"""
import pandas as pd
import numpy as np
#import pyDOE2
import random


    
    
class Event:
    """
    Event_type includes arrival, harvest, process, finish 
    Event is defined as a point on the timeline.
    """
    def __init__(self, name, e_type, e_happen_time, place, machine, operator, job, rework_times):
        self.name = name
        self.e_type = e_type
        self.e_happen_time = e_happen_time
        self.place = place
        self.machine = machine
        self.operator = operator
        self.job = job
        self.rework_times = rework_times
        
    def get_event_info(self):
        if self.machine != None and self.operator != None:
            event_info=[self.name, self.e_type, self.e_happen_time, self.place.name, self.machine.name, self.operator.name, self.job.name, self.rework_times, self.job.process_yield]
        elif self.place == 'finish_stack' or 'quality check, no place':
            event_info=[self.name, self.e_type, self.e_happen_time, self.place, self.machine, self.operator, self.job.name, self.rework_times, self.job.process_yield]
        else:
            event_info=[self.name, self.e_type, self.e_happen_time, self.place.name, self.machine, self.operator, self.job.name, self.rework_times, self.job.process_yield]
        return event_info
        
        
        
class Job:    
    #also called patient
    def __init__(self, name, id_num, place, conversion_factor, BV_m_LB, BV_m_HB, BV_f_LB, BV_f_HB, mfg_time_separator_1, mfg_time_separator_2, delta_mix_1, delta_mix_2, bad_pat_separator, average_pat_separator,good_pat_separator):
        self.name = name
        self.id_num = id_num
        self.place = place  #can be queue or machine
        self.state = 'initial'   #can be initial, harvesting/ed, processing/ed, finished #also in queue
        self.rework_times = 0
        self.process_yield = 0  #yield is 0 at initial and will be changed in processing
        self.BV_m_LB=BV_m_LB            #lower bound of male blood vol
        self.BV_m_HB=BV_m_HB            #higher bound of male blood vol
        self.BV_f_LB=BV_f_LB            #lower bound of female blood vol
        self.BV_f_HB=BV_f_HB            #higher bound of female blood vol
        self.mfg_time_separator_1 = mfg_time_separator_1
        self.mfg_time_separator_2 = mfg_time_separator_2
        self.manufacturing_time = 0    #time taken to manufacture i.e upward slope
        
        self.delta_mix_1 = delta_mix_1
        self.delta_mix_2 = delta_mix_2
        
        self.alpha_low_mfg = 0
        self.delta_time = 0

        self.processingtime=0           #time at which processing is done

        self.new_sample = 0             #counter for taking new sample when yield becomes to 0


        self.bad_pat_separator=bad_pat_separator
        self.average_pat_separator=average_pat_separator
        self.good_pat_separator=good_pat_separator




        #generate alpha_low and alpha_up using mfg_mix and delta with coin toss


        #good bad or average patient
        separator1=bad_pat_separator+average_pat_separator
        flip1 = np.random.uniform(0, 1)
        #if (flip1 ):
        if (flip1<=self.bad_pat_separator):
            patient_type = 'bad'

        elif (self.bad_pat_separator<flip1<=separator1):
            patient_type= 'average'

        else:
            patient_type = 'good'
        self.patient_type = patient_type    






        #gender generation
        flip2 = random.randint(0, 1)
        if (flip2 == 0):
            gender = 'male'
        else:
            gender = 'female'
        self.gender = gender
        #blood volume
        if (self.gender == 'Male'):
            BV = np.random.uniform(low = BV_m_LB, high = BV_m_HB) 
        else:
            BV = np.random.uniform(low = BV_f_LB, high = BV_f_HB)
        self.BV = BV
        
        #tgt bc
        self.patients_target_bc = self.BV*conversion_factor


        """

        #time for manufacturing
        flip3 = np.random.uniform(0, 1)
        mfg_time_separator = self.mfg_time_separator_1 + self.mfg_time_separator_2
        #if (flip1 ):
        if (flip2<=self.mfg_time_separator_1):
            self.manufacturing_time = 7 #days or use distribution  5 to 9, 9 to 17, 17 to 23

        elif (self.mfg_time_separator_1<flip2<= mfg_time_separator):
            self.manufacturing_time = 14 #days

        else:
            self.manufacturing_time = 20 #days




        #self.delta_time = delta           #time taken for the yield to remain at max and then decay i.e. plateau            
        #time for manufacturing
        flip4 = np.random.uniform(0, 1)
        delta_time_separator = self.delta_mix_1 + self.delta_mix_2
        #if (flip1 ):
        if (flip4<=self.delta_mix_1):
            self.delta_time = 6 #hours          #hours or use distribution  5 to 9, 9 to 17, 17 to 23

        elif (self.delta_mix_1<flip4<=delta_time_separator):
            self.delta_time = 12 #hours

        else:
            self.delta_time = 24 #hours





        self.alpha_low_mfg = self.patients_target_bc * self.manufacturing_time * 24



        """










        #delta, alpha_up, alpha_low values generated from the limits
        #self.delta_mfg= np.random.uniform(delta_ll,delta_ul)
        #self.alpha_up_mfg= np.random.uniform(alpha_up_ll,alpha_up_ul)
        #self.alpha_low_mfg= np.random.uniform(alpha_low_ll,alpha_low_ul)



        self.starttime=0                #time at which job enters the system
        self.endtime=0                 #time at which job exits the syst
        self.startprocessingtime=0      #time at which processing starts
        self.endprocessingtime=0        #time at which processing ends
        
        self.startreworktime=0          #time at which rework starts
        self.endreworktime=0            #time at which rework ends
        self.reworkduration=0
        
        self.final_processing_time = 0  #time till when 







        self.queue_state = 'initial'

    def put_job_in_queue(self, state):
        self.queue_state = state
        
    def rework(self):
        self.rework_times += 1
        
    def put_job_to(self, place, state):
        self.place = place  #can be queue or machine
        self.state = state

    def booked(self):
        self.state = 'booked'

    def save_startprocess_time(self, time):
        self.startprocessingtime = time

    def save_endprocess_time(self, time):
        self.endprocessingtime = time

    def save_endtime(self,time):
        self.endtime = time

    def save_starttime(self,time):
        self.starttime = time



    def calculate_duration(self):
        if self.rework_times==0:
        #if process == 'process_duration'
            self.processing_duration=self.endprocessingtime - self.startprocessingtime
            #.df_job['Processing_Time'].where(~(self.df_job.Job_number == event.job.id_num), other = event.job.processing_duration , inplace = True)
        else:
        #if process == 'rework'
            self.reworkduration=self.endprocessingtime-self.startprocessingtime
            #self.df_job['Rework Time'].where(~(self.df_job.Job_number == event.job.id_num), other = event.job.reworkduration , inplace = True)
        #something to append to these values to the job_df









class Queue:
    def __init__(self, name, q_type, capacity, place):
        self.name = name
        self.q_type = q_type
        self.capacity = capacity
        self.jobs_in_queue = []
        self.place = place  #the queue is place in front of what
        
    def add_job_to_queue(self, job):
        if self.capacity == 'infinite':
            print("FLAG 1") 
            self.jobs_in_queue.append(job)
        elif len(self.jobs_in_queue) <= self.capacity:
            print("FLAG 2")  
            self.jobs_in_queue.append(job)
        else:
            print('over crowded queue!')
            #this part not considered
    
    def depart_job_to_queue(self, job):
        self.jobs_in_queue.remove(job)
        print("Departure Job from Queue")
    
    def get_next_job_to_depart(self):
        temp=[]
        for item in self.jobs_in_queue:
            if item.state != 'booked':
                temp.append(item)
        if temp != []:
            next_job_to_depart = temp[0]
        else:
            next_job_to_depart = None
        return next_job_to_depart
    
    
    
class Machine:
    """
    Machine we have: harvesting, manufacturing
    """
    def __init__(self, name,id_num, m_type):
        self.name = name
        self.id_num = id_num
        self.m_type = m_type
        self.job = None
        self.operator = None
        self.state = 'idle'


    def start_setup(self, job, operator):
        self.job = job
        self.operator = operator
        self.state = 'setup'
        
    def end_setup(self):
        #self.job = None
        self.operator = None
        self.state = 'setup_end'        
        
    def start_work(self, operator):
        #self.job = job
        #self.operator = operator
        self.operator = None
        self.state = 'busy'
        
    def end_work(self):
        self.job = None
        self.operator = None
        self.state = 'idle'
        
    def booked(self):
        self.state = 'booked' #it is in queue and it is booked

    
    
class Operator:
    """
    Operator is defined as setup machine.
    """
    def __init__(self, name, id_num, o_type):
        self.name = name
        self.id_num = id_num
        self.o_type = o_type
        self.state = 'idle'
        
    def start_setup(self, job, machine):
        self.job = job
        self.machine = machine
        self.state = 'setup'
        
    def end_setup(self):
        self.job = None
        self.machine = None
        self.state = 'setup_end'        
        
    def start_work(self, job, machine):
        self.job = job
        self.machine = None
        self.state = 'idle' #can we put idle here for our case


    def collecting(self,time):
        self.state = 'busy'
    """    
    def end_work(self):
        self.job = None
        self.machine = None
        self.state = 'idle'
    """

    def end_work(self):
        self.job = None
        self.machine = None
        self.state = 'idle'



    def start_qc(self,job):
        self.job = job
        self.state = 'busy'
        
    def end_qc(self):
        self.job = None
        self.state = 'idle' #can we put idle here for our case      
       
    def booked(self):
        self.state = 'booked'

        
class Action:
    #not in use
    def __init__(self, name):
        self.name = name
