const urlRegex = "/[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/ig"

const app = Vue.createApp({
    delimiters: ['${', '}'],
    data() {
        return {
            loading: false,
            youtubeURL: '',
            completed: false,
            status: ''
        }
    },
    methods: {
        fetchCaption() {
            this.loading = true
            const textBody = document.getElementById('text')

            fetch("http://localhost:5000/get_video_text/", {
                method: 'POST',
                headers: {
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify({ text: this.youtubeURL })
            })
            .then(response => {
                response.json()
                    .then(resp => {
                        if (resp.status == 'error') {
                            throw Error("error occured")
                        } else {
                            this.status = "Subtitles found!"
                            this.completed = true
                        }
                    })
                    .catch(err => {
                        this.error = true
                        this.status = "Error occurred or subtitles not found."
                        console.log(err)
                    })
            })
            .catch(err => {
                this.error = true
                this.status = "Error occurred or subtitles not found."
                console.log(err)
            })
            .finally(() => {
                this.loading = false;
            })
        }
    }
})