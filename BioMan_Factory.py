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

#edit 1

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
        self.Hrv_Operators_Count = self.num_of_hrv_operators(Design[5])
        self.Hrv_Bioreactors_Count = self.num_of_hrv_machine(Design[6])
        self.MFG_Operators_Count = self.num_of_mfg_operators(Design[7])
        self.MFG_Bioreactors_Count = self.num_of_mfg_machine(Design[8])
        #self.Patient_Mix_MFG = Design[1]
        #self.QM_Policy_MFG = Design[2]
        

        """
        self.Hrv_Operators_Count = Design[3]
        self.Hrv_Bioreactors_Count = Design[4]
        self.MFG_Operators_Count = Design[5]
        self.MFG_Bioreactors_Count = Design[6]
        """
        #params
        self.patient_max_num = 1000
        self.patient_arrival_distribution = 'Uniform'
        self.conversion_factor = 140000
        self.BV_m_LB = 5
        self.BV_m_HB = 7.5
        self.BV_f_LB = 3.5
        self.BV_f_HB = 6.0
        self.time_budget_for_Arrival = 8760
        #self.time_budget_for_Harvesting = 1000
        #self.time_budget_for_Processing = 1000
        self.Simulation_time_budget = 8760
        
    def num_of_hrv_operators(self,i):
        #Factor 4 corresponds to the harvesting operators count
        if i == 0:
            OPERATOR_HRV = 160#round(NUM_PATIENTS/15)
        elif i == 1:
            OPERATOR_HRV = 50#round(NUM_PATIENTS/25)
        else:
            OPERATOR_HRV = 100#round(NUM_PATIENTS/35)
        return OPERATOR_HRV

    def num_of_hrv_machine(self,i):
        #Factor 5 corresponds to the available harvesting machines count
        if i == 0:
            MACHINES_HRV = 160#round(NUM_PATIENTS/10)
        elif i == 1:
            MACHINES_HRV = 50#round(NUM_PATIENTS/20)
        else:
            MACHINES_HRV = 100#round(2* NUM_PATIENTS/30)
        return MACHINES_HRV

    def num_of_mfg_operators(self,i):        
        #Factor 6 corresponds to the Mfg operators count 
        if i == 0:
            OPERATOR_MFG = 160#round(NUM_PATIENTS/5)
        elif i == 1:
            OPERATOR_MFG = 50#round(NUM_PATIENTS/10)
        else:
            OPERATOR_MFG = 100#round(NUM_PATIENTS/20)
        return OPERATOR_MFG

    def num_of_mfg_machine(self,i):    
        #Factor 7 corresponds to the available Mfg machines(bio-reactors) count
        if i == 0:
            MACHINES_MFG = 160#round(NUM_PATIENTS/2)
        elif i == 1:
            MACHINES_MFG = 50#round(NUM_PATIENTS/5)
        else:
            MACHINES_MFG = 100#round(NUM_PATIENTS)
        return MACHINES_MFG



    def Factor_design(self, alpha_low_mfg, alpha_up_mfg, delta_t_mfg, low_level_factor_mfg, up_level_factor_mfg, separator_1, separator_2, QM_Policy_MFG):
        self.alpha_low_mfg= alpha_low_mfg
        self.alpha_up_mfg= alpha_up_mfg
        self.delta_t_mfg=delta_t_mfg
        self.low_level_factor_mfg=low_level_factor_mfg
        self.up_level_factor_mfg=up_level_factor_mfg
        self.separator_1=separator_1
        self.separator_2=separator_2
        self.QM_Policy_MFG=QM_Policy_MFG
        
        
    def Machine_and_Operator_Setup(self):
        self.job_list = []  #Job is defined by patient arrival function.
        self.queue_1 = toolbox.Queue('queue_1', 'machine_queue_shared', 'infinite', 'harvest')
        self.queue_2 = toolbox.Queue('queue_2', 'machine_queue_shared', 'infinite', 'process')
        self.hrv_operator_list = [toolbox.Operator('HO{}'.format(o+1), o+1, 'harvest') for o in range(0, int(self.Hrv_Operators_Count))]
        self.hrv_machine_list = [toolbox.Machine('HM{}'.format(m+1), m+1, 'harvest') for m in range(0, int(self.Hrv_Bioreactors_Count))]
        self.MFG_operator_list = [toolbox.Operator('PO{}'.format(o+1), o+1, 'process') for o in range(0, int(self.MFG_Operators_Count))]
        self.MFG_machine_list = [toolbox.Machine('PM{}'.format(m+1), m+1, 'process') for m in range(0, int(self.MFG_Bioreactors_Count))]


        #self.hrv_operator_list = [toolbox.Operator('HO{}'.format(o+1), o+1, 'harvest') for o in range(0, self.Hrv_Operators_Count)]
        #self.hrv_machine_list = [toolbox.Machine('HM{}'.format(m+1), m+1, 'harvest') for m in range(0, self.Hrv_Bioreactors_Count)]
        #self.MFG_operator_list = [toolbox.Operator('PO{}'.format(o+1), o+1, 'process') for o in range(0, self.MFG_Operators_Count)]
        #self.MFG_machine_list = [toolbox.Machine('PM{}'.format(m+1), m+1, 'process') for m in range(0, self.MFG_Bioreactors_Count)]
        self.finish_stack = []
        

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
                                                    'hrv_operator_state_list', 'MFG_operator_state_list', 'hrv_machine_state_list', 'MFG_machine_state_list', 'queue_state_list', 'job_state_list',
                                                    'jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_completed', 'total_job_num'])
            
        #first arrival
        new_job = toolbox.Job('J1', 1, self.queue_1, self.conversion_factor, self.BV_m_LB, self.BV_m_HB, self.BV_f_LB, self.BV_f_HB)
        self.job_list.append(new_job)
        first_event = toolbox.Event('patient {} arrival to queue_1'.format(new_job.id_num), 'Arrival', self.clock, self.queue_1, None, None, new_job, 0)
        self.add_event(first_event)
        
        #Simulation
        while self.clock <= self.Simulation_time_budget:
            print('******************************************************')
            print('Now event_list:')
            print('---------------')
            for item in self.event_list:
                print(item.get_event_info())
            print('---------------')
            
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
                print('*Current state:*', self.get_current_state())
                to_append = [self.clock] + this_event.get_event_info() + self.get_current_state() + self.get_job_state_statistics()
                
            a_series = pd.Series(to_append, index = self.df_this_design.columns)
            self.df_this_design = self.df_this_design.append(a_series, ignore_index=True)
            
        #print('Simulation finished due to time budget reached.')
        return self.df_this_design


    def get_current_state(self):
        #get state info for the machine, operator,queue, job
        hrv_operator_state_list = [o.state for o in self.hrv_operator_list]
        MFG_operator_state_list = [o.state for o in self.MFG_operator_list]
        hrv_machine_state_list = [m.state for m in self.hrv_machine_list]
        MFG_machine_state_list = [m.state for m in self.MFG_machine_list]
        queue_state_list = [self.queue_1.jobs_in_queue, self.queue_2.jobs_in_queue]
        job_state_list = [j.state for j in self.job_list]
        current_state_info = [hrv_operator_state_list, MFG_operator_state_list, hrv_machine_state_list, MFG_machine_state_list, queue_state_list, job_state_list]
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
        total_job_num = len(self.job_list)
        job_state_stats = [jobs_in_queue, jobs_in_rework, jobs_in_service, jobs_in_completed, total_job_num]
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
                    next_new_job = toolbox.Job('J{}'.format(event.job.id_num +1),event.job.id_num +1, self.queue_1, self.conversion_factor, self.BV_m_LB, self.BV_m_HB, self.BV_f_LB, self.BV_f_HB)
                    self.job_list.append(next_new_job)
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
            event.machine.start_work(event.job, event.operator)
            #schedule next
            harvest_duration = np.random.randint(6, 9)
            harvest_yield = event.job.patients_target_bc * 0.8
            event.job.process_yield = harvest_yield
            next_event = toolbox.Event('patient {} End harvesting'.format(event.job.id_num), 'End_harvesting', self.clock+harvest_duration, event.place, event.machine, event.operator, event.job, event.rework_times)
            self.add_event(next_event)
            
        elif event.e_type == 'End_harvesting':
            #process event
            event.operator.end_work()
            event.machine.end_work()
            #schedule next
            next_event = toolbox.Event('patient {} arrival to queue_2'.format(event.job.id_num), 'Arrival', self.clock, self.queue_2, None, None, event.job, event.rework_times)
            self.add_event(next_event)
            #if end one, schedule a departure on queue_1
            if self.get_available_operator('harvest') != [] and self.get_available_machine('harvest') != [] and self.queue_1.get_next_job_to_depart() != None:
                chosen_operator = random.choice(self.get_available_operator('harvest'))
                chosen_machine = random.choice(self.get_available_machine('harvest'))
                next_job_to_dpt = self.queue_1.get_next_job_to_depart()
                next_event = toolbox.Event('patient {} depart queue_1'.format(next_job_to_dpt.id_num), 'Departure', self.clock, self.queue_1, chosen_machine, chosen_operator, next_job_to_dpt, event.rework_times)
                event.job.booked()
                chosen_operator.booked()
                chosen_machine.booked()
                self.add_event(next_event)

        elif event.e_type == 'Start_processing':
            #process event
            event.job.put_job_to(event.machine, 'processing')
            event.operator.start_work(event.job, event.machine)
            event.machine.start_work(event.job, event.operator)
            #schedule next
            #bc = event.job.patients_target_bc
            bc = event.job.process_yield
            process_duration, this_process_yield = self.Processing_Machine_process_duration_and_yield_calculation(bc)
            event.job.process_yield = this_process_yield
            next_event = toolbox.Event('patient {} End processing'.format(event.job.id_num), 'End_processing', self.clock+process_duration, event.place, event.machine, event.operator, event.job, event.rework_times)
            self.add_event(next_event)
            
        elif event.e_type == 'End_processing':
            #process event
            event.operator.end_work()
            event.machine.end_work()
            #schedule next
            next_event = toolbox.Event('patient {} Quality check'.format(event.job.id_num), 'Quality_check', self.clock, 'quality check, no place', None, None, event.job, event.rework_times)
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
            
        elif event.e_type == 'Quality_check':
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
        

    def Processing_Machine_process_duration_and_yield_calculation(self, bc):
        """
        This is the calculation of processing duration and yield.
        """
        t_low_mfg = bc/self.alpha_low_mfg
        t_up_mfg = t_low_mfg + self.delta_t_mfg
        t_low_new_mfg = t_low_mfg*self.low_level_factor_mfg
        t_up_new_mfg = t_up_mfg*self.up_level_factor_mfg
        t_normal_mfg = (t_up_new_mfg+t_low_new_mfg)/2
        
        y1_mfg = self.alpha_low_mfg * t_low_new_mfg #1.2*self.alpha_low_mfg * t_low_new_mfg #very good patients
        
        y2_mfg = bc #normal patient 
        y3_mfg = bc - self.alpha_up_mfg*max(0,t_up_new_mfg-t_up_mfg)
        """
        U_3_mfg = np.random.uniform(0, 1)
        if (U_3_mfg <= 0.90):
            y3_mfg = bc
        else:
            y3_mfg = bc - self.alpha_up_mfg*max(0,t_up_new_mfg-t_up_mfg) #poor yield patient
    """
        #patient mix coin flip
        s = np.random.uniform(0, 1)
        if (s <= self.separator_1):
            p_duration = t_low_new_mfg*24
            #p_yield = y1_mfg
            p_yield = np.random.uniform(y1_mfg*(1-0.5*10**(-3)),y1_mfg*(1+0.5*10**(-3)))

        elif (self.separator_1 < s <= self.separator_2):
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
        alpha_HF = 0.95#(P_1_HF * P_3_HF) / (P_1_HF * P_3_HF + P_2_HF * (1 - P_3_HF))
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
        Beta_HF = 0.9#((1-P_1_HF)* P_3_HF) / (((1-P_1_HF)* P_3_HF) + ((1-P_2_HF)*(1-P_3_HF)))
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
        alpha_LF = 0.9#(P_1_LF * P_3_LF) / (P_1_LF * P_3_LF + P_2_LF * (1 - P_3_LF))
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
        Beta_LF = 0.95#((1-P_1_LF)* P_3_LF) / (((1-P_1_LF)* P_3_LF) + ((1-P_2_LF)*(1-P_3_LF)))
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


