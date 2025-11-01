import streamlit as st
import pandas as pd

# -----------------------------
# Data
# -----------------------------
buses = {
    1: ("north nazimabad - power house", "09:00 AM", 500, 30),
    2: ("kda - gulshan", "12:00 PM", 700, 30),
    3: ("ayesha manzil - bahria", "05:00 PM", 600, 30)
}

# Session state to persist data across interactions
if "buses" not in st.session_state:
    st.session_state.buses = buses
if "bookings" not in st.session_state:
    st.session_state.bookings = []


# -----------------------------
# Functions
# -----------------------------
def view_buses():
    st.subheader("🚌 Available Bus Schedules")
    df = pd.DataFrame(
        [(bid, *details) for bid, details in st.session_state.buses.items()],
        columns=["Bus ID", "Route", "Time", "Fare", "Seats Available"]
    )
    st.dataframe(df, use_container_width=True)


def book_ticket():
    st.subheader("🎟️ Book a Ticket")
    view_buses()

    bus_id = st.selectbox("Select Bus ID", list(st.session_state.buses.keys()))
    name = st.text_input("Enter your name")
    seats = st.number_input("Number of seats", min_value=1, max_value=10, step=1)

    if st.button("Book Now"):
        route, time, fare, available = st.session_state.buses[bus_id]

        if available >= seats:
            total_fare = seats * fare
            st.session_state.bookings.append({
                "name": name,
                "bus_id": bus_id,
                "seats": seats,
                "total_fare": total_fare
            })
            # update seats
            st.session_state.buses[bus_id] = (route, time, fare, available - seats)
            st.success(f"Booking successful for {name}! Total Fare: Rs. {total_fare}")
        else:
            st.error("Not enough seats available!")


def cancel_booking():
    st.subheader("❌ Cancel Booking")
    if not st.session_state.bookings:
        st.info("No bookings found to cancel.")
        return

    names = [b["name"] for b in st.session_state.bookings]
    name = st.selectbox("Select name to cancel", names)

    if st.button("Cancel Booking"):
        for b in st.session_state.bookings:
            if b["name"] == name:
                bus_id = b["bus_id"]
                seats = b["seats"]
                route, time, fare, available = st.session_state.buses[bus_id]
                st.session_state.buses[bus_id] = (route, time, fare, available + seats)
                st.session_state.bookings.remove(b)
                st.success(f"Booking for {name} cancelled successfully.")
                break


def view_bookings():
    st.subheader("📋 Your Bookings")
    if not st.session_state.bookings:
        st.info("No bookings yet.")
    else:
        data = []
        for b in st.session_state.bookings:
            route, time, fare, _ = st.session_state.buses[b["bus_id"]]
            data.append({
                "Name": b["name"],
                "Route": route,
                "Time": time,
                "Seats": b["seats"],
                "Total Fare": b["total_fare"]
            })
        st.dataframe(pd.DataFrame(data))


# -----------------------------
# Streamlit Navigation
# -----------------------------
st.title("🚌 Bus Ticket Booking System")

menu = st.sidebar.radio("Navigation", ["View Buses", "Book Ticket", "Cancel Booking", "View My Bookings"])

if menu == "View Buses":
    view_buses()
elif menu == "Book Ticket":
    book_ticket()
elif menu == "Cancel Booking":
    cancel_booking()
elif menu == "View My Bookings":
    view_bookings()
