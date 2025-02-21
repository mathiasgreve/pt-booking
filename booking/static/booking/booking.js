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
    let textField = document.createElement("textarea");
    slotsContainer.appendChild(textField);
}
