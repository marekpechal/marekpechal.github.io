import yaml
import matplotlib.pyplot as plt
import os
import datetime
import locale

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

data_path = os.path.join(os.path.dirname(__file__), '../../_data/hiking.yml')
output_dir = os.path.join(os.path.dirname(__file__), '../../assets/images')

with open(data_path, 'r') as file:
    hiking_data_yml = yaml.safe_load(file)

hike_dates = []
hike_lengths = []
hike_ele_gains = []
for hike in hiking_data_yml['hikes']:
    hike_dates.append(datetime.datetime.strptime(hike["date"], "%d.%m.%Y"))
    hike_lengths.append(hike["length"])
    hike_ele_gains.append(hike["elevation_gain"])

hike_dates_rel_days = [(dt-hike_dates[0]).days for dt in hike_dates]

en_to_cz = {
    "Jan": "Led",
    "Feb": "Úno",
    "Mar": "Bře",
    "Apr": "Dub",
    "May": "Kvě",
    "Jun": "Čer",
    "Jul": "Čvc",
    "Aug": "Srp",
    "Sep": "Zář",
    "Oct": "Říj",
    "Nov": "Lis",
    "Dec": "Pro",
    }

y = 2024
m = 1
ticks_rel_days = []
ticks_labels = {"en": [], "cz": []}
while True:
    dt = datetime.datetime.strptime(f"15.{m:02}.{y}", "%d.%m.%Y")
    rel_days = (dt-hike_dates[0]).days
    ticks_rel_days.append(rel_days)
    ticks_labels["en"].append(dt.strftime("%b %Y"))
    ticks_labels["cz"].append(en_to_cz[dt.strftime("%b")]+" "+dt.strftime("%Y"))
    if rel_days > max(hike_dates_rel_days):
        break
    m += 1
    if m == 13:
        y += 1
        m = 1

for lang in ["en", "cz"]:

    # --- individual hikes ---
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.bar(hike_dates_rel_days, hike_lengths, width=5, color=colors[0])
    plt.ylabel({"en": "Hike length [km]", "cz": "Délka trasy [km]"}[lang])
    plt.xticks(ticks_rel_days, ticks_labels[lang], rotation=90)
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.bar(hike_dates_rel_days, hike_ele_gains, width=5, color=colors[1])
    plt.ylabel({"en": "Hike elevation gain [m]", "cz": "Stoupání trasy [m]"}[lang])
    plt.xticks(ticks_rel_days, ticks_labels[lang], rotation=90)
    plt.grid()

    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)

    plt.savefig(os.path.join(output_dir, f'hiking_statistics_individual_{lang}.png'))
    plt.close()

    # --- cumulative ---
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    X = [hike_dates_rel_days[0]-50]
    Y = [0]
    for t, dl in zip(hike_dates_rel_days, hike_lengths):
        X.append(t)
        Y.append(Y[-1])
        X.append(t)
        Y.append(Y[-1]+dl)
    X.append(X[-1]+50)
    Y.append(Y[-1])
    plt.plot(X, Y, lw=3, color=colors[0])
    plt.ylabel({"en": "Total distance [km]", "cz": "Celková vzdálenost [km]"}[lang])
    plt.xticks(ticks_rel_days, ticks_labels[lang], rotation=90)
    plt.grid()

    plt.subplot(2, 1, 2)
    X = [hike_dates_rel_days[0]-50]
    Y = [0]
    for t, dh in zip(hike_dates_rel_days, hike_ele_gains):
        X.append(t)
        Y.append(Y[-1])
        X.append(t)
        Y.append(Y[-1]+dh)
    X.append(X[-1]+50)
    Y.append(Y[-1])
    plt.plot(X, Y, lw=3, color=colors[1])
    plt.ylabel({"en": "Total elevation gain [m]", "cz": "Celkové stoupání [m]"}[lang])
    plt.xticks(ticks_rel_days, ticks_labels[lang], rotation=90)
    plt.grid()

    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)

    plt.savefig(os.path.join(output_dir, f'hiking_statistics_cumulative_{lang}.png'))
    plt.close()
