const app = {
    data() {
        return {
            message: 'Hello Vue!!',
            diana_celebrate: './assets/images/diana_celebrate.jpg',
            answer: '',
            content: ''
        }
    },
    methods: {
        addToCart() {
            this.cart += 1
        },
        async handleSubmit(e) {
            e.preventDefault()

            if (this.content === '') {
                this.content = this.placeholder
            }

            var params = new Object();
            params.content = this.content
            console.log(params)
            var httpRequest = new XMLHttpRequest();
            httpRequest.open('POST', 'http://127.0.0.1:8000/check', true);
            httpRequest.send(JSON.stringify({
                content: this.content
            }));

            httpRequest.onreadystatechange = function () {
                if (httpRequest.readyState == 4 && httpRequest.status == 200) {
                    var json = httpRequest.responseText;
                    console.log(json);
                }
            };

            console.log(this.answer)
        }
    },
    computed: {
        title() {
            return this.brand + ' ' + this.message
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