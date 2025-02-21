document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var serviceId = calendarEl.getAttribute('service-id');  // Get booking ID

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        dateClick: function(info) {
            const selectedDate = new Date(info.dateStr);
            const today = new Date();
            today.setHours(0,0,0,0);

            if (selectedDate < today) {
                console.log("Date is in the past");
            } else {
                fetchAvailableTimeSlots(info.dateStr);
            }
        },
        selectAllow: function (info) {
            return info.start >= getDateWithoutTime(new Date());
        }
    });
    
    calendar.render();
});

function getDateWithoutTime(dt) {
    dt.setHours(0, 0, 0, 0);
    return dt;
}

// Fetch available time slots when user selects a date
function fetchAvailableTimeSlots(date) {
    fetch(`/booking/api/get_available_slots/?date=${date}`)
      .then(response => response.json())
      .then(data => {
        let slotsContainer = document.getElementById("available-slots");
        slotsContainer.innerHTML = ""; // Clear previous slots
        
        if (data.times.length > 0) {
          data.times.forEach(slot => {
            let btn = document.createElement("button");
            btn.classList.add("time-slot");
            btn.innerText = slot;
            btn.onclick = () => showBookTimeSlot(date, slot);
            slotsContainer.appendChild(btn);
          });
        } else {
          slotsContainer.innerHTML = "<p>Ingen ledige tidspunkter.</p>";
        }
      });
}

function showBookTimeSlot(date, slot) {
    let slotsContainer = document.getElementById("available-slots");
    
    // Clear previous content to avoid duplicates
    slotsContainer.innerHTML = `<h3>Selected Time: ${slot}</h3>`;

    // Create a textarea for additional info
    let textField = document.createElement("textarea");
    textField.id = "additional-info";
    textField.placeholder = "Optional: Add any additional information...";
    slotsContainer.appendChild(textField);

    // Create the confirm booking button
    let confirmButton = document.createElement("button");
    confirmButton.id = "confirm-booking";
    confirmButton.innerText = "Confirm Booking";
    confirmButton.style.display = "block";
    confirmButton.onclick = () => submitBooking(date, slot, textField.value);
    
    slotsContainer.appendChild(confirmButton);
}

// Function to send the booking request
function submitBooking(date, time, additionalInfo) {
    let serviceId = document.getElementById("calendar").getAttribute("service-id"); // Get service ID

    fetch("/booking/api/create_booking/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            date: date,
            time: time,
            additional_info: additionalInfo,
            service_id: serviceId // Include service ID

        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Booking confirmed!");
            location.reload();
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Function to get CSRF token for Django POST requests
function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
}