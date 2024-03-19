const syscallreturn = new Vue({
    el: '#syscallreturn',
    delimiters: ['[[', ']]'],
    data: {
        syscalls: []
    },
    mounted() {
        fetch('/api/phoenix')
            .then(response => response.json())
            .then(data => {
                this.syscalls = data.syscalls;
            })
            .catch(error => console.error('Error fetching syscalls:', error));
    }

});


const actiondropddown = new Vue({
    el: '#actiondrpdown',
    data: {
        selectedAction: '', // The selected action
        actions: ['BLOCK', 'STEP', 'WARN'] // List of actions
    },
    methods: {
        getColor(action) {
            // Define your logic to determine the color based on the action value
            if (action === 'BLOCK') {
                return 'red'; // For example, set the color to red for 'BLOCK' action
            } else if (action === 'STEP') {
                return 'blue'; // For 'STEP', set the color to blue
            } else if (action === 'WARN') {
                return 'orange'; // For 'WARN', set the color to orange
            }
            // Return default color if none of the conditions match
            return 'black';
        }
    },
    mounted() {
        console.log(this.actions); // Check if actions are populated
    }
});

//submit buttom saves to the database

const savebutton = new Vue({
    el: '#savebutton',
    delimiters: ['[[', ']]'],
    data: {
        action: "block",
        syscall: "execve",
        date: '2024-03-15'
    },
    methods: {
        saveData() {
            const data = {
                action: this.action,
                syscall: this.syscall,
                date: this.date
            };
            console.log('Data to be sent:', data);

            fetch('/api/save_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => {
                    console.log('Response status:', response.status);
                    return response.json();
                })
                .then(data => {
                    console.log('Response data:', data);
                })
                .catch(error => console.error('Error saving data:', error));
        }
    }
});



//the fucntion to upload the json file to the database 
const app = new Vue({
    el: '.navbar-brand-31',
    data: {
        selectedFileName: ''
    },
    methods: {
        handleFileUpload(event) {
            const file = event.target.files[0];
            this.selectedFileName = file.name; // Store the filename

            print(this.selectedFileName)

            const reader = new FileReader();
            reader.onload = (e) => {
                const json = JSON.parse(e.target.result);
                this.uploadData(json);
            };
            reader.readAsText(file);


        },
        uploadData(data) {
            fetch('/api/upload_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)

            })
                .then(response => response.json())
                .then(data => {
                    alert('Data uploaded successfully!');
                    console.log('Data uploaded:', data);


                })
                .catch(error => {
                    console.error('Error uploading data:', error);
                });
        }
    }
});













//orginal function not working 
/*
document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/phoenix')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch syscalls. Status: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (!data.syscalls || !Array.isArray(data.syscalls)) {
                throw new Error('Invalid data format: syscalls array is missing or not an array');
            }
            const syscalls = data.syscalls;

            // Update each syscall element by its unique ID
            syscalls.forEach((syscall, index) => {
                const element = document.getElementById('syscall' + (index + 1));
                if (element) {
                    element.textContent = syscall;
                }
            });
        })
        .catch(error => console.error('Error fetching syscalls:', error.message));
});
*/





//displays data for the text box on the page
/*
window.addEventListener('load', function() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_data", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            displayData(data);
        }
    };

    xhr.send();
});

// Function to display data on the form
function displayData(data) {
    var systemCallDiv = document.getElementById("systemCallData");
    var actionDiv = document.getElementById("actionData");

    // Clear previous data
    systemCallDiv.innerHTML = "";
    actionDiv.innerHTML = "";

    // Populate data on the form
    data.forEach(function(entry) {
        systemCallDiv.innerHTML += '<div class="frame-80"><div class="warning-file-location">' + entry.syscall + '</div></div>';
        actionDiv.innerHTML += '<div class="frame-81"><div class="warning-file-location">' + entry.action + '</div></div>';
    });
}*/


/*!
document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_syscalls')
        .then(response => response.json())
        .then(data => {
            const syscalls = data.syscalls;

            // Update each syscall element by its unique ID
            syscalls.forEach((syscall, index) => {
                const element = document.getElementById('syscall' + (index + 1));
                if (element) {
                    element.textContent = syscall;
                }
            });
        })
        .catch(error => console.error('Error fetching syscalls:', error));
});
 */



