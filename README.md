# Agent Based Modelling UvA (2020): Theme Park Dynamics
In this project, ABM us used to simulate visitors of a theme park. The focus will be on distances between attractions and waiting lines. A visualization of a theme park is made with a [visualization toolkit of Mesa](https://mesa.readthedocs.io/en/master/apis/visualization.html).

## Example visualization of model run
![Alt Text](https://github.com/rebeccadavidsson/ABM/blob/master/abm.gif)

### Requirements
All requirements can be installed with:
```
pip install -r requirements.txt
```
Installing:
* Mesa
* matplotlib
* numpy
* pickle

### Repository

* ```run.py```: main file to run. Run with the command:
```
python3 run.py
```
or
```
mesa runserver
```

#### /models

* ```attraction.py```: includes the agent Attraction.
* ```customer.py```: includes the agent Customer and helper functions such as ```get_destination()```.
* ```model.py```: includes the model Themepark and defines the Mesa grid and schedule.
* ```monitor.py```: makes predictions of an agent's move based on distance and wating time.
* ```route.py```: calculates coordinates of attractions and adds possible obstacles.
* ```server.py```: launches the mesa visualization.

### Built with
* [Mesa](https://github.com/projectmesa/mesa) - ABM Framework
* [Matplotlib](https://matplotlib.org) - 2D plotting

### Authors
* __R. Davidsson__
* __S. Donker__
* __A. Dijkhuis__
* __R. van Drimmelen__
* __L. Heek__
* __S. Verhezen__

## License
This project is licensed under the GNU General Public License v3.0.
