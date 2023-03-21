const stpw = document.getElementById("stopwatch");
const result = document.getElementById("result");

let state = {
    interval: null,
    time: 0,
};

let clock = {
    sec: 0,
    min: 0,
    h: 0,
};

function stopwatch() {
    if (stpw.classList.contains("inactive")) {
        stpw.classList.replace("inactive", "active");
        state.interval = setInterval((time) => {
            state.time += 1;
            clock.sec = Math.floor((state.time) % 60);
            clock.min = Math.floor((state.time / (60)) % 60);
            clock.h = Math.floor((state.time / (60 * 60)) % 60);
            stpw.textContent = digit(clock.h) + ":" + digit(clock.min) + ":" + digit(clock.sec);
            stpw.textContent = digit(clock.h) + ":" + digit(clock.min) + ":" + digit(clock.sec);
        }, 1000);
        return;
    }
    clearInterval(state.interval);
    stpw.classList.replace("active", "inactive");
}

function charge_time(btn_id) {
    clearInterval(state.interval);
    let data = {
        'task_id': btn_id,
        'time': state.time,
    }
    $.ajax({
        url: '/timer',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (response) {
            console.log(response);
        }
    });
    state.time = 0;
    stpw.classList.replace("active", "inactive");
    stopwatch();
}

// Present time as two-digits
function digit(amnt) {
    return (('0') + amnt).length > 2 ? amnt : '0' + amnt;
}


function changeTheme() {
    const body = document.body;
    const main = document.getElementById('main')
    const table = document.getElementById('table')

    // Check if the user has a theme preference in localStorage
    const theme = localStorage.getItem('theme');
    if (theme) {
        body.classList.add(theme);
        main.classList.add('main-dark');
        table.classList.add('t-dark');
    }

    // Toggle the theme and update localStorage
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        main.classList.remove('main-dark');
        table.classList.remove('t-dark');
        localStorage.removeItem('theme');
    } else {
        body.classList.add('dark-mode');
        main.classList.add('main-dark');
        table.classList.add('t-dark');
        localStorage.setItem('theme', 'dark-mode');
    }
}

// On page load, apply the theme preference/manage stopwatch if it exists in localStorage
document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const theme = localStorage.getItem('theme');
    const storedState = JSON.parse(localStorage.getItem('stopwatchState'));
    if (storedState) {
        state.time = storedState.time;
        stopwatch();
    }
    if (theme) {
        body.classList.add(theme);
        main.classList.add('main-dark');
        table.classList.add('t-dark');
    }
});

// On page unload, store the stopwatch state in localStorage
window.addEventListener('beforeunload', function () {
    localStorage.setItem('stopwatchState', JSON.stringify(state));
});
