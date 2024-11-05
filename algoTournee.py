# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 09:59:06 2024

@author: ocean
"""

import numpy as np
import random
import matplotlib.pyplot as plt

# Génère les données de distances et de villes
def generate_data(num_cities, max_distance=100, max_circuits=10):
    distances = np.random.randint(1, max_distance, size=(num_cities, num_cities))
    np.fill_diagonal(distances, 0)
    circuits = [0] + [random.randint(1, max_circuits) 
    for i in range(num_cities - 1)]
    return distances, circuits

# Paramètres du problème
num_cities = 10
vehicle_capacity = 15
time_constraint = 400
max_vehicles = 4

# Générer les données
distances, demands = generate_data(num_cities)

def clarke_wright_savings(distances, demands, vehicle_capacity):
    n = len(distances)
    routes = [[i] for i in range(1, n)]
    savings = []

    for i in range(1, n):
        for j in range(i+1, n):
            saving = distances[0][i] + distances[0][j] - distances[i][j]
            savings.append((saving, i, j))

    savings.sort(reverse=True, key=lambda x: x[0])

    for saving, i, j in savings:
        route_i = next((r for r in routes if i in r), None)
        route_j = next((r for r in routes if j in r), None)
        
        if route_i != route_j and sum(demands[k] for k in route_i + route_j) <= vehicle_capacity:
            routes.remove(route_i)
            routes.remove(route_j)
            routes.append(route_i + route_j)

    return routes

def total_distance(route, distances):
    return sum(distances[route[i-1]][route[i]] for i in range(len(route)))

def solve_vrp(distances, demands, vehicle_capacity, time_constraint, max_vehicles):
    routes = clarke_wright_savings(distances, demands, vehicle_capacity)
    
    # Initialisation des tournées des camions
    vehicle_routes = []
    for route in routes:
        vehicle_routes.append([0] + route + [0])
    
    # Vérification de la contrainte de temps et de capacité
    for vehicle_route in vehicle_routes:
        if total_distance(vehicle_route, distances) > time_constraint:
            print("Solution initiale ne respecte pas la contrainte de temps.")
            return None
    
    if len(vehicle_routes) > max_vehicles:
        print("Solution initiale nécessite plus de véhicules que disponible.")
        return None
    
    return vehicle_routes

# Résolution du problème de VRP
vehicle_routes = solve_vrp(distances, demands, vehicle_capacity, time_constraint, max_vehicles)

# Générer des coordonnées pour les villes
def generate_coordinates(num_cities, scale=100):
    coordinates = np.random.rand(num_cities, 2) * scale
    return coordinates

coordinates = generate_coordinates(num_cities)

# Tracer les routes des véhicules
def plot_routes(coordinates, vehicle_routes):
    plt.figure(figsize=(10, 8))
    colors = plt.cm.get_cmap('tab20', len(vehicle_routes))
    
    # Tracer les chemins des camions
    for i, route in enumerate(vehicle_routes):
        for j in range(len(route) - 1):
            start, end = route[j], route[j + 1]
            plt.plot([coordinates[start][0], coordinates[end][0]], 
                     [coordinates[start][1], coordinates[end][1]], 
                     color=colors(i), label=f'Camion {i + 1}' if j == 0 else "")

    # Tracer les villes et le dépôt
    for i, coord in enumerate(coordinates):
        if i == 0:
            plt.scatter(coord[0], coord[1], color='red', s=100, zorder=5, label='Dépôt')
        else:
            plt.scatter(coord[0], coord[1], color='blue', s=50, zorder=5)
            plt.text(coord[0], coord[1], str(i), fontsize=12, ha='right')

    plt.legend()
    plt.title("Tournées des véhicules")
    plt.xlabel("km")
    plt.ylabel("km")
    plt.grid(True)
    plt.show()

if vehicle_routes:
    for i, route in enumerate(vehicle_routes):
        print(f"Tournée du véhicule {i+1}: {route} avec distance totale: {total_distance(route, distances)}")
    
    plot_routes(coordinates, vehicle_routes)