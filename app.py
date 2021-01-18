import matplotlib.pyplot as plt
import seaborn

plt.figure(figsize=(12,2.5))

# random values for x and y

x_values = [10,20,30,40,50]
y1_values = [100, 50, 75, 40, 80]

plt.plot(x_values, y1_values)

# use the same x-values but different y-values
y2_values = [10, 75, 25, 80, 40]

plt.plot(x_values, y2_values )

plt.legend(['line 1','line 2'])
plt.show()
