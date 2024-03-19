const test = new Vue({
    el: '#test',
    delimiters: ['[[', ']]'],
    data: {
        vueGreeting: 'Hello, Vue!'
    }
})


const alertTable = new Vue({
    el: '#alertTable',
    delimiters: ['[[', ']]'],
    data() {
        return {
            alerts: [
                { name: 'Alert 1', type: 'Type A', severity: 'High' },
                { name: 'Alert 2', type: 'Type B', severity: 'Medium' },
                { name: 'Alert 3', type: 'Type A', severity: 'Low' }
            ],
            selectedAlerts: []
        };
    },
    methods: {
        submitForm() {
            if (this.selectedAlerts.length > 0) {
                // You can perform further actions here, such as sending the data to the backend API using fetch or XMLHttpRequest
                console.log('Selected alerts:', this.selectedAlerts);
                // For example:
                fetch('/api/alerts', {
                    method: 'POST',
                    body: JSON.stringify({ selectedAlerts: this.selectedAlerts }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .catch(error => {
                    console.error('Error submitting form:', error);
                });
            } else {
                alert('Please select at least one alert.');
            }
        }
    }
});