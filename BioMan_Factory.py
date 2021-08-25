#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: menghanliu
This is the file containing main processes of the simulation.
This includes:
    (1)Patient arrival
    (2)Harvesting
    (3)Processing
    (4)Quality check
    (5)Finishing
"""

import BioMan_toolbox as toolbox
import pandas as pd
import numpy as np
import pyDOE2
import random


class Controller():
    """
    This is for the convenience of MCTS, not in use now.
    """
    def __init__(self, name, place, ):
        self.name = name
        
    def GetFeasibleActions(self, environment):
        
        return
    
    
        
    
    
class Environment():
    def __init__(self, Design):
        #self.df_this_design = pd.DataFrame()
        self.event_list = []
        self.clock = 0
        self.global_state = 'Initial'
        
        #self.Yield_Curve_MFG = Design[0]
        
        self.alphalow=Design[0]
        self.alphaup= Design[1]
        self.delta = Design[2]        
        self.Patient_Mix_MFG = Design[3]
        self.QM_Policy_MFG = Design[4]
        self.Hrv_Operators_Count, self.Hrv_Bioreactors_Count = self.num_of_hrv_operators_and_machine(Design[5],Design[6])
        #self.Hrv_Bioreactors_Count = self.num_of_hrv_machine()
        self.MFG_Operators_Count, self.MFG_Bioreactors_Count = self.num_of_mfg_operators_and_machine(Design[7],Design[8])
        #self.QC_Operators_Count= self.num_of_hrv_operators(Design[9])
        self.QC_Operators_Count=2#10# 100     
        

        #params
        self.patient_max_num = 2000  #maximum number of patients who can come for therapy
        self.patient_arrival_distribution = 'Uniform'
        self.conversion_factor = 140000   #blood count multiplication factor
        self.BV_m_LB = 5                  # lower bound of blood vol in male
        self.BV_m_HB = 7.5                # higher bound of blood vol in male
        self.BV_f_LB = 3.5                # lower bound of blood vol in female
        self.BV_f_HB = 6.0                # higher bound of blood vol in female
        self.time_budget_for_Arrival = 1000# 8760  #total time for patient arrival in a year's time
        #self.time_budget_for_Harvesting = 1000
        #self.time_budget_for_Processing = 1000
        self.Simulation_time_budget = 1000# 8760    #total time for patient arrival in a year's time
        """

    def num_of_hrv_operators(self,i):
        #Factor 4 corresponds to the harvesting operators count
        if i == 0:
            OPERATOR_HRV = 100#round(NUM_PATIENTS/15)
        elif i == 1:
            OPERATOR_HRV = 1000#round(NUM_PATIENTS/25)
        #as per new as on (08/01/2021) we are keeping it fixed    
        
        else:
            OPERATOR_HRV = 100#round(NUM_PATIENTS/35)
        
        return OPERATOR_HRV        
  

    def num_of_hrv_machine(self,i):
        #Factor 5 corresponds to the available harvesting machines count
        if i == 0:
            MACHINES_HRV = 100#round(NUM_PATIENTS/10)
        elif i == 1:
            MACHINES_HRV = 13#round(NUM_PATIENTS/20)
        #as per new as on(08/01/2021)we are keeping it fixed
        
        else:
            MACHINES_HRV = 100#round(2* NUM_PATIENTS/30)
        
        return MACHINES_HRV
        """
        
    def num_of_hrv_operators_and_machine(self,i,j):        
        #Factor 6 corresponds to the Mfg operators count 
        if j == 0:
            MACHINES_HRV = 2#round(NUM_PATIENTS/2)
        elif j == 1:
            MACHINES_HRV = 300#round(NUM_PATIENTS/5)


        if i == 0:
            OPERATOR_HRV = 1#MACHINES_HRV/3#round(NUM_PATIENTS/5)
        elif i == 1:
            OPERATOR_HRV = 3*MACHINES_HRV/4#round(NUM_PATIENTS/10)

        #as per new we are keep high and low
        """
        else:
            OPERATOR_MFG = 100#round(NUM_PATIENTS/20)
        """
        return OPERATOR_HRV, MACHINES_HRV
        
    def num_of_mfg_operators_and_machine(self,i,j):        
        #Factor 6 corresponds to the Mfg operators count 
        if j == 0:
            MACHINES_MFG = 100#round(NUM_PATIENTS/2)
        elif j == 1:
            MACHINES_MFG = 300#round(NUM_PATIENTS/5)


        if i == 0:
            OPERATOR_MFG = 3#MACHINES_MFG/20#round(NUM_PATIENTS/5)
        elif i == 1:
            OPERATOR_MFG = 3*MACHINES_MFG/4#round(NUM_PATIENTS/10)

        #as per new we are keep high and low
        """
        else:
            OPERATOR_MFG = 100#round(NUM_PATIENTS/20)
        """
        return OPERATOR_MFG, MACHINES_MFG
    """
        #not in use
    def num_of_mfg_machine(self,i):    
        #Factor 7 corresponds to the available Mfg machines(bio-reactors) count
        if i == 0:
            MACHINES_MFG = 100#round(NUM_PATIENTS/2)
        elif i == 1:
            MACHINES_MFG = 50#round(NUM_PATIENTS/5)
        #as per new we are keep high and low
                
        else:
            MACHINES_MFG = 100#round(NUM_PATIENTS)
        
        return MACHINES_MFG
    """

        #alpha_low_ll, alpha_low_ul,alpha_up_ll, alpha_up_ul alpha_up_mfg, delta_ll, delta_ul, low_level_factor_mfg, up_level_factor_mfg, separator_1, separator_2, QM_Policy_MFG
    	#def Factor_design(self, alpha_low_mfg, alpha_up_mfg, delta_t_mfg, low_level_factor_mfg, up_level_factor_mfg, separator_1, separator_2, QM_Policy_MFG):
    def Factor_design(self, alpha_low_ll, alpha_low_ul, alpha_up_ll, alpha_up_ul, delta_ll, delta_ul, low_level_factor_mfg, up_level_factor_mfg, relaxed_separator_1, relaxed_separator_2, stressed_separator_1, stressed_separator_2, prob_relax, QM_Policy_MFG):
    	self.alpha_low_ll= alpha_low_ll
    	self.alpha_low_ul= alpha_low_ul
    	self.alpha_up_ll= alpha_up_ll
    	self.alpha_up_ul= alpha_up_ul
    	self.delta_ll=delta_ll
    	self.delta_ul=delta_ul
    	self.low_level_factor_mfg=low_level_factor_mfg
    	self.up_level_factor_mfg=up_level_factor_mfg

    	self.relaxed_separator_1=relaxed_separator_1 
    	self.relaxed_separator_2=relaxed_separator_2 
    	self.stressed_separator_1=stressed_separator_1 
    	self.stressed_separator_2=stressed_separator_2 
    	self.prob_relax=prob_relax 
    	self.QM_Policy_MFG=QM_Policy_MFG
        
        
    def Machine_and_Operator_Setup(self):
        self.job_list = []  #Job is defined by patient arrival function 
        #name, q_type, capacity, place
        self.queue_1 = toolbox.Queue('queue_1', 'machine_queue_shared', 'infinite', 'harvest')
        self.queue_2 = toolbox.Queue('queue_2', 'machine_queue_shared', 'infinite', 'process')
        self.queue_3 = toolbox.Queue('queue_3', 'machine_queue_shared', 'infinite', 'qc')        
        self.hrv_operator_list = [toolbox.Operator('HO{}'.format(o+1), o+1, 'harvest') for o in range(0, int(self.Hrv_Operators_Count))]
        self.hrv_machine_list = [toolbox.Machine('HM{}'.format(m+1), m+1, 'harvest') for m in range(0, int(self.Hrv_Bioreactors_Count))]
        self.MFG_operator_list = [toolbox.Operator('PO{}'.format(o+1), o+1, 'process') for o in range(0, int(self.MFG_Operators_Count))]
        self.MFG_machine_list = [toolbox.Machine('PM{}'.format(m+1), m+1, 'process') for m in range(0, int(self.MFG_Bioreactors_Count))]
        self.QC_operator_list = [toolbox.Operator('QO{}'.format(q+1), q+1, 'qc') for q in range(0, int(self.QC_Operators_Count))]        
        self.finish_stack = []
        """
        Sets up the job list, mfg and hrv operators and machines  
        """
		
        

    def Take_action(self):
        """
        Not in use.
        """
        return


    def get_event(self):
        '''
        Gets the first event in the event table
        https://github.com/tkralphs/PyQueueSim/blob/master/QueueSim.py
        '''        
        #event = self.event_list.pop()
        #self.clock = event.e_happen_time
        
        temp = self.event_list[0]
        for item in self.event_list:
            if item.e_happen_time < temp.e_happen_time:
                temp = item
        event = temp
        self.event_list.remove(event)
        self.clock = event.e_happen_time
        
        return event


    def add_event(self, event):
        """
        Add event to event_list.
        """
        self.event_list.append(event)
        return
    
    
    def Simulate(self):
        """
        This is the simulation of the factory.
        """
        
        #Seting up
        #self.Factor_design
        self.Machine_and_Operator_Setup()
        
        #df writing
        self.df_this_design = pd.DataFrame(columns=['Clock', 'Event name', 'Event ID', 'Event happen time', 'Event place', 'Event machine', 'Event operator', 'Event job', 'Event rework times', 'Job yield', 
                                                    'hrv_operator_state_list', 'MFG_operator_state_list', 'QC_operator_state_list', 'hrv_machine_state_list', 'MFG_machine_state_list', 'queue_state_list', 'job_state_list',
                                                    'jobs_in_queue', 'jobs_in_rework', 'jobs_in_service','jobs_in_qc', 'jobs_in_completed', 'total_job_num'])
        
        #df to collect job datas
        self.df_job=pd.DataFrame(columns=['Job_number','Alpha_low_mfg','Alpha_up_mfg','Delta_mfg','Gender','Blood vol','Patient Trgt Bld Count'])    
        
        #first arrival
        new_job = toolbox.Job('J1', 1, self.queue_1, self.conversion_factor, self.BV_m_LB, self.BV_m_HB, self.BV_f_LB, self.BV_f_HB, self.alpha_low_ll, self.alpha_low_ul, self.alpha_up_ll, self.alpha_up_ul, self.delta_ll, self.delta_ul)
        
        #append job data to df_job
        to_append2 = [new_job.id_num] + [new_job.alpha_low_mfg] + [new_job.alpha_up_mfg] + [new_job.delta_mfg] + [new_job.gender] + [new_job.BV] + [new_job.patients_target_bc]
        b_series = pd.Series(to_append2, index = self.df_job.columns)
        self.df_job = self.df_job.append(b_series, ignore_index=True)
        
        #print(new_job.alpha_low_mfg)
        
        self.job_list.append(new_job)
        # Event: name, e_type, e_happen_time, place, machine, operator, job, rework_times
        first_event = toolbox.Event('patient {} arrival to queue_1'.format(new_job.id_num), 'Arrival', self.clock, self.queue_1, None, None, new_job, 0)
        self.add_event(first_event)
        
        #Simulation
        while self.clock <= self.Simulation_time_budget:
            print('******************************************************')
            print('Now event_list:')
            print('---------------')
            #for item in self.event_list:
            #    print(item.get_event_info())
            #print('---------------')
            
            if self.event_list == []:
                #print('Simulation finished, there is no more event.')
                #break
                to_append = [self.clock] + ['-','-','-', '-', '-', '-', '-', '-', '-'] + self.get_current_state() + self.get_job_state_statistics()
                self.clock +=1
            else:
                this_event = self.get_event()
                print('*Clock {}:*'.format(self.clock))
                print('\n')
                print('*This event:*', this_event.get_event_info())
                self.process_event(this_event)
                print('\n')
                #print('*Current state:*', self.get_current_state())
                to_append = [self.clock] + this_event.get_event_info() + self.get_current_state() + self.get_job_state_statistics()
                
            a_series = pd.Series(to_append, index = self.df_this_design.columns)
            self.df_this_design = self.df_this_design.append(a_series, ignore_index=True)
        print("Check before")
        return self.df_this_design, self.df_job


    def get_current_state(self):
        #get state info for the machine, operator,queue, job
        hrv_operator_state_list = [o.state for o in self.hrv_operator_list]
        MFG_operator_state_list = [o.state for o in self.MFG_operator_list]
        QC_operator_state_list = [o.state for o in self.QC_operator_list] #QC_operator_list
        hrv_machine_state_list = [m.state for m in self.hrv_machine_list]
        MFG_machine_state_list = [m.state for m in self.MFG_machine_list]
        #print(self.queue_1)
        queue_state_list = [self.queue_1.jobs_in_queue, self.queue_2.jobs_in_queue,self.queue_3.jobs_in_queue]
        job_state_list = [j.state for j in self.job_list]
        current_state_info = [hrv_operator_state_list, MFG_operator_state_list, QC_operator_state_list, hrv_machine_state_list, MFG_machine_state_list, queue_state_list, job_state_list]
        return current_state_info
        
    
    def get_available_operator(self, o_type):
        available_operator_set = []
        if o_type == 'harvest':
            for operator in self.hrv_operator_list:
                if operator.state == 'idle':
                    available_operator_set.append(operator)
        elif o_type == 'process':
            for operator in self.MFG_operator_list:
                if operator.state == 'idle':
                    available_operator_set.append(operator)
        elif o_type == 'qc':
            for operator in self.QC_operator_list:
                if operator.state == 'idle':
                    available_operator_set.append(operator)
        return available_operator_set

        
        
    def get_available_machine(self, m_type):
        available_machine_set = []
        if m_type == 'harvest':
            for machine in self.hrv_machine_list:
                if machine.state == 'idle':
                    available_machine_set.append(machine)
        elif m_type == 'process':
            for machine in self.MFG_machine_list:
                if machine.state == 'idle':
                    available_machine_set.append(machine)
        return available_machine_set
        
    
    def get_job_state_statistics(self):
        jobs_in_queue = 0
        jobs_in_rework = 0
        jobs_in_service = 0
        jobs_in_completed = 0
        jobs_in_qc = 0
        for item in self.job_list:
            #print('job state', item.state)
            if item.state == 'Finished':
                jobs_in_completed +=1
                #print('jobs_in_completed:',jobs_in_completed)
            elif item.state == 'in queue' or item.state =='booked' or item.state == 'initial':
                jobs_in_queue +=1
                #print('jobs_in_queue:', jobs_in_queue)
            elif item.state == 'harvesting':
                jobs_in_service +=1
                #print('jobs_in_service:', jobs_in_service)
            elif item.state == 'processing' or item.state =='setup':
                if item.rework_times==0:
                    jobs_in_service +=1
                    #print('jobs_in_service:', jobs_in_service)
                else:
                    jobs_in_rework +=1
                    #print('jobs_in_rework:', jobs_in_rework)
            elif item.state == 'qc':
                jobs_in_qc+=1

        total_job_num = len(self.job_list)
        job_state_stats = [jobs_in_queue, jobs_in_rework, jobs_in_service, jobs_in_qc, jobs_in_completed, total_job_num]
        #print('job_state_stats:',job_state_stats)
        return job_state_stats
    
    
    def process_event(self, event):
        """
        Process the event and schedule the next.
        """
        if event.e_type == 'Arrival':
            #includes arrival to queue and machine
            if event.place == self.queue_1:
                #process event
                self.queue_1.add_job_to_queue(event.job)
                event.job.put_job_to(self.queue_1, 'in queue')
                #schedule next arrival
                if len(self.job_list) <= self.patient_max_num and self.clock <= self.time_budget_for_Arrival:
                    inter_arrival_time = np.random.randint(4, 10)
                    next_new_job = toolbox.Job('J{}'.format(event.job.id_num +1),event.job.id_num +1, self.queue_1, self.conversion_factor, self.BV_m_LB, self.BV_m_HB, self.BV_f_LB, self.BV_f_HB,  self.alpha_low_ll, self.alpha_low_ul, self.alpha_up_ll, self.alpha_up_ul, self.delta_ll, self.delta_ul)
                	
                	#append job data to df_job
                    to_append2 = [next_new_job.id_num] + [next_new_job.alpha_low_mfg] + [next_new_job.alpha_up_mfg] + [next_new_job.delta_mfg] + [next_new_job.gender] + [next_new_job.BV] + [next_new_job.patients_target_bc]
                    b_series = pd.Series(to_append2, index = self.df_job.columns)
                    self.df_job = self.df_job.append(b_series, ignore_index=True)
               
                    self.job_list.append(next_new_job)
                    #first_event = toolbox.Event('patient {} arrival to queue_1'.format(new_job.id_num), 'Arrival', self.clock, self.queue_1, None, None, new_job, 0)
                    next_arrival_event = toolbox.Event('patient {} arrival to queue_1'.format(next_new_job.id_num), 'Arrival', self.clock+inter_arrival_time, self.queue_1, None, None, next_new_job, 0)
                    self.add_event(next_arrival_event)
                #Go to harvest operator if feasible
                if self.get_available_operator('harvest') != [] and self.get_available_machine('harvest') != []:
                    chosen_operator = random.choice(self.get_available_operator('harvest'))
                    chosen_machine = random.choice(self.get_available_machine('harvest'))
                    #depart
                    next_event = toolbox.Event('patient {} depart queue_1'.format(event.job.id_num), 'Departure', self.clock, self.queue_1, chosen_machine, chosen_operator, event.job, event.rework_times)
                    event.job.booked()
                    chosen_operator.booked()
                    chosen_machine.booked()
                    self.add_event(next_event)
            elif event.place == self.queue_2:
                #process event
                self.queue_2.add_job_to_queue(event.job)
                event.job.put_job_to(self.queue_2, 'in queue')
                #go to process operator if feasible
                if self.get_available_operator('process') != [] and self.get_available_machine('process') != []:
                    chosen_operator = random.choice(self.get_available_operator('process'))
                    chosen_machine = random.choice(self.get_available_machine('process'))
                    #depart
                    next_event = toolbox.Event('patient {} depart queue_1'.format(event.job.id_num), 'Departure', self.clock, self.queue_2, chosen_machine, chosen_operator, event.job, event.rework_times)
                    event.job.booked()
                    chosen_operator.booked()
                    chosen_machine.booked()
                    self.add_event(next_event)
                    
            elif event.place == self.queue_3:
                self.queue_3.add_job_to_queue(event.job)
                event.job.put_job_to(self.queue_3, 'in queue')
                #go to qc operator if feasible
                if self.get_available_operator('qc') != []:
                    chosen_operator = random.choice(self.get_available_operator('qc'))
                    #chosen_machine = random.choice(self.get_available_machine('process'))
                    #depart
                    next_event = toolbox.Event('patient {} depart queue_3'.format(event.job.id_num), 'Departure', self.clock, self.queue_3, None, chosen_operator, event.job, event.rework_times)
                    event.job.booked()
                    chosen_operator.booked()
                    #chosen_machine.booked()
                    self.add_event(next_event)
                    

        
        elif event.e_type == 'Departure':
            if event.place == self.queue_1:
                #process event
                self.queue_1.depart_job_to_queue(event.job)
                #schedule go to harvest operator setup
                next_event = toolbox.Event('patient {} Start harvest setup'.format(event.job.id_num), 'Start_setup', self.clock, event.operator, event.machine, event.operator, event.job, event.rework_times)
                self.add_event(next_event)
            elif event.place == self.queue_2:
                #process event
                self.queue_2.depart_job_to_queue(event.job)
                #schedule go to process operator setup
                next_event = toolbox.Event('patient {} Start process setup'.format(event.job.id_num), 'Start_setup', self.clock, event.operator, event.machine, event.operator, event.job, event.rework_times)
                self.add_event(next_event)
            elif event.place == self.queue_3:
                #process event
                self.queue_3.depart_job_to_queue(event.job)
                #schedule go to process operator setup
                next_event = toolbox.Event('patient {} Quality check'.format(event.job.id_num), 'Start_Quality_Check', self.clock, event.operator, event.machine, event.operator, event.job, event.rework_times)
                self.add_event(next_event)

            
        elif event.e_type == 'Start_setup':
            if event.machine.m_type == 'harvest':
                #process event
                event.job.put_job_to(event.operator, 'setup')
                event.operator.start_setup(event.job, event.machine)
                event.machine.start_setup(event.job, event.operator)
                #schedule next
                setup_duration = np.random.randint(1, 3)
                next_event = toolbox.Event('patient {} End harvest setup'.format(event.job.id_num), 'End_setup', self.clock+setup_duration, event.place, event.machine, event.operator, event.job, event.rework_times)
                self.add_event(next_event)
                
            elif event.machine.m_type == 'process':
                #process event
                event.job.put_job_to(event.operator, 'setup')
                event.operator.start_setup(event.job, event.machine)
                event.machine.start_setup(event.job, event.operator)
                setup_duration = np.random.uniform(5, 8)
                next_event = toolbox.Event('patient {} End process setup'.format(event.job.id_num), 'End_setup', self.clock+setup_duration, event.place, event.machine, event.operator, event.job, event.rework_times)
                self.add_event(next_event)
         
        elif event.e_type == 'End_setup':
            if event.machine.m_type == 'harvest':
                #process event
                event.operator.end_setup()
                event.machine.end_setup()
                #schedule next
                next_event = toolbox.Event('patient {} Start harvesting'.format(event.job.id_num), 'Start_harvesting', self.clock, event.machine, event.machine, event.operator, event.job, event.rework_times)
                self.add_event(next_event)
                
            elif event.machine.m_type == 'process':
                #process event
                event.operator.end_setup()
                event.machine.end_setup()
                #schedule next
                next_event = toolbox.Event('patient {} Start processing'.format(event.job.id_num), 'Start_processing', self.clock, event.machine, event.machine, event.operator, event.job, event.rework_times)
                self.add_event(next_event)
                
        elif event.e_type == 'Start_harvesting':
            #need to schedule end event and duration
            #process event
            event.job.put_job_to(event.machine, 'harvesting')
            event.operator.start_work(event.job, event.machine)
            event.machine.start_work(event.operator)
            #schedule next
            harvest_duration = np.random.randint(6, 9)
            harvest_yield = event.job.patients_target_bc * 0.8
            event.job.process_yield = harvest_yield
            next_event = toolbox.Event('patient {} End harvesting'.format(event.job.id_num), 'End_harvesting', self.clock+harvest_duration, event.place, event.machine, event.operator, event.job, event.rework_times)
            self.add_event(next_event)
            
        elif event.e_type == 'End_harvesting':
            #process event
            #event.operator.end_work()
            event.machine.end_work()
            #schedule next
            next_event = toolbox.Event('patient {} arrival to queue_2'.format(event.job.id_num), 'Arrival', self.clock, self.queue_2, None, None, event.job, event.rework_times)
            self.add_event(next_event)
            #if end one, schedule a departure on queue_1
            if self.get_available_operator('harvest') != [] and self.get_available_machine('harvest') != [] and self.queue_1.get_next_job_to_depart() != None:
                chosen_operator = random.choice(self.get_available_operator('harvest'))
                chosen_machine = random.choice(self.get_available_machine('harvest'))
                next_job_to_dpt = self.queue_1.get_next_job_to_depart()
                #def __init__(self, name, e_type, e_happen_time, place, machine, operator, job, rework_times
                next_event = toolbox.Event('patient {} depart queue_1'.format(next_job_to_dpt.id_num), 'Departure', self.clock, self.queue_1, chosen_machine, chosen_operator, next_job_to_dpt, event.rework_times)
                event.job.booked()
                chosen_operator.booked()
                chosen_machine.booked()
                self.add_event(next_event)

        elif event.e_type == 'Start_processing':
            #process event
            event.job.put_job_to(event.machine, 'processing')
            event.operator.start_work(event.job, event.machine)
            #changing the operator end work to idle
            event.machine.start_work(event.operator)
            #schedule next
            #bc = event.job.patients_target_bc
            bc = event.job.process_yield
            #TRIAL
            print(event.job.id_num)
            process_duration, this_process_yield = self.Processing_Machine_process_duration_and_yield_calculation(bc,event)
            event.job.process_yield = this_process_yield
            next_event = toolbox.Event('patient {} End processing'.format(event.job.id_num), 'End_processing', self.clock+process_duration, event.place, event.machine, event.operator, event.job, event.rework_times)
            #new function of job to save time of completion 
            p_time=self.clock+process_duration
            event.job.save_process_time(p_time)
            self.add_event(next_event)
            
        elif event.e_type == 'End_processing':
            #process event
            #event.operator.end_work()
            event.machine.end_work()

#Refer to meeting on 08/11/2021

            #chose_operator = random.choice(self.get_available_operator('process')) # or harvesting operator as well??
            #chose_operator.qc_()
            #schedule next
            #'patient {}'.format(event.job.id_num), 'Arrival', self.clock, self.queue_2, None, None, event.job, event.rework_times
            
            if self.get_available_operator('process') != []:
                #calculate yield again
                if self.clock != event.job.processingtime:
                    temp_yield=event.job.process_yield
                    event.job.process_yield=temp_yield-np.random.uniform(event.job.alpha_up_mfg*(self.clock-event.job.processingtime)*(1-0.5*10**(-3)),event.job.alpha_up_mfg*(self.clock-event.job.processingtime)*(1+0.5*10**(-3)))
                    #y3_mfg = bc - event.job.alpha_up_mfg*max(0,t_up_new_mfg-t_up_mfg)          (y3_mfg*(1-0.5*10**(-3)),y3_mfg*(1+0.5*10**(-3)
                    event.job.alpha_up_mfg*(self.clock-event.job.processingtime)
                    #np.random.uniform(y1_mfg*(1-0.5*10**(-3)),y1_mfg*(1+0.5*10**(-3)))

                next_event = toolbox.Event('patient {} arrival to queue_3'.format(event.job.id_num), 'Arrival', self.clock, self.queue_3, None, None, event.job, event.rework_times)
                self.add_event(next_event)

                
            #if end one, schedule a departure on queue_2
            if self.get_available_operator('process') != [] and self.get_available_machine('process') != [] and self.queue_2.get_next_job_to_depart() != None:
                chosen_operator = random.choice(self.get_available_operator('process'))
                chosen_machine = random.choice(self.get_available_machine('process'))
                next_job_to_dpt = self.queue_2.get_next_job_to_depart()
                next_event = toolbox.Event('patient {} depart queue_2'.format(next_job_to_dpt.id_num), 'Departure', self.clock, self.queue_2, chosen_machine, chosen_operator, next_job_to_dpt, event.rework_times)
                event.job.booked()
                chosen_operator.booked()
                chosen_machine.booked()
                self.add_event(next_event)


        elif event.e_type == 'Start_Quality_Check':
            #process event
            event.job.put_job_to(event.operator, 'qc')
            event.operator.start_qc(event.job)
            #changing the operator end work to idle
            #event.machine.start_work(event.operator)
            qc_duration = np.random.uniform(1, 2) 
            #schedule next
            print(event.job.id_num)
            next_event = toolbox.Event('patient {} Quality Check'.format(event.job.id_num), 'Quality_check', self.clock, event.place, event.machine, event.operator, event.job, event.rework_times)
            self.add_event(next_event)
            
        elif event.e_type == 'Quality_check':
            event.operator.end_qc()
            #event.job.put_job_to(None, 'Finish')
            qc_duration = np.random.uniform(1, 2) 
            #schedule next
            #print(event.job.id_num)
            next_event = toolbox.Event('patient {} End Quality Check'.format(event.job.id_num), 'End_Quality_check', self.clock+qc_duration, event.place, event.machine, event.operator, event.job, event.rework_times)
            self.add_event(next_event)
           

        elif event.e_type == 'End_Quality_check':
            #process event
            test_result = self.quality_policy(self.QM_Policy_MFG, event.job)
            #print('test result on job {}:'.format(event.job.name), test_result)
            if test_result in ("Sample Rejected", "Rejected in LF and HF Both"):
                #if fail the check, rework, arrival to queue_2
                event.job.rework()
                next_event = toolbox.Event('patient {} arrival to queue_2'.format(event.job.id_num), 'Arrival', self.clock, self.queue_2, None, None, event.job, event.rework_times+1)
                self.add_event(next_event)
            else:
                #if success, leave the system
                next_event = toolbox.Event('patient {} leaves the system'.format(event.job.id_num), 'Finish', self.clock, 'finish_stack', None, None, event.job, event.rework_times)
                self.add_event(next_event)
                
        elif event.e_type == 'Finish':
            event.job.put_job_to(self.finish_stack, 'Finished')
            self.finish_stack.append(event.job)
            print('***Job {} finished!***'.format(event.job.id_num))
        

    def Processing_Machine_process_duration_and_yield_calculation(self, bc, event):
        """
        This is the calculation of processing duration and yield.
        """
        print(self.job_list)
        t_low_mfg = bc/event.job.alpha_low_mfg
        t_up_mfg = t_low_mfg + event.job.delta_mfg
        t_low_new_mfg = t_low_mfg*self.low_level_factor_mfg
        t_up_new_mfg = t_up_mfg*self.up_level_factor_mfg
        t_normal_mfg = (t_up_new_mfg+t_low_new_mfg)/2
        
        y1_mfg = event.job.alpha_low_mfg * t_low_new_mfg #1.2*self.alpha_low_mfg * t_low_new_mfg #very good patients
        y2_mfg = bc #normal patient 
        y3_mfg = bc - event.job.alpha_up_mfg*max(0,t_up_new_mfg-t_up_mfg)

        #randomly choose whether the patient is treated in a relaxed or stressed environment
        coin_toss= np.random.uniform(0,1)
        print(self.prob_relax)
        if (coin_toss<=self.prob_relax):
        	separator_1=self.relaxed_separator_1
        	separator_2=self.relaxed_separator_2
        elif (coin_toss>self.prob_relax):
        	separator_1=self.stressed_separator_1
        	separator_2=self.stressed_separator_2

        """
        U_3_mfg = np.random.uniform(0, 1)
        if (U_3_mfg <= 0.90):
            y3_mfg = bc
        else:
            y3_mfg = bc - self.alpha_up_mfg*max(0,t_up_new_mfg-t_up_mfg) #poor yield patient
    """
        #patient mix coin flip

        #patient mix for some patients should be relaxed and stressed for some
        
        s = np.random.uniform(0, 1)
        if (s <= separator_1):
            p_duration = t_low_new_mfg*24
            #p_yield = y1_mfg
            p_yield = np.random.uniform(y1_mfg*(1-0.5*10**(-3)),y1_mfg*(1+0.5*10**(-3)))

        elif (separator_1 < s <= separator_2):
            p_duration = t_normal_mfg*24
            #p_yield = y2_mfg
            p_yield = np.random.uniform(y2_mfg*(1-0.5*10**(-3)),y2_mfg*(1+0.5*10**(-3)))

        else:
            p_duration = t_up_new_mfg*24
            #p_yield = y3_mfg
            p_yield = np.random.uniform(y3_mfg*(1-0.5*10**(-3)),y3_mfg*(1+0.5*10**(-3)))

            
        return p_duration, p_yield


    #Testing policy
    def high_fidelity_test_case_A(self):
        P_1_HF = 0.99   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
        P_2_HF = 0.10   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
        P_3_HF = 0.65   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)

        #calculating P(Y'>= Y* / Ytilda>= Y*) 
        #i.e. proability of measured yield being more than expected yield given calculated yield is more than expected
        #P(Y'>= Y* / Ytilda>= Y*)  = P(Ytilda >= Y* / Y' >= Y*) * P(Y' >= Y*) / [P(Ytilda >= Y* / Y' >= Y*) * P(Y' >= Y*) + P(Ytilda >= Y* / Y' < Y*) * P(Y' < Y*)]
        alpha_HF = 0.95#(P_1_HF * P_3_HF) / (P_1_HF * P_3_HF + P_2_HF * (1 - P_3_HF))  = 0.6785
        U1 = np.random.uniform(0, 1)
        if (U1 <= alpha_HF):
            Test_Result = 'Sample Passed'
        else:
            Test_Result = 'Sample Rejected'
        return Test_Result
        
    def high_fidelity_test_case_B(self):
        P_1_HF = 0.99   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
        P_2_HF = 0.10   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
        P_3_HF = 0.65   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)
        Beta_HF = 0.9#((1-P_1_HF)* P_3_HF) / (((1-P_1_HF)* P_3_HF) + ((1-P_2_HF)*(1-P_3_HF))) =  0.02021772
        U2 = np.random.uniform(0, 1) 
        if (U2 <= Beta_HF):
            Test_Result = 'Sample Passed'    #It was fail, but Test confirms Pass
        else:
            Test_Result = 'Sample Rejected'  #It was fail, Test Confirms Fail
        return Test_Result

    def low_fidelity_test_case_A(self):
        P_1_LF = 0.85   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
        P_2_LF = 0.45   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
        P_3_LF = 0.40   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)
        #calculating P(Y'>= Y* / Ytilda < Y*)
        alpha_LF = 0.9#(P_1_LF * P_3_LF) / (P_1_LF * P_3_LF + P_2_LF * (1 - P_3_LF)) = 0.55737704
        U3 = np.random.uniform(0, 1)
        if (U3 <= alpha_LF):
            Test_Result = 'Sample Passed'
        else:
            Test_Result = 'Sample Rejected'
        return Test_Result

    def low_fidelity_test_case_B(self):
        P_1_LF = 0.85   #P(Ytilda >= Y* / Y' >= Y*) #P(viable/Test = Positive)
        P_2_LF = 0.45   #P(Ytilda >= Y* / Y' < Y*)  #P(viable/Test = Negative)
        P_3_LF = 0.40   #P(Y' >= Y*) #P(Measured Yield < Expected Yield)
        Beta_LF = 0.95#((1-P_1_LF)* P_3_LF) / (((1-P_1_LF)* P_3_LF) + ((1-P_2_LF)*(1-P_3_LF))) = 0.15384615
        U4 = np.random.uniform(0, 1)
        if (U4 <= Beta_LF):
            Test_Result = 'Sample Passed'    #It was fail, but Test confirms Pass
        else:
            Test_Result = 'Sample Rejected'  #It was fail, Test Confirms Fail
        return Test_Result


    def quality_policy(self, QM_Policy_MFG, job):

        #defining level for each quality control policy
        #Test happens according to that level and the results are recorded
        Test_Result='Default result'
        process_yield = job.process_yield
        patients_target_bc =job.patients_target_bc
        if QM_Policy_MFG == 0:
            #test everything in high fidelity
            #Case A
            if (process_yield >= patients_target_bc):
                Test_Result=self.high_fidelity_test_case_A()
            #Case B
            else:
                Test_Result=self.high_fidelity_test_case_B()


        elif QM_Policy_MFG == 1:
            #test everything in low fidelity and if test fails then check again in high fidelity
            #Case A
            if (process_yield >= patients_target_bc):
                Test_Result = self.low_fidelity_test_case_A() 
                if Test_Result == "Sample Rejected":
                    Test_Result = self.high_fidelity_test_case_A()
                    if Test_Result == "Sample Rejected":
                        Test_Result = "Rejected in LF and HF Both"
                    else:
                        Test_Result = "Rejected in LF but Passed in HF"
            #Case B
            else:
                Test_Result= self.low_fidelity_test_case_B()
                if Test_Result == "Sample Rejected":
                    Test_Result = self.high_fidelity_test_case_B()
                    if Test_Result == "Sample Rejected":
                        Test_Result = "Rejected in LF and HF Both"
                    else:
                        Test_Result = "Rejected in LF, Passed in HF"

                        
        else:
            U5 = np.random.uniform(0, 1)
            if (U5 <= 0.70):
                if (process_yield >= patients_target_bc):
                    Test_Result=self.high_fidelity_test_case_A()
                else:
                    Test_Result=self.high_fidelity_test_case_B()
            else:
                Test_Result= "Proceeding Sample without contamination"
                
        return Test_Result


