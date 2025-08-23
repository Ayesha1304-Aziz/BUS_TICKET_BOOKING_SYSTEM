# Bus data: bus_id: (route, time, fare, seats_available)
buses = {
    1: ("north nazimabad - power house", "09:00 AM", 500, 30),
    2: ("kda - gulshan", "12:00 PM", 700, 30),
    3: ("ayesha manzil - bahria", "05:00 PM", 600, 30)
}

bookings = []  # List to store booked tickets

# Function to view bus schedules
def view_buses():
    print("\n--- Available Bus Schedules ---")
    for bus_id, details in buses.items():
        route, time, fare, seats = details
        print(f"ID: {bus_id} | Route: {route} | Time: {time} | Fare: {fare} | Seats Left: {seats}")
    print()

# Function to book a ticket
def book_ticket():
    view_buses()
    bus_id = int(input("Enter Bus ID to book: "))
   
    if bus_id in buses and buses[bus_id][3] > 0:
        name = input("Enter your name: ")
        seats = int(input("Enter number of seats: "))
        if seats <= buses[bus_id][3]:  # Check available seats
            total_fare = seats * buses[bus_id][2] 
            bookings.append({"name": name, "bus_id": bus_id, "seats": seats, "total_fare": total_fare})
            # Update available seats in booking list in simple storing data of booked seats
            route, time, fare, available = buses[bus_id]
            buses[bus_id] = (route, time, fare, available - seats)
            print(f"Booking successful! Total Fare: {total_fare}\n")
        else:
            print("Not enough seats available.\n")
    else:
        print("Invalid Bus ID or no seats available.\n")

# Function to cancel a booking
def cancel_booking():
    name = input("Enter your name to cancel booking: ")
    for booking in bookings:
        if booking["name"].lower() == name.lower():
            bus_id = booking["bus_id"]
            seats = booking["seats"]
            # Restore seats
            route, time, fare, available = buses[bus_id]
            buses[bus_id] = (route, time, fare, available + seats)
            bookings.remove(booking)
            print("Booking cancelled successfully!\n")
            return
    print("Booking not found.\n")

# Function to view all bookings
def view_bookings():
    if not bookings:
        print("No bookings yet.\n")
    else:
        print("\n--- Booked Tickets ---")
        for b in bookings:
            route, time, fare, _ = buses[b["bus_id"]]
            print(f"Name: {b['name']}, Route: {route}, Time: {time}, Seats: {b['seats']}, Total Fare: {b['total_fare']}")
        print()

# Main loop
while True:
    print("0. Exit")
    print("1. View Bus Schedules")
    print("2. Book Ticket")
    print("3. Cancel Booking")
    print("4. View My Bookings")
   
    choice = input("Enter your choice: ")
   
    if choice == "0":
        print("Exiting Bus Ticket Booking System...")
        break
    elif choice == "1":
        view_buses()
    elif choice == "2":
        book_ticket()
    elif choice == "3":
        cancel_booking()
    elif choice == "4":
        view_bookings()
    else:
        print("Invalid choice, try again.\n")



