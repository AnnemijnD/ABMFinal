# Agent Based Modelling UvA (2020): Theme Park Dynamics
Since people tend to avoid long waiting lines for attractions, theme parks aim to distribute thepeople over the attractions in the most optimal way. In this project, an agent based model is applied to evaluate dynamics of visitors in a theme park. Visitors with different strategies are simulated in a theme park. The focus of vistors' strategies will lie on distances between attractions and waiting lines. A visualization of a theme park is made with a [visualization toolkit of Mesa](https://mesa.readthedocs.io/en/master/apis/visualization.html).

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
This will automatically open up a UI on your standard browser. The UI consists of three buttons that change the parameters of the model. These are:
* Number of customers: default is set to 20
* Strategy choice: this will generate customers with a specific strategy.
  * Closest_by: customers will choose their next attraction based on distance and/or waitingtime.
  * Random: customers will choose a random attraction as their next destination
* Theme park lay-out: either circle or cluster.

To use the buttons, select your choice and click on "Reset" in the right top of the screen.

> :warning: **Sometimes the visualisation does not respond to the buttons when using Safari** The problem should be solved by using Google Chrome.


Furthermore, after starting the model, three charts are displayed. At the top, a pie chart that shows the ratio of all strategies at a specific moment.
Secondly, a linechart that shows the course of how many customers adopted which strategy. At last, a linechart showing the park efficiency score over time.


### Structure
* ```run.py```: main module to run the vizualisation of the model.
* ```sensitivity_analysis.py```: a module that is used to plot results of the OFAT sensitivity analysis.

#### /models

* ```attraction.py```: includes the agent Attraction.
* ```customer.py```: includes the agent Customer and helper functions such as ```get_destination()```.
* ```model.py```: includes the model Themepark and defines the Mesa grid and schedule.
* ```monitor.py```: makes predictions of an agent's move based on distance and wating time.
* ```route.py```: calculates coordinates of attractions and adds possible obstacles.
* ```server.py```: launches the mesa visualization.
* ```analyse.py```: analyse data and generates plots.
* ```main.py```: see description below

### Collect data
Data collection is done by running:
```
python models/main.py
```
This script will run 65 runs of the model with 1000 time steps. For example:

```
theme = "cluster"
strategy = "Random"
```
However, if data needs to be collected for a run with a different strategy, parameters may be changed:
```
theme = "circle"
strategy = "Closest_by"
```


### Analyse data
To analyse the data with plots, use ```analyse.py``` . Files and data to be included can be found in either the folder 'data' or 'results'. All functions require input of a specific file from the these folders, named as variable file. After running ```main.py```, data gets collected into the 'data' folder by default and can be directly analysed by changing the 'file' variables into the file of interest.

An example is:
```
file = pickle.load(open('data/all_rides.p', 'rb'))
```
The file names that are now included give an indication of what files can be plotted by which function.


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
