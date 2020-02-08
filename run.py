from models.server import server

server.launch()


# zo werkt pickle:
# 1. terminal/bash: pip install pickle
# 2. import pickle
# 3. data opslaan  = pickle.dump(<datanaam>, open(picklename.p, 'wb'))
# 4. data openene = pickle.load(open('filename.p', 'rb'))
