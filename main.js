const app = {
    data() {
        return {
            message: 'Hello Vue!!',
            diana_celebrate: './assets/images/diana_celebrate.jpg',
            content: '',
            answer: null,
            isSendRequest: false,
            isGetResponse: false,
            isError: false,
            isTooLong: false,
            maxLength: 500
        }
    },
    methods: {
        async handleSubmit(e) {
            e.preventDefault()
            this.isError = false
            this.isSendRequest = true
            this.isGetResponse = false
            this.isTooLong = false

            if (this.content === '') {
                this.content = this.placeholder
            }
            if (this.content.length > this.maxLength) {
                this.isTooLong = true
                this.isGetResponse = true
                return
            }

            try {
                let response = await axios.post('https://118.25.75.14:8888/check', {
                    content: this.content
                })

                if (response.status == 200) {
                    this.answer = response.data
                    this.isGetResponse = true
                    console.log(this.answer)
                } else {
                    this.isError = true
                }
            }
            catch (err) {
                this.isError = true
            }
        }
    },
    computed: {
        title() {
            return this.brand + ' ' + this.message
        },
        isDisable() {
            return this.isSendRequest && !this.isGetResponse && !this.isError
        },
        avgRate() {
            if (this.answer === null) {
                return 0;
            }
            const total = this.answer.reduce(function (sum, object) {
                return sum + parseFloat(object.rate);
            }, 0);
            console.log(total)
            return (total / this.answer.length).toFixed(3);

        },
        placeholder() {
            return `这个冬天真冷，窗外的大雪飞扬，像是要吹灭街上的光。但是看着嘉然跳跳唱唱，处刑大家的小作文，再被写给晚晚的小作文处刑，我觉得有股热流在身体里流淌，紧绷的立毛肌都舒展开来了。

当初在嘉然出现时，有人警告说雪崩时没有一片雪花是无辜的。但我现在想如果是落到嘉然的怀里，再冷的雪也会融化的吧。

可是我没有落到她的怀里，而是落到她的手心了。

我对然然的表演傻笑，旁边脸被冻得发红的妹妹问我，还有哪个冬天比这个更冷吗？

我突然很害怕。我知道，没有嘉然的冬天才是最冷的。

更让人难过的是我没有妹妹，但这个冬天迟早会来。`
        }
    }
}

Vue.createApp(app).mount('#app')
