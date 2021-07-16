"""
@author: menghanliu

This is the run file of the simluation.
It's discrete params of Bioman.
"""

import pandas as pd
import numpy as np
import pyDOE2
import random
import matplotlib.pyplot as plt
import timeit


import BioMan_toolbox as toolbox
import BioMan_Factory as Factory

"""
#Factor design
def yield_curve_level(Yield_Curve_MFG):
    delta_t_mfg = 5
    low_level_factor_mfg = 0.9
    up_level_factor_mfg = 1.10
    if Yield_Curve_MFG == 0: #relaxed
        alpha_low_mfg = 100000 
        alpha_up_mfg = 4000
    else:                   # stressed
        alpha_low_mfg =  85000
        alpha_up_mfg = 20000
    return alpha_low_mfg, alpha_up_mfg, delta_t_mfg, low_level_factor_mfg, up_level_factor_mfg
"""
def alpha_values(i,j):
    low_level_factor_mfg = 0.9
    up_level_factor_mfg = 1.10    
    if i == 0: 
        alpha_low =4000
        alpha_up = 20000
        alpha_low_mfg= np.random.uniform(alpha_low,alpha_up)
        alpha_low_mfg_fact='low'


    elif i == 1: 
        alpha_low =20000
        alpha_up = 85000
        alpha_low_mfg= np.random.uniform(alpha_low,alpha_up)
        alpha_low_mfg_fact='med'

    else: 
        alpha_low =85000 
        alpha_up = 100000
        alpha_low_mfg= np.random.uniform(alpha_low,alpha_up)
        alpha_low_mfg_fact='high'

    if j == 0: 
        alpha_low =4000
        alpha_up = 20000
        alpha_up_mfg= np.random.uniform(alpha_low,alpha_up)
        alpha_up_mfg_fact='low'


    elif j == 1: 
        alpha_low =20000
        alpha_up = 85000
        alpha_up_mfg= np.random.uniform(alpha_low,alpha_up)
        alpha_up_mfg_fact='med'

    else: 
        alpha_low =85000 
        alpha_up = 100000
        alpha_up_mfg= np.random.uniform(alpha_low,alpha_up)
        alpha_up_mfg_fact='high'

    return alpha_low_mfg, alpha_up_mfg, alpha_low_mfg_fact, alpha_up_mfg_fact, low_level_factor_mfg, up_level_factor_mfg

def delta_value(i):
    if i == 0: 
        delta_low=2 
        delta_up =5
        delta_mfg=np.random.uniform(delta_low,delta_up)
        delta_fact='low'


    elif i == 1: 
        delta_low=5 
        delta_up =8
        delta_mfg=np.random.uniform(delta_low,delta_up)
        delta_fact='med'


    else: 
        delta_low=8
        delta_up =10
        delta_mfg= np.random.uniform(delta_low,delta_up)
        delta_fact='high'

    return delta_mfg, delta_fact

def Patient_Mix(Patient_Mix_MFG):
    if Patient_Mix_MFG == 0:
        separator_1 = 0.25
        separator_2 = 0.75
    elif Patient_Mix_MFG == 1:
        separator_1 = 0.10
        separator_2 = 0.90
    return separator_1, separator_2

def Machine_and_operator_num(MandO_num):
    Machine_and_operator_num =[]
    if MandO_num == 0:

        Machine_and_operator_num = [10, 10, 10, 10]
    elif MandO_num == 1:
        Machine_and_operator_num = [5,5,5,5]
    elif MandO_num == 2:
        Machine_and_operator_num = [3,3,3,3]
    return Machine_and_operator_num


#not in use
def num_of_operators_and_machine(i, NUM_PATIENTS):
    #Factor 4 corresponds to the harvesting operators count
    if i == 0:
        OPERATOR_HRV = round(NUM_PATIENTS/15)
    elif i == 1:
        OPERATOR_HRV = round(NUM_PATIENTS/25)
    else:
        OPERATOR_HRV = round(NUM_PATIENTS/35)
        
    #Factor 5 corresponds to the available harvesting machines count
    if i == 0:
        MACHINES_HRV = round(NUM_PATIENTS/10)
    elif i == 1:
        MACHINES_HRV = round(NUM_PATIENTS/20)
    else:
        MACHINES_HRV = round(2* NUM_PATIENTS/30)
        
    #Factor 6 corresponds to the Mfg operators count 
    if i == 0:
        OPERATOR_MFG = round(NUM_PATIENTS/5)
    elif i == 1:
        OPERATOR_MFG = round(NUM_PATIENTS/10)
    else:
        OPERATOR_MFG = round(NUM_PATIENTS/20)
    
    #Factor 7 corresponds to the available Mfg machines(bio-reactors) count
    if i == 0:
        MACHINES_MFG = round(NUM_PATIENTS/2)
    elif i == 1:
        MACHINES_MFG = round(NUM_PATIENTS/5)
    else:
        MACHINES_MFG = round(NUM_PATIENTS)
        return OPERATOR_HRV, MACHINES_HRV, OPERATOR_MFG, MACHINES_MFG


def cell_state_graph_new1(x,y,design_run):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.stackplot(x, percent, labels = ['hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_busy_cnt','hrv_opr_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"

    #plt.show()
    #plt.savefig('Figure{}{}{}{}{}{}{}_{}.png'.format(design[0]),format(design[1]),format(design[2]),format(design[3]),format(design[4]),format(design[5]),format(design[6]),format(design_run))
    plt.savefig('Figure_for_hrv_opr{}.png'.format(design_run))


def plot_cell_state_graph1(this_df,design_run):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_busy_cnt','hrv_opr_booked_cnt']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new1(cell_graph_x_trans, cell_graph_y_trans,design_run)

def cell_state_graph_new2(x,y,design_run):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.stackplot(x, percent, labels = ['mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_busy_cnt','mfg_opr_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"

    #plt.show()
    #plt.savefig('Figure{}{}{}{}{}{}{}_{}.png'.format(design[0]),format(design[1]),format(design[2]),format(design[3]),format(design[4]),format(design[5]),format(design[6]),format(design_run))
    plt.savefig('Figure_for_mfg_opr{}.png'.format(design_run))

    #hrv_operator
def plot_cell_state_graph2(this_df,design_run):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_busy_cnt','mfg_opr_booked_cnt']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new2(cell_graph_x_trans, cell_graph_y_trans,design_run)

def cell_state_graph_new3(x,y,design_run):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.stackplot(x, percent, labels = ['hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"

    #plt.show()
    #plt.savefig('Figure{}{}{}{}{}{}{}_{}.png'.format(design[0]),format(design[1]),format(design[2]),format(design[3]),format(design[4]),format(design[5]),format(design[6]),format(design_run))
    plt.savefig('Figure_for_hrv_mc{}.png'.format(design_run))


def plot_cell_state_graph3(this_df,design_run):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new3(cell_graph_x_trans, cell_graph_y_trans,design_run)

def cell_state_graph_new4(x,y,design_run):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.stackplot(x, percent, labels = ['mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"

    #plt.show()
    #plt.savefig('Figure{}{}{}{}{}{}{}_{}.png'.format(design[0]),format(design[1]),format(design[2]),format(design[3]),format(design[4]),format(design[5]),format(design[6]),format(design_run))
    plt.savefig('Figure_for_mfg_mc{}.png'.format(design_run))
    
def plot_cell_state_graph4(this_df,design_run):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new4(cell_graph_x_trans, cell_graph_y_trans,design_run)

def cell_state_graph_new5(x,y,design_run):
    # Make new array consisting of fractions of column-totals,
    # using .astype(float) to avoid integer division
    percent = y /  y.sum(axis=0).astype(float) * 100 

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.stackplot(x, percent, labels = ['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_completed'])
    ax.legend(loc='upper left')
    ax.set_title('100 % stacked area chart')
    ax.set_ylabel('Percent (%)')
    ax.margins(0, 0) # Set margins to avoid "whitespace"

    #plt.show()
    #plt.savefig('Figure{}{}{}{}{}{}{}_{}.png'.format(design[0]),format(design[1]),format(design[2]),format(design[3]),format(design[4]),format(design[5]),format(design[6]),format(design_run))
    plt.savefig('Figure_for_job{}.png'.format(design_run))

def plot_cell_state_graph5(this_df,design_run):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_completed']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new5(cell_graph_x_trans, cell_graph_y_trans,design_run)


def Main():
    #count=0
    #levels = [2, 2, 3, 3,3,3,3]
    levels = [3,3,3,2,3,3,3,3,3]
    total_design = pyDOE2.fullfact(levels)
    #print(total_design)
    print(len(total_design))
    #print(total_design[45])
    print('START SIM')
    design_run = 0
    for design in total_design:
        design_run += 1
        design=list(design)
        #print('design',design)
        print(design)
        
        #design = design + [3,3,3,3]  #the 4 elements in the lists represent hrv-operator, hrv_machine, mfg_operator and mfg_machine numbers, you can choose it yourself
       #MandO_num = design[3::]
        #print('WOAH',MandO_num)
        #design = design[0:3] + [3,3,3,3]#Machine_and_operator_num(MandO_num)
        
        #just for test--------
        #design=[0,0,0,3,3,3,3]
        #---------------------
        
        print('***Start***')
        print('This design:', design)
        print('____________________________________')
        """
        alphalow=design[0]
        alphaup= design[1]
        delta = design[2]
    
    
        #Yield_Curve_MFG = design[0]
        Patient_Mix_MFG = design[3]
        QM_Policy_MFG = design[4]
        
        #alpha_low_mfg, alpha_up_mfg, delta_t_mfg, low_level_factor_mfg, up_level_factor_mfg = yield_curve_level(Yield_Curve_MFG)
        
        alpha_low_mfg, alpha_up_mfg, alpha_low_mfg_fact, alpha_up_mfg_fact, low_level_factor_mfg, up_level_factor_mfg=alpha_values(alphalow,alphaup)
        #alpha_low_mfg, alpha_up_mfg, delta_t_mfg, low_level_factor_mfg, up_level_factor_mfg = yield_curve_level(Yield_Curve_MFG)
        delta_mfg, delta_fact=delta_value(delta)
    
    
        separator_1, separator_2 = Patient_Mix(Patient_Mix_MFG)
        
        #OurController = Factory.Controller()        
        OurEnvironment = Factory.Environment(design)
        OurEnvironment.Factor_design(alpha_low_mfg, alpha_up_mfg, delta_mfg, low_level_factor_mfg, up_level_factor_mfg, separator_1, separator_2, QM_Policy_MFG)
        start = timeit.default_timer()
        this_df = OurEnvironment.Simulate()
        #this_df.to_csv('experiment_output_design{}{}{}{}{}{}{}_{}.csv'.format(design[0]),format(design[1]),format(design[2]),format(design[3]),format(design[4]),format(design[5]),format(design[6]),format(design_run))
        
        #'_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_busy_cnt','hrv_opr_booked_cnt'
        
        this_df['hrv_opr_idle_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("idle") , axis=1)
        this_df['hrv_opr_start_setup_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("setup") , axis=1)
        this_df['hrv_opr_setup_end_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("setup_end") , axis=1)
        this_df['hrv_opr_busy_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("busy") , axis=1)
        this_df['hrv_opr_booked_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("booked") , axis=1)
        
        #'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_busy_cnt','mfg_opr_booked_cnt'

        this_df['mfg_opr_idle_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("idle") , axis=1)
        this_df['mfg_opr_start_setup_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("setup") , axis=1)
        this_df['mfg_opr_setup_end_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("setup_end") , axis=1)
        this_df['mfg_opr_busy_cnt'] = this_df.apply(lambda row: row['MFG_operator_state_list'].count("busy") , axis=1)
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
 
    
 
    
 
    #this_df['hrv_opr_idle_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("idle") , axis=1)
        #this_df['hrv_opr_idle_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("idle") , axis=1)
        #this_df['hrv_opr_idle_cnt'] = this_df.apply(lambda row: row['hrv_operator_state_list'].count("idle") , axis=1)
         
        this_df.to_csv('experiment_output_design{}.csv'.format(design_run))
        
        plot_cell_state_graph1(this_df,design_run)
        plot_cell_state_graph2(this_df,design_run)
        plot_cell_state_graph3(this_df,design_run)
        plot_cell_state_graph4(this_df,design_run)
        plot_cell_state_graph5(this_df,design_run)
        
        stop = timeit.default_timer()
        print('Time: ', stop - start)
        """
                #just for test--------
        if design_run == 4:
            break
        #---------------------
            
        #return

Main()


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
        