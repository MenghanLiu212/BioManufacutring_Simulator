"""
@author: menghanliu

This is the run file of the simluation.
It's discrete params of Bioman.
"""

import pandas as pd
import numpy as np
#import pyDOE2
import random
import matplotlib.pyplot as plt
import timeit


import BioMan_toolbox as toolbox
import BioMan_Factory as Factory

#We have 2 values of alpha_low and alpha_up either low or high
def alpha_values(i,j):
    low_level_factor_mfg = 0.9
    up_level_factor_mfg = 1.10    
    if i == 0: 
        alpha_low_ll =4000
        alpha_low_ul = 50000
        alpha_low_mfg_fact='low'

    elif i==1: 
        alpha_low_ll =50000 
        alpha_low_ul = 100000
        alpha_low_mfg_fact='high'

    if j == 0: 
        alpha_up_ll =4000
        alpha_up_ul = 50000
        alpha_up_mfg_fact='low'

    elif j==1: 
        alpha_up_ll =50000 
        alpha_up_ul = 100000
        alpha_up_mfg_fact='high'

    return alpha_low_ll, alpha_low_ul, alpha_up_ll, alpha_up_ul, alpha_low_mfg_fact, alpha_up_mfg_fact, low_level_factor_mfg, up_level_factor_mfg

#We have 2 values of delta either low or high
def Delta_mix(i):
    if i == 0: 
        delta_mix_1 = 0.5 
        delta_mix_2 = 0.25

    elif i ==1:
        delta_mix_1 = 0.25
        delta_mix_2 = 0.25

    elif i ==2:
        delta_mix_1 = 0.25
        delta_mix_2 = 0.5 

    elif i ==3:    
        delta_mix_1 = 0.33
        delta_mix_2 = 0.33

    #else: 
    #    delta_low=6
    #    delta_up =10
    #    delta_fact='high'

    return delta_mix_1, delta_mix_2 
    


#Manufacturing_Mix(Manufacturing_Mix_MFG)
def Manufacturing_Mix(Manufacturing_Mix_MFG):
    if Manufacturing_Mix_MFG == 0:
        mfg_time_separator_1 = 0.5
        mfg_time_separator_2 = 0.25


    elif Manufacturing_Mix_MFG == 1:
        mfg_time_separator_1 = 0.25
        mfg_time_separator_2 = 0.25


    elif Manufacturing_Mix_MFG == 2:
        mfg_time_separator_1 = 0.25
        mfg_time_separator_2 = 0.5



    elif Manufacturing_Mix_MFG == 3:
        mfg_time_separator_1 = 0.33
        mfg_time_separator_2 = 0.33


    return mfg_time_separator_1, mfg_time_separator_2
    # mfg_time_separator_1, mfg_time_separator_2 = Manufacturing_Mix(Manufacturing_Mix_MFG)


def Patient_Mix(Patient_Mix_MFG):
    if Patient_Mix_MFG == 0:
        bad_pat_separator = 0.8
        average_pat_separator = 0.1
        good_pat_separator = 0.1 
		#100% relaxed system

    """
    #elif Patient_Mix_MFG == 1:
        bad_pat_separator = 0.5
        average_pat_separator = 0.3
        good_pat_separator = 0.2
        #0% stressed system
    """

    #elif Patient_Mix_MFG == 2:
    if Patient_Mix_MFG == 1:
        bad_pat_separator = 0.1
        average_pat_separator = 0.8
        good_pat_separator = 0.1
    	#50% relaxed system
    
    """
    elif Patient_Mix_MFG == 3:
        bad_pat_separator = 0.2
        average_pat_separator = 0.5
        good_pat_separator = 0.3
    	#25% relaxed system 75% stressed system
    """

    #elif Patient_Mix_MFG == 4:
    if Patient_Mix_MFG == 2:
        bad_pat_separator = 0.1
        average_pat_separator = 0.1
        good_pat_separator = 0.8
        #75% relaxed system 25% stressed system

    return bad_pat_separator, average_pat_separator, good_pat_separator

def System_Mix(System_Mix_MFG):

    if System_Mix_MFG == 0:
        stressed_sys_separator = 0.8
        average_sys_separator = 0.1
        relaxed_sys_separator = 0.1 
        #100% relaxed system

    """
    elif System_Mix_MFG == 1:
        stressed_sys_separator = 0.5
        average_sys_separator = 0.3
        relaxed_sys_separator = 0.2
        #0% stressed system
    """

    #elif System_Mix_MFG == 2:
    if System_Mix_MFG == 1:
        stressed_sys_separator = 0.1
        average_sys_separator = 0.8
        relaxed_sys_separator = 0.1
        #50% relaxed system

    """
    elif System_Mix_MFG == 3:
        stressed_sys_separator = 0.2
        average_sys_separator = 0.5
        relaxed_sys_separator = 0.3
        #25% relaxed system 75% stressed system
    """


    if System_Mix_MFG == 2:
        stressed_sys_separator = 0.1
        average_sys_separator = 0.1
        relaxed_sys_separator = 0.8
        #75% relaxed system 25% stressed system
    return stressed_sys_separator, average_sys_separator, relaxed_sys_separator


def plot_cell_state_graph_m(this_df,design_run,iteration_num,idle,start_setup, setup_end, busy, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, busy, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_m(cell_graph_x_trans, cell_graph_y_trans,design_run,iteration_num, pname, idle,start_setup, setup_end, busy, booked)

def plot_cell_state_graph_o(this_df,design_run,iteration_num,idle,start_setup, setup_end, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_o(cell_graph_x_trans, cell_graph_y_trans,design_run,iteration_num, pname, idle,start_setup, setup_end, booked)

def cell_state_graph_new_m(x, y, design_run,iteration_num, pname, idle,start_setup, setup_end, busy, booked):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.stackplot(x, percent, labels = [pname+'_idle_cnt',pname+'_start_setup_cnt',pname+'_setup_end_cnt',pname+'_busy_cnt',pname+'_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"
    plt.savefig('{}Figure_for_{}_{}_{}.png'.format(design_run,pname,design_run,iteration_num))

def cell_state_graph_new_o(x, y, design_run,iteration_num, pname, idle,start_setup, setup_end, booked):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.stackplot(x, percent, labels = [pname+'_idle_cnt',pname+'_start_setup_cnt',pname+'_setup_end_cnt',pname+'_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"
    plt.savefig('{}Figure_for_{}_{}_{}.png'.format(design_run,pname,design_run,iteration_num,))



def plot_cell_state_graph_o_abs_states(this_df,design_run,iteration_num,idle,start_setup, setup_end, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_o_abs_states(cell_graph_x_trans, cell_graph_y_trans,design_run,iteration_num, pname, idle,start_setup, setup_end, booked)

def cell_state_graph_new_o_abs_states(x, y, design_run,iteration_num, pname, idle,start_setup, setup_end, booked):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    #percent = y /  y.sum(axis=0).astype(float) * 100 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.stackplot(x, y, labels = [pname+'_idle_cnt',pname+'_start_setup_cnt',pname+'_setup_end_cnt',pname+'_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Number of {}'.format(pname))
    ax.margins(0, 0) # Set margins to avoid "whitespace"
    plt.savefig('{}Abs_Figure_for_{}_{}_{}.png'.format(design_run,pname,design_run,iteration_num))



def plot_cell_state_graph_m_abs_states(this_df,design_run,iteration_num,idle,start_setup, setup_end, busy, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, busy, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_m_abs_states(cell_graph_x_trans, cell_graph_y_trans,design_run,iteration_num, pname, idle,start_setup, setup_end, busy, booked)

def cell_state_graph_new_m_abs_states(x, y, design_run,iteration_num, pname, idle,start_setup, setup_end, busy, booked):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    #percent = y /  y.sum(axis=0).astype(float) * 100 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.stackplot(x, y, labels = [pname+'_idle_cnt',pname+'_start_setup_cnt',pname+'_setup_end_cnt',pname+'_busy_cnt',pname+'_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Number of {}'.format(pname))
    ax.margins(0, 0) # Set margins to avoid "whitespace"
    plt.savefig('{}Abs_Figure_for_{}_{}_{}.png'.format(design_run,pname,design_run,iteration_num))


def plot_cell_state_job(this_df,design_run,iteration_num):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_qc', 'jobs_in_completed']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_job(cell_graph_x_trans, cell_graph_y_trans,design_run,iteration_num)

def cell_state_graph_job(x,y,design_run,iteration_num):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.stackplot(x, percent, labels = ['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_qc', 'jobs_in_completed'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"
    plt.savefig('{}Figure_for_job{}_{}.png'.format(design_run,design_run,iteration_num))


#def plot_cell_state_job_abs(this_df,design_run):
def plot_cell_state_job_abs(this_df,design_run,iteration_num):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_qc', 'jobs_in_completed']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_job_abs(cell_graph_x_trans, cell_graph_y_trans,design_run,iteration_num)

def cell_state_graph_job_abs(x,y,design_run,iteration_num):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    #percent = y /  y.sum(axis=0).astype(float) * 100 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.stackplot(x, y, labels = ['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_qc', 'jobs_in_completed'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Number of Jobs')
    ax.margins(0, 0) # Set margins to avoid "whitespace"
    plt.savefig('{}Figure_for_job_abs{}_{}.png'.format(design_run,design_run,iteration_num))



def plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[pname].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_for_abs_val(cell_graph_x_trans, cell_graph_y_trans,design_run,iteration_num,pname)

def cell_state_graph_for_abs_val(x,y,design_run,iteration_num,pname):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    #percent = y /  y.sum(axis=0).astype(float) * 100 
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.stackplot(x, y, labels = [pname])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel(pname)
    ax.margins(0, 0) # Set margins to avoid "whitespace"
    plt.savefig('{}Figure_for_abs_val_{}_{}_{}.png'.format(design_run,pname,design_run,iteration_num))







def Main():
    #count=0   
    #according to the new discussing we removed the mid from alpha(U n L) and delta; patient mix quality policy FIX; 
    #Hrv Operator and Machines FIX ; 2 levels of machines and 2 of operators (ratio of machine)
    #levels = [alphalow, alphaup, delta, Patient mix, System mix, QM Policy, Hrv Operator, Hrv Machines, Mfg Operators, Mfg Machines]
    #levels = [2,2,2,5,5,1,2,2,2,2]    # this is the levels we are following

    #levels = [Manufacturing Time mix, Delta mix, Patient mix, System mix, QM Policy, Hrv Operator, Hrv Machines, Mfg Operators, Mfg Machines]
    levels =  [4,4,5,5,1,2,2,2,2]


    start_num=1
    #total_design = pyDOE2.fullfact(levels)
    #print(len(total_design))
    #print(total_design)        #give the entire list of all possible scenarios of the levels
    

    #print(random.choice(total_design))
    print('START SIM')
    design_run = 0
    #print(type(total_design))


    #main_df = pd.DataFrame(columns=['Level Number','Iteration Number','Clock', 'Event name', 'Event ID', 'Event happen time', 'Event place', 'Event machine', 'Event operator', 'Event job', 'Event rework times', 'Job yield', 
     #                                               'hrv_operator_state_list', 'MFG_operator_state_list', 'QC_operator_state_list', 'hrv_machine_state_list', 'MFG_machine_state_list', 'queue_state_list', 'job_state_list',
                                                    
      


    main_df=pd.DataFrame(columns=['Level Number','Iteration Number','Clock', 'Event name', 'Event ID', 'Event happen time', 'Event place', 'Event machine', 'Event operator', 'Event job', 'Event rework times', 'Job yield', 
                                                    'hrv_operator_state_list', 'MFG_operator_state_list', 'QC_operator_state_list', 'hrv_machine_state_list', 'MFG_machine_state_list', 'queue_state_list', 'job_state_list',
                                                    'jobs_entered', 'job_booked','jobs_in_queue', 'jobs_in_q1','jobs_in_q2','jobs_in_q3','jobs_in_rework', 'jobs_in_service','jobs_in_qc', 'jobs_in_completed', 'total_job_num'])
                                                    
        #self.df_this_design = pd.DataFrame(columns=['Clock', 'Event name', 'Event ID', 'Event happen time', 'Event place', 'Event machine', 'Event operator', 'Event job', 'Event rework times', 'Job yield', 
        #                                            'hrv_operator_state_list', 'MFG_operator_state_list', 'QC_operator_state_list', 'hrv_machine_state_list', 'MFG_machine_state_list', 'queue_state_list', 'job_state_list',
         #                                           'jobs_in_queue', 'jobs_in_rework', 'jobs_in_service','jobs_in_qc', 'jobs_in_completed', 'total_job_num'])
        
        #df to collect job datas
    df_mainjob=pd.DataFrame(columns=['Level Number','Iteration Number','Job_number','Alpha_low_mfg','Alpha_up_mfg','Delta_mfg','Gender','Blood vol','Patient Trgt Bld Count','Start_Time','Processing_Time','Rework Time','End Time'])    
        

    #expt_levels=open("Expt_level1.txt", "r")
    #for x in expt_level:
       # print(x)

    bioman_exp_table_fname="Bio_man_exp_table.csv"   #agave path
    EXP_COUNT=1
    
    experiments = pd.read_csv(bioman_exp_table_fname)
    experiments=experiments.replace('^L','',regex=True).astype(int)-1








    """
    #generate random value list
    rand_level_list = []
    i=0
    for i in range(0,9):
        random_level=random.choice(total_design)
        rand_level_list.append(random_level)

    with open('Experiment Level.txt', 'w') as f:
        for item in rand_level_list:
            f.write("%s" % item)    

    for iteration_num in range(0,5):
        print(iteration_num)

    #print(rand_level_list)
    """



    design_run =0
    

    #for design in total_design:
    #for  design in rand_level_list:
    start_exp = (start_num-1)*10 
    
    #for x in range(start_exp, EXP_COUNT+start_exp):
    #for x in range(0, 20):
    for x in range(0, 1):

        
        row=experiments[x:x+1]     



        design_run += 1
        iteration = 0

        main_df=pd.DataFrame(columns=['Level Number','Iteration Number','Clock', 'Event name', 'Event ID', 'Event happen time', 'Event place', 'Event machine', 'Event operator', 'Event job', 'Event rework times', 'Job yield', 
                                                    'hrv_operator_state_list', 'MFG_operator_state_list', 'QC_operator_state_list', 'hrv_machine_state_list', 'MFG_machine_state_list', 'queue_state_list', 'job_state_list',
                                                    'jobs_entered', 'job_booked','jobs_in_queue', 'jobs_in_q1','jobs_in_q2','jobs_in_q3','jobs_in_rework', 'jobs_in_service','jobs_in_qc', 'jobs_in_completed', 'total_job_num'])
    

            #self.df_this_design = pd.DataFrame(columns=['Clock', 'Event name', 'Event ID', 'Event happen time', 'Event place', 'Event machine', 'Event operator', 'Event job', 'Event rework times', 'Job yield', 
            #                                            'hrv_operator_state_list', 'MFG_operator_state_list', 'QC_operator_state_list', 'hrv_machine_state_list', 'MFG_machine_state_list', 'queue_state_list', 'job_state_list',
             #                                           'jobs_in_queue', 'jobs_in_rework', 'jobs_in_service','jobs_in_qc', 'jobs_in_completed', 'total_job_num'])
        
            #df to collect job datas
        df_mainjob=pd.DataFrame(columns=['Level Number','Iteration Number','Job_number','Alpha_low_mfg','Alpha_up_mfg','Delta_mfg','Manufacturing_Mix','Gender','Blood vol','Patient Trgt Bld Count','Start_Time','Processing_Time','Rework Time','End Time'])    


        #print("Level")
        #print(design_run)
        #print("Iteration")
        """
        alphalow=row["alpha_low"].values[0]
        alphaup= row["alpha_high"].values[0]
        delta = row["delta"].values[0]
        Patient_Mix_MFG = row["patient_mix"].values[0]
        System_Mix_MFG = row["system_mix"].values[0]
        QM_Policy_MFG = 0
        Hrv_operator=row["Hrv_operator"].values[0]
        Hrv_machine=row["Hrv_machine"].values[0]
        Mfg_operator=row["Mfg_operator"].values[0]
        Mfg_machine=row["Mfg_machine"].values[0]
        """
        
        Manufacturing_Mix_MFG =row["Mfg Time"].values[0]   #change in excel
        Delta_Mix  = row["Delta Mix"].values[0]

#        Patient_Mix_MFG, System_Mix_MFG, QM_Policy_MFG,Hrv_machine,Hrv_operator,Mfg_machine,Mfg_operator
        

        Patient_Mix_MFG = row["patient_mix"].values[0]
        #System_Mix_MFG = row["system_mix"].values[0]
        QM_Policy_MFG = 0
        Hrv_operator=row["Hrv_operator"].values[0]
        Hrv_machine=row["Hrv_machine"].values[0]
        Mfg_operator=row["Mfg_operator"].values[0]
        Mfg_machine=row["Mfg_machine"].values[0]

        
        #print("HElloOsdasjkfsdkjsad")
        #print(alphalow,alphaup, delta,Patient_Mix_MFG, System_Mix_MFG, QM_Policy_MFG)
        #alpha_low_ll, alpha_low_ul, alpha_up_ll, alpha_up_ul, alpha_low_mfg_fact, alpha_up_mfg_fact, low_level_factor_mfg, up_level_factor_mfg=alpha_values(alphalow,alphaup)
        

        delta_mix_1, delta_mix_2=Delta_mix(Delta_Mix) 

        design= [Manufacturing_Mix_MFG, Delta_Mix, Patient_Mix_MFG, QM_Policy_MFG, Hrv_machine, Hrv_operator, Mfg_machine, Mfg_operator]



        ITERATION = 1  #replication number

        for iteration_num in range(0,ITERATION):
            

            #print(iteration_num)
            #break

            design=list(design)
            #print('design',design)
            #design = [1,1,1,0,0,0,1,1,1,1]
            print(design)
            print('***Start***')
            print('This design:', design)
            print('____________________________________')




            """
        #for design in total_design:
        for  design in total_design:
            design_run += 1
            design=list(design)
            #print('design',design)
            print(design)
            print('***Start***')
            print('This design:', design)
            print('____________________________________')
            """
            
            #alphalow=design[0]
            #alphaup= design[1]
            
            #Manufacturing_Mix_MFG

            #design= [Manufacturing_Mix_MFG,Delta_Mix, Patient_Mix_MFG, System_Mix_MFG, QM_Policy_MFG,Hrv_machine,Hrv_operator,Mfg_machine,Mfg_operator]

            Manufacturing_Mix_MFG=design[0]

            delta = design[1]
            Patient_Mix_MFG = design[2]
            #System_Mix_MFG = design[3]
            QM_Policy_MFG = design[3]
            
            
            #Hrv Operator = design[6], Hrv Machines, Mfg Operators, Mfg Machines
            
            #alpha_low_ll, alpha_low_ul, alpha_up_ll, alpha_up_ul, alpha_low_mfg_fact, alpha_up_mfg_fact, low_level_factor_mfg, up_level_factor_mfg=alpha_values(alphalow,alphaup)
            #delta_ll, delta_ul, delta_fact=delta_value(delta)  
            #separator_1, separator_2 = Patient_Mix(Patient_Mix_MFG)
            

            bad_pat_separator, average_pat_separator, good_pat_separator= Patient_Mix(Patient_Mix_MFG) #prob_stress
            #stressed_sys_separator, average_sys_separator, relaxed_sys_separator=System_Mix(System_Mix_MFG)            
            delta_mix_1, delta_mix_2 = Delta_mix(delta)
            mfg_time_separator_1, mfg_time_separator_2 = Manufacturing_Mix(Manufacturing_Mix_MFG)

            low_level_factor_mfg = 0.9 
            up_level_factor_mfg = 1.1
            #OurController = Factory.Controller()        
            OurEnvironment = Factory.Environment(design)
            OurEnvironment.Factor_design(mfg_time_separator_1, mfg_time_separator_2, delta_mix_1, delta_mix_2, low_level_factor_mfg, up_level_factor_mfg, bad_pat_separator, average_pat_separator, good_pat_separator, QM_Policy_MFG)
            start = timeit.default_timer()
            this_df, df_job = OurEnvironment.Simulate()
            print("SIM DONE")
            print("SIM DONE CHECK")
            


            #adding collumns to the this_df which show the count of idle, setup, setup_end, busy, booked operators and machines at each time epoch
            
            #'_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_busy_cnt','hrv_opr_booked_cnt'
            this_df['hrv_opr_idle_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("idle") , axis=1)
            this_df['hrv_opr_start_setup_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("setup") , axis=1)
            this_df['hrv_opr_setup_end_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("setup_end") , axis=1)
            #this_df['hrv_opr_busy_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("busy") , axis=1)
            this_df['hrv_opr_booked_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("booked") , axis=1)
            
            #'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_busy_cnt','mfg_opr_booked_cnt'
            this_df['mfg_opr_idle_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("idle") , axis=1)
            this_df['mfg_opr_start_setup_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("setup") , axis=1)
            this_df['mfg_opr_setup_end_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("setup_end") , axis=1)
            #this_df['mfg_opr_busy_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("busy") , axis=1)
            this_df['mfg_opr_booked_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("booked") , axis=1)

             #'hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt'
            this_df['hrv_mc_idle_cnt'] = this_df.apply(lambda row: row['hrv_machine_state_list'].count("idle") , axis=1)
            this_df['hrv_mc_start_setup_cnt'] = this_df.apply(lambda row: row['hrv_machine_state_list'].count("setup") , axis=1)
            this_df['hrv_mc_setup_end_cnt'] = this_df.apply(lambda row: row['hrv_machine_state_list'].count("setup_end") , axis=1)
            this_df['hrv_mc_busy_cnt'] = this_df.apply(lambda row: row['hrv_machine_state_list'].count("busy") , axis=1)
            this_df['hrv_mc_booked_cnt'] = this_df.apply(lambda row: row['hrv_machine_state_list'].count("booked") , axis=1)

            #'mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt'
            this_df['mfg_mc_idle_cnt'] = this_df.apply(lambda row: row['MFG_machine_state_list'].count("idle") , axis=1)
            this_df['mfg_mc_start_setup_cnt'] = this_df.apply(lambda row: row['MFG_machine_state_list'].count("setup") , axis=1)
            this_df['mfg_mc_setup_end_cnt'] = this_df.apply(lambda row: row['MFG_machine_state_list'].count("setup_end") , axis=1)
            this_df['mfg_mc_busy_cnt'] = this_df.apply(lambda row: row['MFG_machine_state_list'].count("busy") , axis=1)
            this_df['mfg_mc_booked_cnt'] = this_df.apply(lambda row: row['MFG_machine_state_list'].count("booked") , axis=1)

            #'qc_opr_idle_cnt','qc_opr_start_setup_cnt','qc_opr_cnt','qc_opr_busy_cnt','qc_opr_cnt'
            this_df['qc_opr_idle_cnt'] = this_df.apply(lambda row: row['QC_operator_state_list'].count("idle") , axis=1)
            #this_df['qc_opr_start_setup_cnt'] = this_df.apply(lambda row: row['QC_operator_state_list'].count("setup") , axis=1)
            #this_df['qc_opr_setup_end_cnt'] = this_df.apply(lambda row: row['QC_operator_state_list'].count("setup_end") , axis=1)
            this_df['qc_opr_busy_cnt'] = this_df.apply(lambda row: row['QC_operator_state_list'].count("busy") , axis=1)
            this_df['qc_opr_booked_cnt'] = this_df.apply(lambda row: row['QC_operator_state_list'].count("booked") , axis=1)        
            
            

            #add a new df to get all job data
            
            main_df=main_df.append(this_df)
            df_mainjob=df_mainjob.append(df_job)


            #'Level Number':design_run,'Iteration Number'
            
            """
            main_df['Iteration number'] = iteration_num
            df_mainjob['Iteration number'] = iteration_num
            main_df['Design'] = design_run    
            df_mainjob['Level'] = design_run
            """
            df_mainjob['Level Number'] = design_run






            #converting df to csv files 
            this_df.to_csv('{}experiment_output_design{}_{}.csv'.format(design_run,design_run,iteration_num))
            df_job.to_csv('{}job_data{}_{}.csv'.format(design_run,design_run,iteration_num))

            

            """
            #plotting graphs to get png files
            #plot_cell_state_graph(this_df,design_run,'hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_busy_cnt','hrv_opr_booked_cnt','hrc_opr')
            #plot_cell_state_graph(this_df,design_run,'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_busy_cnt','mfg_opr_booked_cnt','mfg_opr')
            #plot_cell_state_graph(this_df,design_run,'hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt','hrv_mc')
            #plot_cell_state_graph(this_df,design_run,'mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt','mfg_mc')
            #plot_cell_state_job(this_df,design_run)
            #plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_opr_busy_cnt')
            #plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_opr_idle_cnt')
            #plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_mc_busy_cnt')
            #plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_mc_idle_cnt')
            #plot_cell_state_job_abs(this_df,design_run)
            """
            
            
            
            #plotting graphs to get png files
            plot_cell_state_graph_o(this_df,design_run,iteration_num,'hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_booked_cnt','hrv_opr')
            plot_cell_state_graph_o(this_df,design_run,iteration_num,'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_booked_cnt','mfg_opr')
            plot_cell_state_graph_m(this_df,design_run,iteration_num,'hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt','hrv_mc')
            plot_cell_state_graph_m(this_df,design_run,iteration_num,'mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt','mfg_mc')
            plot_cell_state_job_abs(this_df,design_run,iteration_num)
            #plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_opr_busy_cnt')
            
            plot_cell_state_job(this_df,design_run,iteration_num)


            
            plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,'mfg_opr_idle_cnt')
            plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,'hrv_mc_busy_cnt')
            plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,'hrv_mc_idle_cnt')
            plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,'mfg_mc_busy_cnt')
            plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,'mfg_mc_idle_cnt')
            plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,'qc_opr_idle_cnt')
            plot_cell_state_graph_for_abs_value(this_df,design_run,iteration_num,'qc_opr_busy_cnt')
            
            #plot_cell_state_job_abs(this_df,design_run)



            plot_cell_state_graph_o_abs_states(this_df,design_run,iteration_num,'hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_booked_cnt','hrv_opr')
            plot_cell_state_graph_o_abs_states(this_df,design_run,iteration_num,'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_booked_cnt','mfg_opr')
            plot_cell_state_graph_m_abs_states(this_df,design_run,iteration_num,'hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt','hrv_mc')
            plot_cell_state_graph_m_abs_states(this_df,design_run,iteration_num,'mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt','mfg_mc')
            




            #stop = timeit.default_timer()
            #print('Time: ', stop - start)
            
        
            if iteration_num == ITERATION:


            #this_df['run_number'] = design_run
            #this_df['design_number'] = design_run
            #this_df['run_number'] = run_no
                #main_df.to_csv('{}CUMULATIVE_experiment_output_design{}.csv'.format(design_run,design_run)
                df_mainjob.to_csv('{}CUMULATIVE_job_data{}.csv'.format(design_run,design_run))
                break

                #just for test--------
        if design_run == 81:
            #stop = timeit.default_timer()
            #print('Time: ', stop - start)
            break

        #---------------------
        
        #return
#**********************************
"""
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bio_man Simulation')
    parser.add_argument('start_num', type=int, nargs=1, help='Bio_man Simulation')
    args = parser.parse_args()

    start_num = args.start_num[0]
    
print('start_num:', start_num)
Main(start_num)
"""
Main()
#command: python BioMan_runfile.py start_num

"""
# main function

if __name__ =='__main__':
    levels = [2, 2, 3, 3, 3, 3, 3]
    total_design = pyDOE2.fullfact(levels)
    
    design_run = 0
    for design in total_design:
        design_run += 1
        
        #just for test
        design=[0,0,0,3,3,3,3]
        
        print('***Start***')
        print('This design:', design)
        
        Yield_Curve_MFG = design[0]
        Patient_Mix_MFG = design[1]
        QM_Policy_MFG = design[2]
        
        alpha_low_mfg, alpha_up_mfg, delta_t_mfg, low_level_factor_mfg, up_level_factor_mfg = yield_curve_level(Yield_Curve_MFG)
        separator_1, separator_2 = Patient_Mix(Patient_Mix_MFG)
        
        #OurController = Factory.Controller()        
        OurEnvironment = Factory.Environment(design)
        OurEnvironment.Factor_design(alpha_low_mfg, alpha_up_mfg, delta_t_mfg, low_level_factor_mfg, up_level_factor_mfg, separator_1, separator_2, QM_Policy_MFG)
        this_df = OurEnvironment.Simulate()
        this_df.to_csv('experiment_output_design{}.csv'.format(design_run))
        
        #for test only
        if design_run >= 1:
            break
    """    
        
