const module2 = new Vue({
    delimiters: ['[[', ']]'],
    el: '#module1',
    data () {
        return {
            module1_status: '',
            alerts: [],
        };
    },
    mounted() {
        // Make an initial API call when the component is mounted
        this.fetchData();

        // Set up interval to make API calls every second
        setInterval(() => {
            this.fetchData();
        }, 1000);
    },
    methods: {
        fetchData() {
            // Make AJAX request to backend API
            fetch('/api/module1')
                .then((response) => {
                    response.json().then((data) => {
                        this.module1_status = data.counter;
                        this.alerts = data.alerts;
                });
            })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
    }
});