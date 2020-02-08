from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import PieChartModule
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
try:
    from model import Themepark
    from customer import Customer
    from route import Route
    from attraction import Attraction
except ModuleNotFoundError:
    from .model import Themepark
    from .customer import Customer
    from .route import Route
    from .attraction import Attraction

width = 36
height = 36
N_cust = 50
pixel_ratio = 20
num_agents = 12
max_time = 300

STEPS = max_time
MEMORY = 6


def agent_draw(agent):
    if agent is None:
        return
    portrayal = {}

    if type(agent) is Route:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "grey"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Layer"] = 0

    elif type(agent) is Attraction:
        portrayal["Color"] = "purple"
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 2
        portrayal["r"] = 1
        portrayal["text"] = str(agent.current_waitingtime)
        portrayal["text_color"] = "black"

    elif type(agent) is Customer:

        portrayal["Layer"] = 1
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.65

        if agent.waiting is False:
            portrayal["text"] = agent.unique_id
            portrayal["text_color"] = "black"

        if agent.weight == 0.0:
            portrayal["Color"] = "#F6412D"
        elif agent.weight == 0.25:
            portrayal["Color"] = "#FF5607"
        elif agent.weight == 0.5:
            portrayal["Color"] = "#FF9800"
        elif agent.weight == 0.75:
            portrayal["Color"] = "#FFC100"
        elif agent.weight == 1.0:
            portrayal["Color"] = "#FFEC19"
        elif agent.strategy == "Random" or agent.strategy == "Random_test_4":
            portrayal["Color"] = "#add8e6"

    return portrayal


class HistogramModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["HistogramModule.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.data = []
        new_element = "new HistogramModule({}, {}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height,
                                         self.data)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        """Render a histogram with HistogramModule.js"""

        data = model.calculate_people()
        return data


grid = CanvasGrid(agent_draw, width, height, width * pixel_ratio, height * pixel_ratio)

# try:
chart = PieChartModule([
                    {"Label": "Random", "Color": "#add8e6"},
                    {"Label": "0.00", "Color": "#F6412D"},
                    {"Label": "0.25", "Color": "#FF5607"},
                    {"Label": "0.50", "Color": "#FF9800"},
                    {"Label": "0.75", "Color": "#FFC100"},
                    {"Label": "1.00", "Color": "#FFEC19"},
                    ], data_collector_name='datacollector')
linechart = ChartModule([
                    {"Label": "Random", "Color": "#add8e6"},
                    {"Label": "0.00", "Color": "#F6412D"},
                    {"Label": "0.25", "Color": "#FF5607"},
                    {"Label": "0.50", "Color": "#FF9800"},
                    {"Label": "0.75", "Color": "#FFC100"},
                    {"Label": "1.00", "Color": "#FFEC19"},
                    ], data_collector_name='datacollector')

linechart_2 = ChartModule([
                    {"Label": "score", "Color": "#F6412D"},
                    ], data_collector_name='datacollector2')

histogram = HistogramModule(["Attraction1", "Attraction2", "Attraction3",
                            "Attraction4", "Attraction5"], 20, 50)

model_params = {
    "height": height,
    "width": width,
    "N_attr": UserSettableParameter("slider", "Number of attractions", num_agents, 1, num_agents, 1),
    "N_cust": UserSettableParameter("slider", "Number of customers", int(N_cust/1.5), 1, N_cust * 2, 1),
    "strategy": UserSettableParameter('choice', 'Strategy choice', value='Closest_by',
                                      choices=['Random', 'Closest_by']),
    "theme": UserSettableParameter('choice', 'Theme park lay-out', value='circle',
                                   choices=['random', 'circle', 'cluster']),
    "max_time": max_time,
    "weight": UserSettableParameter("slider", "Weight of waitingtime", 0, 0, 1, 0.25),
    "adaptive": True
}

server = ModularServer(
    Themepark,
    [grid, histogram, chart, linechart, linechart_2],
    "Theme Park Model",
    model_params,
)
server.max_steps = 0
server.port = 8521
