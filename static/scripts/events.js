// Skeleton of code from https://www.codingnepalweb.com/dynamic-calendar-html-css-javascript/

const daysTag = document.querySelector(".days"),
currentDate = document.querySelector(".current-date"),
prevNextIcon = document.querySelectorAll(".icons span");
const eventsTag = document.querySelector(".events"),
eventInfoTag = document.querySelector(".event_info");

// getting new date, current year and month
let date = new Date(),
currYear = passedYear,
currMonth = passedMonth - 1,
selectedYear = currYear,
selectedMonth = currMonth,
selectedDate = passedDate,
selectedPeriod = passedPeriod;
let firstLoad = true;

let events = [];
let usertype = "unauthenticated";

// storing full name of all months in array
const months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];

const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(), // getting first day of month
    lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // getting last date of month
    lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // getting last day of month
    lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // getting last date of previous month
    let liTag = "";

    for (let i = firstDayofMonth; i > 0; i--) { // creating li of previous month last days
        let tempMonth = currMonth - 1,
        tempYear = currYear;

        if (tempMonth < 0) {
            tempYear -= 1;
            tempMonth = 11;
        }

        if ((lastDateofLastMonth - i + 1) === selectedDate && selectedMonth === tempMonth && selectedYear === tempYear) {
            liTag += `<li id="${lastDateofLastMonth - i + 1}" class="active" onclick="daySelected('active', '${lastDateofLastMonth - i + 1}')">${lastDateofLastMonth - i + 1}</li>`;
        }
        else
            liTag += `<li id="${lastDateofLastMonth - i + 1}" class="inactive" onclick="daySelected('inactive', '${lastDateofLastMonth - i + 1}')">${lastDateofLastMonth - i + 1}</li>`;
    }

    for (let i = 1; i <= lastDateofMonth; i++) { // creating li of all days of current month
        // adding active class to li if the current day, month, and year matched
        let isToday = "";
        let today = false;
        let selected = false;

        if (i === new Date().getDate() && currMonth === new Date().getMonth() 
            && currYear === new Date().getFullYear()) {
            today = true;
        }
        if (i === selectedDate && currMonth === selectedMonth && currYear === selectedYear) {
            selected = true;
        }

        if (today && selected)
            isToday = "active";
        else if (today && !selected)
            isToday = "current";
        else if (!today && selected)
            isToday = "active"

        // Embedded onclick function wizardry :D
        liTag += `<li id="${i}" class="${isToday}" onclick="daySelected('${isToday}', '${i}')">${i}</li>`;
    }

    for (let i = lastDayofMonth; i < 6; i++) { // creating li of next month first days
        let tempMonth = currMonth + 1,
        tempYear = currYear;

        if (tempMonth > 11) {
            tempYear += 1;
            tempMonth = 0;
        }

        if ((i - lastDayofMonth + 1) === selectedDate && selectedMonth === tempMonth && selectedYear === tempYear)
            liTag += `<li id="${i - lastDayofMonth + 1}" class="active" onclick="daySelected('active', '${i - lastDayofMonth + 1}')">${i - lastDayofMonth + 1}</li>`;
        else
            liTag += `<li id="${i - lastDayofMonth + 1}" class="inactive" onclick="daySelected('inactive', '${i - lastDayofMonth + 1}')">${i - lastDayofMonth + 1}</li>`;
    }
    currentDate.innerText = `${months[currMonth]} ${currYear}`; // passing current mon and yr as currentDate text
    daysTag.innerHTML = liTag;
}
// renderCalendar();

const renderEvents = () => {
    let liTagE = "";
    for (let i = 0; i < events.length; i++) {
        var available_class = "";
        var event_title = "";
        if ("approved" in events[i] && events[i]["approved"] == true) {
            available_class = "taken";
            event_title = events[i]["title"]
        }
        else {
            available_class = "open";
            event_title = events[i]["time"] + " Available";
        }

        var prd = events[i]["_id"];
        prd = prd[prd.length - 1];
        if (prd == selectedPeriod)
                available_class += " selected"
        

        liTagE += `<li class="events_button ${available_class}" onclick="eventSelected('${prd}')">${event_title}</li>`;
    }
    eventsTag.innerHTML = liTagE;
}

const renderEventInfo = (period) => {
    let EvTag = "";
    var i = period-1;
    if ("approved" in events[i] && events[i]["approved"] == true) {
        EvTag += `
        <h2>${events[i]["title"]}</h2>
        <h2>Image w/ border here :)</h2>
        <!-- https://stackoverflow.com/questions/14096292/how-to-have-two-headings-on-the-same-line-in-html -->
        <div style="clear: both;">
            <h4 style="float: left;">${events[i]["time"]}</h4>
            <h4 style="float: right;">Contact for Info: ${events[i]["contact"]}</h4>
        </div>
        <br>
        <h5 style="float: left">${events[i]["desc"]}</h5>
        `;
    }
    eventInfoTag.innerHTML = EvTag;
}

sessionStorage.setItem("usertype", "admin");

function eventSelected(period) {
    window.location.replace(`/events/e=?year=${selectedYear}&month=${selectedMonth + 1}&day=${selectedDate}&period=${parseInt(period)}`);
}

prevNextIcon.forEach(icon => { // getting prev and next icons
    icon.addEventListener("click", () => { // adding click event on both icons
        // if clicked icon is previous icon then decrement current month by 1 else increment it by 1
        if (icon.id === "prev")
            currMonth -= 1;
        else
            currMonth += 1;

        if(currMonth < 0 || currMonth > 11) { // if current month is less than 0 or greater than 11
            // creating a new date of current year & month and pass it as date value
            date = new Date(currYear, currMonth, new Date().getDate());
            currYear = date.getFullYear(); // updating current year with new date year
            currMonth = date.getMonth(); // updating current month with new date month
        } else {
            date = new Date(); // pass the current date as date value
        }
        renderCalendar(); // calling renderCalendar function
    });
});

// Modifies selected day
function selectEvent(year, month, date, period) {
    selectedYear = year;
    selectedMonth = month;
    selectedDate = date;
    selectedPeriod = period;

    // getEvents(selectedDate)
}

function getEvents(day_id) {
    // Render calender before fetch
    renderCalendar();
    // Send selected day to url, then receive events for that day
    fetch('/get-event-by-day', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
                 'year': selectedYear, 'month': selectedMonth + 1, 'day': day_id
             })
    })
    .then(res => {return res.json();})
    .then(data => {
        events = data;
        //console.log(events);
        renderEvents();
        renderEventInfo(selectedPeriod);
    })
    .catch(error => console.log(error))
}
getEvents(selectedDate);

function daySelected(day_class, day_id) {
    if (day_class == "inactive")
    {
        if (Number(day_id) < 15)
        {
            selectedMonth += currMonth - selectedMonth + 1;
            selectedYear += currYear - selectedYear;
        }
        else
        {
            selectedMonth += currMonth - selectedMonth - 1;
            selectedYear += currYear - selectedYear;
        }
    }
    else
    {
        // if (currMonth == selectedMonth + 1)
        //     selectedMonth += 1
        // else if (currMonth == selectedMonth - 1)
        //     selectedMonth -=1
        selectedMonth += currMonth - selectedMonth;
        selectedYear += currYear - selectedYear;
    }

    if (selectedMonth < 0) {
        selectedYear -= 1;
        selectedMonth = 11;
    }
    else if (selectedMonth > 11) {
        selectedYear += 1;
        selectedMonth = 0;
    }

    // Modifies selected day
    selectedDate = parseInt(day_id)

    // Passes selected day into new URL
    window.location.replace(`/events/e=?year=${selectedYear}&month=${selectedMonth + 1}&day=${selectedDate}&period=${1}`);

    
}