# HTG Robotics #

Robotic horizontal gene transfer simulation. Here's how to run an experiment.

## Petri Dish ##

An example of an experiment is found in 'examplePetriA.py'. Each of the parameters is explained in the file 'PetriDish.py' at the header of the PetriDish class. To start a new experiment, copy the layout of the 'examplePetriA.py' file and make sure you define a unique 'nametag' for the experiment.

You will also want to make your own custom HTG Method which defines how genes are selected within a robot. New methods should be added to the 'HTGmethods.py' file and imported into your petri dish example file. 

## Running An Experiment ##

![alt text](imgs/instructions.png)

* Move mouse over a robot to display its ID number and position.
* Data is saved in the '/outputs' directory as a '.csv' file, with a file name similar to your experiment name.

## Working Features ##

TODO features:

1. Fitness function incorporation.
2. Recording/Saving data for gene transfers.
3. Fitness-dependent gene-transfer.
4. Fitness-proportional gene-selection.
