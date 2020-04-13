'''
Testing interventions in Covasim
'''

#%% Imports and settings
import sciris as sc
import covasim as cv
import datetime as dt
import unittest

do_plot = 1
do_show = 1
do_save = 0
debug = 1
keep_sims = 0
fig_paths = [f'results/testing_scen_{i}.png' for i in range(3)]


class TestInterventions(unittest.TestCase):

    def test_change_beta(do_plot=False, do_show=True, do_save=False, fig_path=None):
        make_ppl = 1

        # Filename settings
        fn = sc.objdict()
        fn.version = 'v1'
        fn.date = '2020apr01'
        fn.folder = f'results_{fn.date}'
        fn.base_path = f'{fn.folder}/paper_{fn.date}_{fn.version}'
        fn.sim_fig = f'{fn.base_path}_sim.png'
        fn.sim_obj = f'{fn.base_path}.sim'
        fn.ppl_obj = f'{fn.base_path}.ppl'
        fn.scens_fig = f'{fn.base_path}_scens.png'
        fn.scens_obj = f'{fn.base_path}.scens'

        # %% Parameters -- see equivalent list in calibration/run_sim.py
        sc.heading('Setting parameters...')
        total_pop = 330e6  # US population size
        n_days = 180
        pop_size = 10e3
        prev_pct = 0.1
        min_infected = 5
        start_day = dt.datetime(2020, 3, 20)
        pop_scale = round(total_pop / pop_size)
        # popchoices = ['random', 'microstructure'][1]  # Choose whether or not to use microstructure

        pop_infected = round(pop_size * prev_pct / 100)
        assert pop_infected > min_infected  # Avoid too small of numbers

        verbose = 1
        basepars = sc.objdict(
            pop_size=pop_size,
            pop_infected=pop_infected,
            n_days=n_days,
            start_day=start_day,
            pop_scale=pop_scale,
            pop_type='synthpops',
        )

        # %% Run settings
        sc.heading('Setting run configuration...')
        metapars = dict(
            n_runs=11,  # Number of parallel runs; change to 3 for quick, 11 for real
            noise=0.1,  # Use noise, optionally
            noisepar='beta',
            rand_seed=1,
            quantiles={'low': 0.1, 'high': 0.9},
        )

        today = sc.now()
        days_from_start = (today - basepars.start_day).days

        base_sim = cv.Sim(pars=basepars)
        if make_ppl:
            base_sim.initialize()
            if do_save:
                base_sim.save_people(filename=fn.ppl_obj)
        else:
            base_sim.load_people(filename=fn.ppl_obj)
            base_sim.initialize()

        n_people = base_sim['pop_size']
        npts = base_sim.npts

        # %% Define the scenarios
        sc.heading('Defining scenarios...')

        scenarios = {
            'BL': {
                'name': 'Baseline (no interventions)',
                'pars': {
                }
            },
            'CI': {
                'name': 'Case isolation in the home',
                'pars': {
                    'interventions': cv.change_beta(days=days_from_start, changes=0.5)  # Placeholder
                }
            },
            'HQ': {
                'name': 'Voluntary home quarantine',
                'pars': {
                    'interventions': cv.change_beta(days=days_from_start, changes=0.7)  # Placeholder
                }
            },
            'SDO': {
                'name': 'Social distancing of those over 70 years of age',
                'pars': {
                    'interventions': cv.change_beta(days=days_from_start, changes=0.9)  # Placeholder
                }
            },
            'SD': {
                'name': 'Social distancing of entire population',
                'pars': {
                    'interventions': cv.change_beta(days=days_from_start, changes=0.6)  # Placeholder
                }
            },
            'PC': {
                'name': 'Closure of schools and universities',
                'pars': {
                    'interventions': [cv.dynamic_pars({
                        'beta_pop': {
                            'days': days_from_start,
                            'vals': [{
                                'H': 3.0,
                                'S': 0.0,
                                'W': 1.0,
                                'R': 0.45,
                            }]
                        }
                    })]
                }
            },
        }

        scens = cv.Scenarios(sim=base_sim, metapars=metapars, scenarios=scenarios)
        scens.run(verbose=verbose, debug=debug)
