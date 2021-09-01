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
def delta_value(i):
    if i == 0: 
        delta_low=2 
        delta_up =6
        delta_fact='low'

    else: 
        delta_low=6
        delta_up =10
        delta_fact='high'

    return delta_low, delta_up, delta_fact
    

def Patient_Mix(Patient_Mix_MFG):
	relaxed_separator_1 = 0.25
	relaxed_separator_2 = 0.75
	stressed_separator_1 = 0.1
	stressed_separator_2 = 0.9

	if Patient_Mix_MFG == 0:
		#100% relaxed system
		prob_relax=1.0
    	#prob_stress=0.0

	elif Patient_Mix_MFG == 1:
		#0% stressed system
		prob_relax=0.0
    	#prob_stress=1.0

	elif Patient_Mix_MFG == 2:
		#50% relaxed system
		prob_relax=0.5
    	#prob_stress=0.5

	elif Patient_Mix_MFG == 3:
		#25% relaxed system 75% stressed system
		prob_relax=0.25
    	#prob_stress=0.75

	elif Patient_Mix_MFG == 4:
		#75% relaxed system 25% stressed system
		prob_relax=0.75
    	#prob_stress=0.25

	return relaxed_separator_1, relaxed_separator_2, stressed_separator_1, stressed_separator_2, prob_relax#, prob_stress



def plot_cell_state_graph_m(this_df,design_run,idle,start_setup, setup_end, busy, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, busy, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_m(cell_graph_x_trans, cell_graph_y_trans,design_run, pname, idle,start_setup, setup_end, busy, booked)

def plot_cell_state_graph_o(this_df,design_run,idle,start_setup, setup_end, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_o(cell_graph_x_trans, cell_graph_y_trans,design_run, pname, idle,start_setup, setup_end, booked)

def cell_state_graph_new_m(x, y, design_run, pname, idle,start_setup, setup_end, busy, booked):
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
    plt.savefig('{}Figure_for_{}_{}.png'.format(design_run,pname,design_run))

def cell_state_graph_new_o(x, y, design_run, pname, idle,start_setup, setup_end, booked):
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
    plt.savefig('{}Figure_for_{}_{}.png'.format(design_run,pname,design_run))



def plot_cell_state_graph_o_abs_states(this_df,design_run,idle,start_setup, setup_end, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_o_abs_states(cell_graph_x_trans, cell_graph_y_trans,design_run, pname, idle,start_setup, setup_end, booked)

def cell_state_graph_new_o_abs_states(x, y, design_run, pname, idle,start_setup, setup_end, booked):
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
    plt.savefig('{}Abs_Figure_for_{}_{}.png'.format(design_run,pname,design_run))



def plot_cell_state_graph_m_abs_states(this_df,design_run,idle,start_setup, setup_end, busy, booked, pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[[idle, start_setup, setup_end, busy, booked]].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_new_m_abs_states(cell_graph_x_trans, cell_graph_y_trans,design_run, pname, idle,start_setup, setup_end, busy, booked)

def cell_state_graph_new_m_abs_states(x, y, design_run, pname, idle,start_setup, setup_end, busy, booked):
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
    plt.savefig('{}Abs_Figure_for_{}_{}.png'.format(design_run,pname,design_run))


def plot_cell_state_job(this_df,design_run):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_qc', 'jobs_in_completed']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_job(cell_graph_x_trans, cell_graph_y_trans,design_run)

def cell_state_graph_job(x,y,design_run):
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
    plt.savefig('{}Figure_for_job{}.png'.format(design_run,design_run))



def plot_cell_state_job_abs(this_df,design_run):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[['jobs_in_queue', 'jobs_in_rework', 'jobs_in_service', 'jobs_in_qc', 'jobs_in_completed']].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_job_abs(cell_graph_x_trans, cell_graph_y_trans,design_run)

def cell_state_graph_job_abs(x,y,design_run):
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
    plt.savefig('{}Figure_for_job_abs{}.png'.format(design_run,design_run))



def plot_cell_state_graph_for_abs_value(this_df,design_run,pname):
    #print('plot_cell_mfg_event_calendar_row:', mfg_event_calendar.iloc[0])
    cell_graph_x = np.array(this_df['Clock'].values, dtype=float)
    cell_graph_y = np.array(this_df[pname].values, dtype=float)
    cell_graph_x_trans = np.transpose(cell_graph_x)
    cell_graph_y_trans = np.transpose(cell_graph_y)
    cell_state_graph_for_abs_val(cell_graph_x_trans, cell_graph_y_trans,design_run,pname)

def cell_state_graph_for_abs_val(x,y,design_run,pname):
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
    plt.savefig('{}Figure_for_abs_val_{}_{}.png'.format(design_run,pname,design_run))






def Main():
    #count=0
    #levels = [2, 2, 3, 3,3,3,3]
    #levels = [3,3,3,2,3,3,3,3,3]
    
    #according to the new discussing we removed the mid from alpha(U n L) and delta; patient mix quality policy FIX; 
    #Hrv Operator and Machines FIX ; 2 levels of machines and 2 of operators (ratio of machine)
    #levels = [alphalow, alphaup, delta, Patient mix, QM Policy, Hrv Operator, Hrv Machines, Mfg Operators, Mfg Machines]
    #levels = [2,2,2,5,1,1,1,2,2]    # this is the levels we are following
    levels = [1,1,1,5,1,1,1,1,1]
    total_design = pyDOE2.fullfact(levels)
    #print(total_design)
    print(len(total_design))
    
    #print(total_design)
    #give the entire list of all possible scenarios of the levels
    
    print('START SIM')
    design_run = 0
    for design in total_design:
        design_run += 1
        design=list(design)
        #print('design',design)
        print(design)
        print('***Start***')
        print('This design:', design)
        print('____________________________________')
        
        alphalow=design[0]
        alphaup= design[1]
        delta = design[2]
        Patient_Mix_MFG = design[3]
        QM_Policy_MFG = design[4]
                	
        alpha_low_ll, alpha_low_ul, alpha_up_ll, alpha_up_ul, alpha_low_mfg_fact, alpha_up_mfg_fact, low_level_factor_mfg, up_level_factor_mfg=alpha_values(alphalow,alphaup)
        delta_ll, delta_ul, delta_fact=delta_value(delta)  
        #separator_1, separator_2 = Patient_Mix(Patient_Mix_MFG)
        relaxed_separator_1, relaxed_separator_2, stressed_separator_1, stressed_separator_2, prob_relax = Patient_Mix(Patient_Mix_MFG) #prob_stress
        #OurController = Factory.Controller()        
        OurEnvironment = Factory.Environment(design)
        OurEnvironment.Factor_design(alpha_low_ll, alpha_low_ul,alpha_up_ll, alpha_up_ul, delta_ll, delta_ul, low_level_factor_mfg, up_level_factor_mfg, relaxed_separator_1, relaxed_separator_2, stressed_separator_1, stressed_separator_2, prob_relax, QM_Policy_MFG)
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
        
        #converting df to csv files 
        this_df.to_csv('{}experiment_output_design{}.csv'.format(design_run,design_run))
        df_job.to_csv('{}job_data{}.csv'.format(design_run,design_run))

        """
        #plotting graphs to get png files
        plot_cell_state_graph(this_df,design_run,'hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_busy_cnt','hrv_opr_booked_cnt','hrc_opr')
        plot_cell_state_graph(this_df,design_run,'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_busy_cnt','mfg_opr_booked_cnt','mfg_opr')
        plot_cell_state_graph(this_df,design_run,'hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt','hrv_mc')
        plot_cell_state_graph(this_df,design_run,'mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt','mfg_mc')
        plot_cell_state_job(this_df,design_run)
        plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_opr_busy_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_opr_idle_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_mc_busy_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_mc_idle_cnt')
        plot_cell_state_job_abs(this_df,design_run)
        """
        
        """
        #plotting graphs to get png files
        plot_cell_state_graph_o(this_df,design_run,'hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_booked_cnt','hrv_opr')
        plot_cell_state_graph_o(this_df,design_run,'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_booked_cnt','mfg_opr')
        plot_cell_state_graph_m(this_df,design_run,'hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt','hrv_mc')
        plot_cell_state_graph_m(this_df,design_run,'mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt','mfg_mc')
        plot_cell_state_job(this_df,design_run)
        #plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_opr_busy_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_opr_idle_cnt')

        plot_cell_state_graph_for_abs_value(this_df,design_run,'hrv_mc_busy_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'hrv_mc_idle_cnt')
        

        plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_mc_busy_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'mfg_mc_idle_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'qc_opr_idle_cnt')
        plot_cell_state_graph_for_abs_value(this_df,design_run,'qc_opr_busy_cnt')
        
        plot_cell_state_job_abs(this_df,design_run)



        plot_cell_state_graph_o_abs_states(this_df,design_run,'hrv_opr_idle_cnt','hrv_opr_start_setup_cnt','hrv_opr_setup_end_cnt','hrv_opr_booked_cnt','hrv_opr')
        plot_cell_state_graph_o_abs_states(this_df,design_run,'mfg_opr_idle_cnt','mfg_opr_start_setup_cnt','mfg_opr_setup_end_cnt','mfg_opr_booked_cnt','mfg_opr')
        plot_cell_state_graph_m_abs_states(this_df,design_run,'hrv_mc_idle_cnt','hrv_mc_start_setup_cnt','hrv_mc_setup_end_cnt','hrv_mc_busy_cnt','hrv_mc_booked_cnt','hrv_mc')
        plot_cell_state_graph_m_abs_states(this_df,design_run,'mfg_mc_idle_cnt','mfg_mc_start_setup_cnt','mfg_mc_setup_end_cnt','mfg_mc_busy_cnt','mfg_mc_booked_cnt','mfg_mc')
        """




        #stop = timeit.default_timer()
        #print('Time: ', stop - start)
        
        
                #just for test--------
        if design_run == 1:
        	stop = timeit.default_timer()
        	print('Time: ', stop - start)
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
        