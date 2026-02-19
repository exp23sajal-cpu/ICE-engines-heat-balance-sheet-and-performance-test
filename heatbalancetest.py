import math
import matplotlib.pyplot as plt

# ENGINE SELECTION

print("Select Engine Type:")
print("1. Diesel Engine")
print("2. Petrol Engine")

choice = int(input("Enter choice (1 or 2): "))

# ENGINE CONSTANTS (Based on Type)

if choice == 1:
    engine_type = "Diesel"
    Cv = 45500        # kJ/kg
    Sp_gravity = 0.82
    FP = 0.75         # kW
else:
    engine_type = "Petrol"
    Cv = 47000        # kJ/kg (typical petrol CV)
    Sp_gravity = 0.74
    FP = 0.60         # slightly lower friction power

print(f"\nSelected Engine: {engine_type}")

# FIXED CONSTANTS


g = 9.81
rho_water = 1000
R_air = 287
Patm = 101325
Tamb = 298
theta_gen = 0.80
Cd = 0.6
d_orifice = 0.02
Cp_water = 4.187
Cp_exhaust = 1.005

# Engine geometry
k = 1
L = 0.11
D = 0.08
A = math.pi * D**2 / 4

# INPUT OBSERVATION TABLE

n = int(input("\nEnter number of load readings: "))

# Lists for plotting
BMEP_list = []
SFC_list = []
eta_bt_list = []
eta_m_list = []
Load_list = []

print("\n----- ENTER OBSERVATION DATA -----")

for i in range(n):

    print(f"\n--- Reading {i+1} ---")

    Load = float(input("Load (W): "))
    V = float(input("Voltage (V): "))
    I = float(input("Current (A): "))
    N = float(input("Speed (RPM): "))
    t = float(input("Time for 10cc fuel (sec): "))
    h1 = float(input("Manometer h1 (mm): "))
    h2 = float(input("Manometer h2 (mm): "))
    T1 = float(input("Cooling water inlet temp (°C): "))
    T2 = float(input("Cooling water outlet temp (°C): "))
    T4 = float(input("Exhaust gas temp (°C): "))
    mw = float(input("Cooling water flow rate (kg/s): "))

    # CALCULATIONS
    

    # Fuel mass flow rate
    mf = (10 * Sp_gravity) / (t * 1000)

    # Brake Power
    BP = (V * I) / (1000 * theta_gen)

    # Indicated Power
    IP = BP + FP

    # Efficiencies
    eta_m = (BP / IP) * 100 if IP != 0 else 0
    Qin = mf * Cv
    eta_bt = (BP / Qin) * 100 if Qin != 0 else 0
    SFC = (mf * 3600) / BP if BP != 0 else 0

    # BMEP
    BMEP = (BP * 60 * 1000) / (L * A * N * (k/2))
    BMEP_bar = BMEP / 1e5

    # Air calculations
    Hw = (h1 + h2) / 1000
    rho_air = Patm / (R_air * Tamb)
    Ha = (Hw * rho_water) / 1.2
    ma = rho_air * Cd * (math.pi * d_orifice**2 / 4) * math.sqrt(2 * g * Ha)
    m_ex = ma + mf

    # Heat balance
    Qw = mw * Cp_water * (T2 - T1)
    Qe = m_ex * Cp_exhaust * (T4 - 25)
    Q_un = Qin - (BP + Qw + Qe)

    # PRINT RESULTS
   

    print("\n--- PERFORMANCE RESULTS ---")
    print(f"Brake Power = {BP:.3f} kW")
    print(f"Indicated Power = {IP:.3f} kW")
    print(f"Mechanical Efficiency = {eta_m:.2f} %")
    print(f"Brake Thermal Efficiency = {eta_bt:.2f} %")
    print(f"SFC = {SFC:.3f} kg/kWh")
    print(f"BMEP = {BMEP_bar:.3f} bar")

    print("\n--- HEAT BALANCE ---")
    print(f"Heat Input = {Qin:.3f} kW")
    print(f"Cooling Water Loss = {Qw:.3f} kW")
    print(f"Exhaust Gas Loss = {Qe:.3f} kW")
    print(f"Unaccounted Loss = {Q_un:.3f} kW")

    # Store for plotting
    Load_list.append(Load)
    BMEP_list.append(BMEP_bar)
    SFC_list.append(SFC)
    eta_bt_list.append(eta_bt)
    eta_m_list.append(eta_m)

# VISUALIZATION

# 1. BMEP vs SFC
plt.figure()
plt.plot(BMEP_list, SFC_list, marker='o')
plt.xlabel("BMEP (bar)")
plt.ylabel("SFC (kg/kWh)")
plt.title(f"{engine_type} Engine: BMEP vs SFC")
plt.grid(True)
plt.show()

# 2. BMEP vs Brake Thermal Efficiency
plt.figure()
plt.plot(BMEP_list, eta_bt_list, marker='o')
plt.xlabel("BMEP (bar)")
plt.ylabel("Brake Thermal Efficiency (%)")
plt.title(f"{engine_type} Engine: BMEP vs Brake Thermal Efficiency")
plt.grid(True)
plt.show()

# 3. BMEP vs Mechanical Efficiency
plt.figure()
plt.plot(BMEP_list, eta_m_list, marker='o')
plt.xlabel("BMEP (bar)")
plt.ylabel("Mechanical Efficiency (%)")
plt.title(f"{engine_type} Engine: BMEP vs Mechanical Efficiency")
plt.grid(True)
plt.show()

# 4. Load vs Brake Power Trend
plt.figure()
plt.plot(Load_list, BMEP_list, marker='o')
plt.xlabel("Load (W)")
plt.ylabel("BMEP (bar)")
plt.title(f"{engine_type} Engine: Load vs BMEP")
plt.grid(True)
plt.show()

