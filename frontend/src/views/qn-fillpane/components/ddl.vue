<template>
    <div class="container">
        <div class="times" v-if="!isEnd">
            距离考试结束还有<br>
            <span class="num">{{ hour }}</span>时
            <span class="num">{{ minute }}</span>分
            <span class="num">{{ second }}</span>秒
        </div>
        <div class="end" v-else>
            考试已结束
        </div>
    </div>
</template>

<script>
export default {
    name: 'DeadTime',
    props: {
        endTime: Date // 修改 props 的类型为 Date
    },
    data() {
        return {
            currentTime: new Date(),
            ms: 1,
            hour: 1,
            minute: 1,
            second: 1,
            isEnd: false,
        };
    },
    methods: {
        change() {
            this.currentTime = new Date();
            this.ms = this.endTime - this.currentTime;
            if (this.ms <= 0) this.isEnd = true;
            this.hour = Math.floor(this.ms / 1000 / 60 / 60);
            this.minute = Math.floor((this.ms - this.hour * 1000 * 60 * 60) / 1000 / 60);
            this.second = Math.floor((this.ms - this.hour * 1000 * 60 * 60 - this.minute * 1000 * 60) / 1000);
        }
    },
    mounted() {
        let _this = this;
        this.timer = setInterval(() => {
            _this.change();
        }, 500)
    },
    beforeUnmount() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    }
}
</script>

<style scoped>
@media screen and (min-width: 600px) {
    .times {
        color: #ffffff;
        font-size: 16px;
        text-align: center;
    }

    .times .num {
        color: #ffffff;
        font-size: 20px;
        font-weight: bold;
        margin-right: 5px;
    }

    .container {
        position: fixed;
        right: 3%;
        top: 10px;
        margin: auto;
        background-color: #ec5e66;
        border-radius: 0 0 15px 15px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-right: 15px;
        padding-left: 15px;
    }

    .end {
        color: #ffffff;
        font-size: 20px;
        text-align: center;
    }
}

@media screen and (max-width: 600px) {/*手机端显示*/ 
    .times {
        color: #ffffff;
        font-size: 16px;
        text-align: center;
    }

    .times .num {
        color: #ffffff;
        font-size: 20px;
        font-weight: bold;
        margin-right: 5px;
    }

    .container {
        position: fixed;
        right: 3%;
        top: 10px;
        margin: auto;
        background-color: #ec5e66;
        border-radius: 0 0 15px 15px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-right: 15px;
        padding-left: 15px;
        z-index: 9999;
    }

    .end {
        color: #ffffff;
        font-size: 20px;
        text-align: center;
    }
}
</style>
