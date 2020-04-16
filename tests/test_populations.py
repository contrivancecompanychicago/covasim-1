'''
Testing populations in Covasim
'''

#%% Imports and settings
import os
import covasim as cv
import unittest

from unittest_support_classes import CovaSimTest, TestProperties

TPKeys = TestProperties.ParameterKeys.SimulationKeys
ResKeys = TestProperties.ResultsDataKeys


def del_file(filename, dir=None):
    if dir:
        filepath = os.path.join(dir, filename)
    else:
        filepath = os.path.join(os.path.curdir, filename)

    if os.path.exists(filepath):
        print(filepath)
        os.remove(filepath)


class TestPopulations(CovaSimTest):

    def setUp(self):
        pass

    def tearDown(self):
        cached_population_filename_1 = os.path.join('test_data', 'example_population_100.ppl')
        del_file(cached_population_filename_1)
        cached_population_filename_2 = os.path.join('test_data', 'example_population_5000.ppl')
        del_file(cached_population_filename_2)

    def test_save_load_synthpops_population(self):
        # Simulation parameters
        params = {
            "pop_size": 100,  # Population size
            "pop_infected": 10,  # Initial infections
            "start_day": "2020-03-20",
            "n_days": 180,
            "pop_type": "synthpops",
            "use_layers": True
        }

        # Store the filename
        cached_population_filename = f'example_population_{params["pop_size"]}.ppl'

        base_sim = cv.Sim(pars=params)
        # save the population
        save_pop = base_sim.save_population(cached_population_filename)
        # now load it
        load_pop = base_sim.load_population(cached_population_filename)

        # and compare
        self.assertEqual(save_pop, load_pop)

        # Test cleanup - delete file
        del_file(cached_population_filename)

    def test_random_load_population(self):

        # Simulation parameters
        params = {
            "pop_size": 100,  # Population size -- choices are 5000, 10000, 20000, 50000, 100000, 122000
            "pop_infected": 10,  # Initial infections
            "start_day": "2020-01-15",
            "n_days": 60,
            "pop_type": "random",
            "use_layers": True
        }

        # Store the filename
        cached_population_filename = f'example_population_{params["pop_size"]}.ppl'

        # Create the simulation
        sim = cv.Sim(params)
        save_pop = sim.save_population(cached_population_filename)
        # Now load the population
        load_pop = sim.load_population(cached_population_filename)

        # and compare
        self.assertEqual(save_pop, load_pop)

        # Test cleanup - delete file
        del_file(cached_population_filename)

    def test_clustered_load_population(self):

        load_population = False
        save_population = True

        # Simulation parameters
        params = {
            "pop_size": 100,  # Population size -- choices are 5000, 10000, 20000, 50000, 100000, 122000
            "pop_infected": 10,  # Initial infections
            "start_day": "2020-01-15",
            "n_days": 60,
            "pop_type": "clustered",
            "use_layers": True
        }

        # Store the filename
        cached_population_filename = f'example_population_{params["pop_size"]}.ppl'

        # Create the simulation
        sim = cv.Sim(params)
        if load_population:
            sim.load_population(cached_population_filename)

        # Run the simulation
        sim.run()
        sim.plot()

        # Optionally save
        if save_population:
            sim.save_population(cached_population_filename)

        pop_10_infected = self.get_day_zero_channel_value()
        self.assertEqual(pop_10_infected, sim[TPKeys.initial_infected_count])

        # Test cleanup - delete file
        del_file(cached_population_filename)

        pass

    def test_load_pregenerated_file(self):

        # Simulation parameters
        params = {
            "pop_size": 100000,  # Population size -- choices are 5000, 10000, 20000, 50000, 100000, 122000
            "pop_infected": 10,
            "start_day": "2020-01-15",
            "n_days": 60,
            "pop_type": "synthpops",
            "use_layers": True
        }

        cached_population_filename = os.path.join('test_data',
                                                  'example_population_{:d}.ppl'.format(int(params['pop_size'])))
        sim = cv.Sim(params)
        # sim.load_population(cached_population_filename)
        sim.run()

        pop_10_infected = self.get_day_zero_channel_value()
        self.assertEqual(pop_10_infected, sim[TPKeys.initial_infected_count])

        # Test cleanup - delete file
        del_file(cached_population_filename)

        pass


if __name__ == '__main__':
    unittest.main()
