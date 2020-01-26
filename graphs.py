import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

objects = ('0.1','0.5',"0.9")
y_pos = np.arange(len(objects))
performance = [900.98,301.545,243.27]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Time')
plt.xlabel('Evaporation constant')
plt.title('Evaporation constant changes in medium maze')

plt.show()
