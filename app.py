from flask import Flask, request, render_template
from collections import deque

app = Flask(__name__)

# Lista de enfermedades y tratamientos 
illnesses = ["Fever", "Cough", "Infection", "Wound", "Skin Disease"]
treatments = ["Antibiotics", "Surgery", "Bandaging", "Vaccination", "Pain Relief"]

# Clase Animal que define las propiedades de cada animal
class Animal:
    def __init__(self, name, species, age, illness=None, treatment=None):
        self.name = name
        self.species = species
        self.age = age
        self.illness = illness
        self.treatment = treatment

# Clase VeterinaryClinic que administra el comportamiento de la clínica
class VeterinaryClinic:
    def __init__(self):
        self.animals = []  
        self.waiting_queue = deque() 
        self.consultation_stack = []  
        self.treatment_plans = {}  
        self.animal_array = [] 
        self.history = []  

    def add_animal(self, animal):
        self.animals.append(animal)
        self.animal_array.append(animal.name) 
        # Agregar el animal al historial
        self.history.append({
            "name": animal.name,
            "species": animal.species,
            "age": animal.age,
            "illness": animal.illness,
            "treatment": animal.treatment
        })

    def add_to_waiting_queue(self, animal):
        self.waiting_queue.append(animal)

    def consult_animal(self):
        if self.waiting_queue:
            animal = self.waiting_queue.popleft()
            self.consultation_stack.append(animal)
            return f"Consulting {animal.name} ({animal.species})"
        else:
            return "No animals waiting for consultation"

    def finish_consultation(self):
        if self.consultation_stack:
            animal = self.consultation_stack.pop()
            self.treatment_plans[animal.name] = {
                "species": animal.species,
                "age": animal.age,
                "illness": animal.illness,
                "treatment": animal.treatment
            }
            return f"Finished consulting {animal.name} ({animal.species})"
        else:
            return "No animals being consulted"

    def display_treatment_plans(self):
        plans = []
        for i, (animal_name, plan) in enumerate(self.treatment_plans.items()):
            plans.append(f"Treatment Plan {i+1}: {animal_name} ({plan['species']}) - Age: {plan['age']} - Illness: {plan['illness']} - Treatment: {plan['treatment']}")
        return "<br>".join(plans)

    def display_animal_array(self):
        animals = []
        for animal in self.animal_array:
            animals.append(animal)
        return "<br>".join(animals)

    def display_history(self):
        history_list = []
        for i, animal in enumerate(self.history):
            history_list.append(f"Animal {i+1}: {animal['name']} ({animal['species']}) - Age: {animal['age']} - Illness: {animal['illness']} - Treatment: {animal['treatment']}")
        return "<br>".join(history_list)

clinic = VeterinaryClinic()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")
        species = request.form.get("species")
        age = request.form.get("age")
        illness = request.form.get("illness")
        treatment = request.form.get("treatment")

        if action == "add_animal":
            if name and species and age:  
                try:
                    age = int(age) 
                    animal = Animal(name, species, age, illness, treatment)
                    clinic.add_animal(animal)
                    clinic.add_to_waiting_queue(animal)
                    selection_info = f"<strong>Selected Illness:</strong> {illness}<br><strong>Selected Treatment:</strong> {treatment}"
                    return render_template("index.html", illnesses=illnesses, treatments=treatments, selection_info=selection_info)

                except ValueError:
                    return render_template("index.html", illnesses=illnesses, treatments=treatments, error="Invalid age. Please enter a valid number for the age.")

            else:
                return render_template("index.html", illnesses=illnesses, treatments=treatments, error="Please fill in all fields: name, species, and age.")

        elif action == "consult_animal":
            result = clinic.consult_animal()
            return render_template("index.html", illnesses=illnesses, treatments=treatments, result=result)

        elif action == "finish_consultation":
            result = clinic.finish_consultation()
            return render_template("index.html", illnesses=illnesses, treatments=treatments, result=result)

        elif action == "display_treatment_plans":
            treatment_plans = clinic.display_treatment_plans()
            return render_template("index.html", illnesses=illnesses, treatments=treatments, treatment_plans=treatment_plans)

        elif action == "display_animal_array":
            animal_array = clinic.display_animal_array()
            return render_template("index.html", illnesses=illnesses, treatments=treatments, animal_array=animal_array)

        elif action == "show_history":
            history = clinic.display_history()
            return render_template("index.html", illnesses=illnesses, treatments=treatments, history=history)

    return render_template("index.html", illnesses=illnesses, treatments=treatments)

if __name__ == "__main__":
    app.run(debug=True)
