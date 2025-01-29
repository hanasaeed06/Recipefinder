from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize parking system
class ParkingSystem:
    def __init__(self, capacity):
        self.capacity = capacity
        self.parking_slots = []  # Stack to represent parked cars
        self.waiting_line = []  # Queue to represent waiting cars

    def park_car(self, car_number):
        if len(self.parking_slots) < self.capacity:
            self.parking_slots.append(car_number)
            return f"Car {car_number} parked."
        else:
            self.waiting_line.append(car_number)
            return f"Parking full. Car {car_number} added to the waiting line."

    def remove_car(self, car_number):
        if car_number in self.parking_slots:
            self.parking_slots.remove(car_number)
            if self.waiting_line:
                next_car = self.waiting_line.pop(0)
                self.parking_slots.append(next_car)
                return f"Car {car_number} removed. Car {next_car} moved from waiting line to parking lot."
            return f"Car {car_number} removed."
        return f"Car {car_number} not found in the parking lot."

# Initialize with default capacity
parking_system = ParkingSystem(capacity=5)

@app.route('/')
def index():
    return render_template(
        'index.html', 
        parking_slots=parking_system.parking_slots, 
        waiting_line=parking_system.waiting_line
    )

@app.route('/park', methods=['POST'])
def park():
    car_number = request.form.get('car_number')
    if car_number:
        message = parking_system.park_car(car_number)
        return redirect(url_for('index', message=message))
    return redirect(url_for('index'))

@app.route('/remove', methods=['POST'])
def remove():
    car_number = request.form.get('car_number')
    if car_number:
        message = parking_system.remove_car(car_number)
        return redirect(url_for('index', message=message))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
