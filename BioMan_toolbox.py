#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: menghanliu
This is the file defining objects and tool functions.
"""
import pandas as pd
import numpy as np
import pyDOE2
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
    def __init__(self, name, id_num, place, conversion_factor, BV_m_LB, BV_m_HB, BV_f_LB, BV_f_HB, alpha_low_ll, alpha_low_ul, alpha_up_ll, alpha_up_ul, delta_ll, delta_ul):
        self.name = name
        self.id_num = id_num
        self.place = place  #can be queue or machine
        self.state = 'initial'   #can be initial, harvesting/ed, processing/ed, finished
        self.rework_times = 0
        self.process_yield = 0  #yield is 0 at initial and will be changed in processing
        self.BV_m_LB=BV_m_LB
        self.BV_m_HB=BV_m_HB 
        self.BV_f_LB=BV_f_LB 
        self.BV_f_HB=BV_f_HB 
        self.alpha_low_ll=alpha_low_ll
        self.alpha_low_ul=alpha_low_ul
        self.alpha_up_ll=alpha_up_ll 
        self.alpha_up_ul=alpha_up_ul 
        self.delta_ll=delta_ll
        self.delta_ul=delta_ul

        #gender generation
        flip = random.randint(0, 1)
        if (flip == 0):
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

        self.delta_mfg= np.random.uniform(delta_ll,delta_ul)
        self.alpha_up_mfg= np.random.uniform(alpha_up_ll,alpha_up_ul)
        self.alpha_low_mfg= np.random.uniform(alpha_low_ll,alpha_low_ul)
                
    def rework(self):
        self.rework_times += 1
        
    def put_job_to(self, place, state):
        self.place = place  #can be queue or machine
        self.state = state

    def booked(self):
        self.state = 'booked'
        
        
class Patient_Alpha_and_Delta:
    #used to generate alpha and delta values for each patient
    def __init__(self, name, id_num, place, conversion_factor, BV_m_LB, BV_m_HB, BV_f_LB, BV_f_HB):
        self.name = name
        self.id_num = id_num
        self.place = place  #can be queue or machine
        self.state = 'initial'   #can be initial, harvesting/ed, processing/ed, finished
        self.rework_times = 0
        self.process_yield = 0  #yield is 0 at initial and will be changed in processing




class Queue:
    def __init__(self, name, q_type, capacity, place):
        self.name = name
        self.q_type = q_type
        self.capacity = capacity
        self.jobs_in_queue = []
        self.place = place  #the queue is place in front of what
        
    def add_job_to_queue(self, job):
        if self.capacity == 'infinite':
            self.jobs_in_queue.append(job)
        elif len(self.jobs_in_queue) <= self.capacity:
            self.jobs_in_queue.append(job)
        else:
            print('over crowded queue!')
            #this part not considered
    
    def depart_job_to_queue(self, job):
        self.jobs_in_queue.remove(job)
    
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
    Machine we have: harvesting, 
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
        self.job = None
        self.operator = None
        self.state = 'setup_end'        
        
    def start_work(self, job, operator):
        self.job = job
        self.operator = operator
        self.state = 'busy'
        
    def end_work(self):
        self.job = None
        self.operator = None
        self.state = 'idle'
        
    def booked(self):
        self.state = 'booked'

    
    
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
        self.machine = machine
        self.state = 'busy'
        
    def end_work(self):
        self.job = None
        self.machine = None
        self.state = 'idle'
        
    def booked(self):
        self.state = 'booked'

        
class Action:
    #not in use
    def __init__(self, name):
        self.name = name
