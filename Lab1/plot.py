import numpy as np
import matplotlib.pyplot as plt
from pyorbital.orbital import Orbital
from pyorbital import tlefile
from datetime import datetime, timedelta


sat = Orbital('NOAA 19', tle_file='noaa19.txt')
#utc_time = datetime(2022, 3, 18)
utc_time = datetime.utcnow()
length = 24
lat, lon = 55.920625, 37.557141
alt = 0.185
passes = sat.get_next_passes(utc_time, length, lon, lat, alt)
out = "В течение следующих " + str(length) + " часов ожидается " + str(len(passes)) + " пролётов:\n"

fig, ax = plt.subplots(figsize=(8, 7), dpi=100, subplot_kw={'projection': 'polar'})

index = 1
for i in passes:
    az, el = [], []
    j = i[0]
    out += str(i[0]) + " - " + str(i[1]) + '\n'
    while j <= i[1]:
        tmp = sat.get_observer_look(j, lon, lat, alt)
        az.append(tmp[0])
        el.append(tmp[1])
        j += timedelta(seconds=5)
    tmp = sat.get_observer_look(i[1], lon, lat, alt)
    az.append(tmp[0])
    el.append(tmp[1])
    ax.plot(np.array(az) / 180 * np.pi, np.array(el), label=str(index))
    index += 1

f = open('passes.txt', 'w')
print(out)
f.write(out)
f.close()
ax.set_rlim(90, 0)
ax.set_rlabel_position(0)
ax.yaxis.set_tick_params(labelsize=8)
ax.set_theta_direction(-1)
ax.grid(True)
ax.set_theta_zero_location('N')
ax.set_thetagrids(np.arange(0.0, 360.0, 30.0))
angle = np.deg2rad(0)
ax.legend(loc="lower left", bbox_to_anchor=(.6 + np.cos(angle)/2, .5 + np.sin(angle)/2))
fig.subplots_adjust(left=0.0)
plt.show()

fig.savefig('sat.png', dpi=500)
