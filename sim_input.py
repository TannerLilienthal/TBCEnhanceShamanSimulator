import simulator
import tkinter as tk
from tkinter import ttk
import weapons
from matplotlib import pyplot as plt

# Root Window
root = tk.Tk()
root.geometry("640x480")
root.title('Enhance Shaman Simulator')
root.resizable(0, 0)

ap = tk.StringVar()
hit = tk.StringVar()
crit = tk.StringVar()
expertise = tk.StringVar()

# Configure the Grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(5, weight=2)


# --------------- CREATE GRAPH --------------- #
def create_graph(x_list, y_list):
    plt.plot(x_list, y_list)
    plt.show()


# --------------- STAT INPUTS --------------- #
# Stat Frame
stat_frame = tk.Frame(root)
stat_frame.grid(column=0, row=0)

# Attack Power
attackpower_label = ttk.Label(stat_frame, text="Attack Power:")
attackpower_label.grid(column=0, row=0, sticky=tk.E, padx=4, pady=4)

attackpower_entry = ttk.Entry(stat_frame, textvariable=ap)
attackpower_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
attackpower_entry.insert(0, 1500)
attackpower_entry.focus()

# Hit Chance
hit_label = ttk.Label(stat_frame, text="Hit Chance (%):")
hit_label.grid(column=0, row=1, sticky=tk.E, padx=4, pady=4)

hit_entry = ttk.Entry(stat_frame, textvariable=hit)
hit_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
hit_entry.insert(0, 20)


# Crit Chance
critchance_label = ttk.Label(stat_frame, text="Crit Chance (%):")
critchance_label.grid(column=0, row=2, sticky=tk.E, padx=4, pady=4)

critchance_entry = ttk.Entry(stat_frame, textvariable=crit)
critchance_entry.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
critchance_entry.insert(0, 20)


# Expertise Chance
expertise_label = ttk.Label(stat_frame, text="Expertise:")
expertise_label.grid(column=0, row=3, sticky=tk.E, padx=4, pady=4)

expertise_entry = ttk.Entry(stat_frame, textvariable=expertise)
expertise_entry.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
expertise_entry.insert(0, 4)

# --------------- WEAPON SELECTION --------------- #
weapon_frame = tk.Frame(root)
weapon_frame.grid(column=0, row=1)
weapon_frame["borderwidth"] = 5

# Mainhand
mh_wep_label = tk.Label(weapon_frame, text="Mainhand:")
mh_wep_label.grid(column=0, row=0, sticky=tk.E, padx=4, pady=4)
mh_wep = tk.StringVar()
mh_weapon_box = ttk.Combobox(weapon_frame, textvariable=mh_wep)
mh_weapon_box.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
mh_weapon_box["values"] = weapons.get_weapons()
mh_weapon_box["state"] = "readonly"
mh_weapon_box.current(0)

# Offhand
oh_wep_label = tk.Label(weapon_frame, text="Offhand:")
oh_wep_label.grid(column=0, row=1, sticky=tk.E, padx=4, pady=4)
oh_wep = tk.StringVar()
oh_weapon_box = ttk.Combobox(weapon_frame, textvariable=oh_wep)
oh_weapon_box.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
oh_weapon_box["values"] = weapons.get_weapons()
oh_weapon_box["state"] = "readonly"
oh_weapon_box.current(1)


# --------------- BUFF SELECTION --------------- #
self_buff_frame = tk.Frame(root)
self_buff_frame.grid(column=1, row=0, sticky=tk.W)
self_buffs_label = tk.Label(self_buff_frame, text="Self Buffs")
self_buffs_label.grid(column=0, row=0)

party_buff_frame = tk.Frame(root)
party_buff_frame.grid(column=2, row=0, sticky=tk.W)
party_buffs_label = tk.Label(party_buff_frame, text="Party Buffs")
party_buffs_label.grid(column=0, row=0)


def command_pass():
    pass


# Strength of Earth Totem
strength_of_earth_var = tk.IntVar(root)
strength_of_earth_check = ttk.Checkbutton(self_buff_frame, text="Strength of Earth Totem", command=command_pass,
                                          variable=strength_of_earth_var, onvalue=1, offvalue=0)
strength_of_earth_check.grid(column=0, row=1, sticky=tk.W)


# Grace of Air Totem
grace_of_air_var = tk.IntVar(root)
grace_of_air_check = ttk.Checkbutton(self_buff_frame, text="Grace of Air Totem", command=command_pass,
                                     variable=grace_of_air_var, onvalue=1, offvalue=0)
grace_of_air_check.grid(column=0, row=2, sticky=tk.W)


# Battle Shout (382 attack power)
battle_shout_var = tk.IntVar(root)
battle_shout_check = ttk.Checkbutton(party_buff_frame, text="Battle Shout", command=command_pass,
                                     variable=battle_shout_var, onvalue=1, offvalue=0)
battle_shout_check.grid(column=0, row=1, sticky=tk.W)


# Leader of the Pack (5% crit)
leader_of_the_pack_var = tk.IntVar(root)
leader_of_the_pack_check = ttk.Checkbutton(party_buff_frame, text="Leader of the Pack", command=command_pass(),
                                           variable=leader_of_the_pack_var, onvalue=1, offvalue=0)
leader_of_the_pack_check.grid(column=0, row=2, sticky=tk.W)


# --------------- NUMBER OF SIMULATIONS --------------- #
simulations_frame = tk.Frame(root)
simulations_frame.grid(column=0, row=2, sticky=tk.E, padx=20, pady=10)

# Total simulations and duration.
total_sims = tk.IntVar()
low = tk.Radiobutton(simulations_frame, text="100 Simulations", variable=total_sims, value=100)
low.grid(column=0, row=1)
medium = tk.Radiobutton(simulations_frame, text="500 Simulations", variable=total_sims, value=500)
medium.grid(column=0, row=2)
high = tk.Radiobutton(simulations_frame, text="999 Simulations", variable=total_sims, value=999)
high.grid(column=0, row=3)
total_sims.set(100)

duration = tk.IntVar()
duration_label = tk.Label(simulations_frame, text="Total seconds of encounter:")
duration_label.grid(column=0, row=4, sticky=tk.E, padx=4, pady=4)
duration_entry = ttk.Entry(simulations_frame, textvariable=duration, width=5)
duration_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)
duration_entry.insert(0, 6)


# --------------- BUTTONS --------------- #
submit_frame = tk.Frame(root)
submit_frame.grid(column=0, row=5)


# Submit Function
def submit():
    # Gather inputs for stats to send to simulator
    attack_power = int(ap.get()) + 224*strength_of_earth_var.get() + 382*battle_shout_var.get()
    hit_chance = float(hit.get())
    crit_chacne = float(crit.get()) + round((88/25)*grace_of_air_var.get() + 5*leader_of_the_pack_var.get(), 2)
    exp_val = int(expertise.get())
    # dps_list goes [mh_white, oh_white, mh_wf, oh_wf, ss, fs, es, total]
    dps_list = simulator.main(attack_power, hit_chance, crit_chacne, exp_val, mh_wep.get(), oh_wep.get(),
                              duration.get(), total_sims.get())[0]

    # DPS Output
    total_dps_label = ttk.Label(submit_frame, text=f"Total DPS: {dps_list[-1]}")
    total_dps_label.grid(column=1, row=0)


# Simulate Button
simulate_button = ttk.Button(submit_frame, text="Simulate", command=submit)
simulate_button.grid(column=0, row=0)


# Graph Function
def graph():
    # Gather data from simulation
    attack_power = int(ap.get()) + 224*strength_of_earth_var.get() + 382*battle_shout_var.get()
    hit_chance = float(hit.get())
    crit_chacne = float(crit.get()) + round((88/25)*grace_of_air_var.get() + 5*leader_of_the_pack_var.get(), 2)
    exp_val = int(expertise.get())
    # dps_list goes [mh_white, oh_white, mh_wf, oh_wf, ss, fs, es, total] x_data is time and y_data is dps
    dps_list, x_data, y_data = simulator.main(attack_power, hit_chance, crit_chacne, exp_val, mh_wep.get(),
                                              oh_wep.get(), duration.get(), 1)
    create_graph(x_data, y_data)


# Graph Button
graph_button = ttk.Button(submit_frame, text="Graph DPS", command=graph)
graph_button.grid(column=0, row=1)


root.mainloop()
