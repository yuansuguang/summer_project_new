<template>
  <div class="qn-fill">
    <div class="back-bt" v-if="mode === '0' || mode === 0">
      <el-button type="danger" @click="quit">
        <arrow-left />退出预览
      </el-button>
    </div>
    <div class="paper">
      <div v-if="success" style="padding-bottom: 50px">
        <div class="tyn-icon">
          <img src="../../../src/assets/images/Edit.png" alt="">
        </div>
        <h2 class="tyn-text" v-if="success" >提交成功，感谢您的参与！</h2>
        <el-button class="mb" type="primary" size="middle" @click="backToSurvey">继续查看问卷信息</el-button>
      </div>
      <div v-else-if="close" style="padding-bottom: 50px">
        <div class="tyn-icon">
          <img src="../../../src/assets/images/Edit.png" a klt="">
        </div>
        <h1 v-if="close">问卷已结束，感谢您的参与！</h1>
        <el-button type="primary" size="middle" @click="gotoHome">返回</el-button>
      </div>
      <div class="body" v-else>

        <div class="title">
          {{ title }}
        </div>

        <div class="description" v-if="description !== ''">
          &emsp;&emsp;{{ description }}
        </div>

        <div class="description" v-if="limit > 0">
          &emsp;&emsp;该问卷剩余限额：{{ limit }}
        </div>

        <el-divider></el-divider>
        <div class="main">
          <div class="ques-block" v-for="item in questions" :key="item.id">
            <!-- <div v-if="item.is_shown&&ahead(item.last_question)"> -->
            <div class="q-title">
              {{ item.id }}. {{ item.title }} <span class="must" v-if="item.must">(必填)</span>
            </div>

            <div class="q-description"
              v-if="item.description !== '' && item.description !== null && item.description !== undefined">
              {{ item.description }}
            </div>

            <!--                  图片-->
            <el-row class="block-img" v-for="(i, index) in item.imgList" :key="i.index">
              <el-col :offset="4" :span="8" class="demo-image__preview" v-if="index % 2 === 0">
                <el-image class="img" :src="i.url" :preview-src-list="[i.url]">
                </el-image>
              </el-col>
              <el-col :span="8" class="demo-image__preview" v-if="index % 2 === 0 && index + 1 <= item.imgList.length - 1">
                <el-image class="img" :src="item.imgList[index + 1].url" :preview-src-list="[item.imgList[index + 1].url]">
                </el-image>
              </el-col>
            </el-row>
            <span style="color: #9b9ea0;font-size: x-small;margin: 5px" v-if="item.imgList.length !== 0">（点击图片查看大图）</span>


            <!--                视频-->
            <!-- <el-row class="block-img" v-for="i in item.videoList" :key="i.index">
                  <embed width=400 height=230 transparentatstart=true
                         animationatstart=false autostart=true autosize=false volume=100
                         displaysize=0 showdisplay=true showstatusbar=true showcontrols=true
                         showaudiocontrols=true showtracker=true showpositioncontrols=true
                         balance=true :src="i.url">
                </el-row> -->


            <!--                  单选-->
            <div v-if="item.type === 'radio'">
              <div class="q-opt" v-for="opt in item.options" :key="opt.id">
                <el-radio v-model="answers[item.id - 1].ans" :label="opt.title">
                  {{ opt.title }}
                </el-radio>
              </div>
            </div>

            <!--                  多选-->
            <el-checkbox-group class="q-opt" v-if="item.type === 'checkbox'" v-model="answers[item.id - 1].ansList">
              <el-checkbox v-for="opt in item.options" :key="opt.id" :label="opt.title">
                {{ opt.title }}
              </el-checkbox>
            </el-checkbox-group>

            <!--                  填空-->
            <div class="q-opt" v-if="item.type === 'text'">
              <el-input v-if="item.row > 1" type="textarea" :autosize="{ minRows: 2, maxRows: item.row }"
                placeholder="请输入内容" v-model="answers[0].ans">
              </el-input>
              <el-input v-if="item.row === 1" placeholder="请输入内容" v-model="answers[0].ans">
              </el-input>
            </div>

            <!--                  评分-->
            <div class="q-opt" v-if="item.type === 'mark'">
              <el-rate v-model="answers[item.id - 1].ans" :max="item.score"></el-rate>
            </div>
          </div>
        </div>

        <div class="submit-bt">
          <el-button type="primary" @click="saveans" size="default">暂存并退出</el-button>
          <el-button type="primary" @click="submit" size="default">提交</el-button>
        </div>

      </div>
      <div class="tail">
        <a :href="rootUrl">问卷星球</a>&ensp;提供技术支持
      </div>
    </div>
  </div>
</template>

<script>
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElButton, ElRadio, ElCheckbox, ElInput, ElRate, ElRow, ElCol } from 'element-plus';
// import 'element-plus/lib/theme-chalk/index.css'; // 全局引入样式
import getDataApi from "@/utils/getDataApi";
import saveAnsApi from "@/utils/saveDataApi";
export default {
  name: "FillQn",
  mixins: [getDataApi, saveAnsApi],
  components: {
    ElButton, ElRadio, ElCheckbox, ElInput, ElRate, ElRow, ElCol,
    ArrowLeft // 引用图标
  },
  data() {
    return {
      rootUrl: 'http://localhost:8080/',

      success: false,
      close: false,

      mode: this.$route.query.mode,
      title: '',
      description: '',
      limit: 0,
      // type: '',
      answers: [
        {
            "question_id": 66,
            "type": "radio",
            "ans": "",
            "ansList": [],
            "answer": ""
        },
        {
            question_id: 67,
            type: "checkbox",
            ans: "",
            ansList: [],
            answer: ""
        },
        {
            question_id: 68,
            type: "radio",
            ans: "",
            ansList: [],
            answer: ""
        },
        {
            question_id: 69,
            type: "radio",
            ans: "",
            ansList: [],
            answer: ""
        },
        {
            question_id: 70,
            type: "mark",
            ans: 9,
            ansList: [],
            answer: "9"
        },
      ],
      questions: [
        // {
        //     last_question: 0,
        //     last_option: 0,
        //     is_shown: true,
        //     question_id: 222,
        //     row: 1,
        //     score: 10,
        //     title: "小学期开发的内容是？",
        //     description: "看看你们是不是还没看需求",
        //     must: true,
        //     type: "radio",
        //     qn_id: 97,
        //     refer: "问卷星球",
        //     point: 20,
        //     id: 1,
        //     options: [
        //         {
        //             id: 1,
        //             title: "问卷星球"
        //         },
        //         {
        //             id: 2,
        //             title: "出版系统"
        //         }
        //     ],
        //     answer: "",
        //     imgList: [{
        //       name: '1.jpg',
        //       url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg'
        //     },{
        //       name: '2.jpg',
        //       url: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
        //     }],
        //     videoList: [
        //     ]
        // },
        // {
        //     last_question: 1,
        //     last_option: 1,
        //     is_shown: true,
        //     question_id: 223,
        //     row: 1,
        //     score: 10,
        //     title: "本次小学期的助教有？",
        //     description: "不会吧不会吧，不会有人真以为助教只是助教吧？",
        //     must: true,
        //     type: "checkbox",
        //     refer: "ZXH-<^-^>-HZY", 
        //     point: 30,
        //     id: 2,
        //     options: [
        //         {
        //             id: 1,
        //             title: "ZXH"
        //         },
        //         {
        //             id: 2,
        //             title: "ZYH"
        //         },
        //         {
        //             id: 3,
        //             title: "HZY"
        //         },
        //         {
        //             id: 4,
        //             title: "ZHT"
        //         },
        //         {
        //             id: 5,
        //             title: "LKW"
        //         }
        //     ],
        //     answer: "",
        //     imgList: [],
        //     videoList: []
        // },
        // {
        //     last_question: 2,
        //     last_option: 1,
        //     is_shown: true,
        //     question_id: 224,
        //     row: 1,
        //     score: 10,
        //     title: "杀戮尖塔最强的角色是",
        //     description: "没开偏差认知",
        //     must: true,
        //     type: "radio",
        //     // qn_id: 99,
        //     refer: "问卷星球",
        //     point: 20,
        //     id: 3,
        //     options: [
        //         {
        //             id: 1,
        //             title: "鸡煲"
        //         },
        //         {
        //             id: 2,
        //             title: "观者"
        //         }
        //     ],
        //     answer: "",
        //     imgList: [],
        //     videoList: []
        // },
      ]

    }
  },
  methods: {
    ahead(qid) {
      if (qid === 0) return true;
      for (let i = 0; i < this.questions.length; i++) {
        if (this.questions[i].id === qid) {
          if (this.questions[i].is_shown === true) return this.ahead(this.questions[i].last_question);
          else return false;
        }
      }
      return false;
    },
    changeHandler(id, value) {
      console.log(id + '改变之后的值是:' + value);
      let pid = 0;
      for (let j = 0; j < this.questions[id - 1].options.length; j++) {
        if (value === this.questions[id - 1].options[j].title) pid = this.questions[id - 1].options[j].id;
      }
      for (let i = id; i < this.questions.length; i++) {
        if (this.questions[i].last_question === id && this.questions[i].last_option === pid) {
          console.log(this.questions[i]);
          console.log(this.questions[i].last_option);
          this.questions[i].is_shown = true;
        }
        else if (this.questions[i].last_question === id) {
          this.questions[i].is_shown = false;
        }
      }
    },
    changeHandler2(id, value) {
      console.log(id + '改变之后的值是:' + value);
      let pid = [];
      let a = 0;
      let find = false;
      for (let j = 0; j < this.questions[id - 1].options.length; j++) {
        for (let k = 0; k < value.length; k++) {
          if (value[k] === this.questions[id - 1].options[j].title) {
            pid[a++] = this.questions[id - 1].options[j].id;
            break;
          }
        }
      }
      for (let i = id; i < this.questions.length; i++) {
        if (this.questions[i].last_question === id) {
          for (let k = 0; k < pid.length; k++) {
            if (this.questions[i].last_option === pid[k]) {
              this.questions[i].is_shown = true;
              find = true;
              break;
            }
          }
          if (!find) this.questions[i].is_shown = false;
        }
      }
    },
    gotoHome() {
      this.$router.push('/');
    },
    backToSurvey() {
      this.success = false;
      this.repeat = false;
      this.close = false;
      location.reload();
    },
    submit: function () {
      this.submitAns('1');
    },
    saveans: function () {
      this.saveQnInfo('save', '1')
    },
    quit: function () {
      this.$confirm('请选择返回问卷编辑页面或问卷中心？', '确认信息', {
        distinguishCancelAndClose: true,
        confirmButtonText: '编辑页面',
        cancelButtonText: '问卷中心'
      })
        .then(() => {
          location.href = this.GLOBAL.baseUrl + "/edit?pid=" + this.$route.query.pid;
        })
        .catch(action => {
          if (action === 'cancel') {
            this.$router.push('/index');
          }
        });

    },
    fetchQuestions() {
      // 假设从后端获取问题数据的过程
      const formData = new FormData();
      // formData.append("survey_keyword", this.loginForm.user);
      formData.append("code", this.$route.params.code);
      this.$axios({
        method: 'post',
        url: '/question/api/listquestionalt',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            this.title = res.data.title;
            this.description = res.data.description;
            this.questions = JSON.parse(res.data.data);
            if (res.data.survey_type == '4') {
              this.limit = res.data.resume;
            }
            console.log(res.data.has_answers);
            if (res.data.has_answers) {
              console.log("enter 1");
              console.log(res.data.answers);
              this.answers = JSON.parse(res.data.answers);
              console.log("all ans:", this.answers);
              console.log("ans length:", this.answers.length);
              console.log("ans1:", this.answers[0]);
              console.log("answer[0].ans:", this.answers[0].ans);
            }
            else {
              console.log("enter 2");
              this.answers = this.questions.map(question => ({
                id: question.id,
                type: question.type,
                ans: '',
                ansList: []
              }));
            }
            // for (var i = 0; i < this.questionnaires.length; i++) {
            // if (this.questionnaires[i].questionType == '1')
            //     this.questionnaires[i].questionType = '普通问卷'
            // else if (this.questionnaires[i].questionType == '2')
            //     this.questionnaires[i].questionType = '投票问卷'
            // else if (this.questionnaires[i].questionType == '3')
            //     this.questionnaires[i].questionType = '考试问卷'
            // else
            //     this.questionnaires[i].questionType = '报名问卷'
            // }
            console.log(this.title);
            console.log(this.description);
            console.log(this.questions);
            console.log("answers init:");
            console.log(this.answers);
            console.log("success on fetching questions");
            break;
          case 2:
            console.log("error 2");
            break;
          case 3:
            console.log("error 3");
            break;
          case 4:
            console.log("error 4");
            break;
          case 5:
            console.log("error 5");
            break;
          case -1:
            break;
        }
      }).catch(err => {
        console.log(err);
      });
    },
  },
  created() {
    // if (this.mode === '0') {
    //   this.getQnDataForPreview();
    // }
    // else if (this.mode === '1') {
    //   this.getQnDataForFill(false,false);
    // }
    this.fetchQuestions();
    console.log("answers:", this.answers);
  },
}
</script>

<style>
@media screen and (min-width: 600px) {
  .tyn-icon {
    margin: 50px;
    padding-top: 100px;
  }
  .qn-fill {
    /* background-image: url("../../../src/assets/images/Edit.png"); */
    background-repeat: repeat-y;
    min-height: 800px;
    overflow: hidden;
    background-position: center;
    background-size: 100% auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .qn-fill .back-bt {
    position: fixed;
    right: 90px;
    top: 0;
    margin: auto;
  }

  .qn-fill .back-bt .el-button {
    border-radius: 0 0 15px 15px;
  }

  .qn-fill .paper {
    margin: 120px auto 0;
    width: 900px;
    background-color: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }

  .qn-fill .body {
    margin-left: 80px;
    margin-right: 80px;
  }

  .qn-fill .body .title {
    font-size: 28px;
    font-weight: bold;
    padding-bottom: 40px;
    padding-top: 45px;
  }

  .qn-fill .body .description {
    text-align: left;
    font-size: 16px;
    color: black;
    line-height: 30px;
    padding-bottom: 20px;
  }

  .img {
    width: 200px;
    height: 200px;
  }

  .qn-fill .body .el-divider--horizontal {
    margin: 0;
  }

  .qn-fill .body .q-title {
    text-align: left;
    /*border: solid 1px black;*/
    font-size: 16px;
    padding: 40px 10px 10px;
    font-weight: bold;
  }

  .qn-fill .body .q-description {
    text-align: left;
    font-size: 14px;
    padding-left: 10px;
    padding-top: 5px;
    padding-bottom: 10px;
    color: #969696;
  }

  .qn-fill .body .must {
    font-weight: normal;
    color: crimson;
  }

  .qn-fill .body .q-opt {
    text-align: left;
    /*border: solid 1px black;*/
    font-size: 16px;
    padding: 10px 10px 10px;
  }

  .qn-fill .body .el-checkbox {
    padding: 10px 0;
    display: block;
  }

  .qn-fill .body .q-opt .el-textarea__inner {
    max-height: 100px;
  }

  .qn-fill .body .submit-bt {
    padding-top: 30px;
    padding-bottom: 50px;
  }

  .qn-fill .tail {
    padding-top: 25px;
    font-size: 15px;
    color: #b9b9b9;
    border-top: solid 1px #e3e3e3;
    height: 50px;
    margin: 0 30px 130px;
  }
}

@media screen and (max-width: 600px) {
  .tyn-icon {
    margin: 50px;
    padding-top: 50px;
    margin-left: 32%;
  }
  .tyn-text{
    margin-left: 55px;
  }
  .mb {
    margin-left: 120px;
  }
  .qn-fill {
    /* background-image: url("../../../src/assets/images/Edit.png"); */
    /* background-repeat: repeat-y;
    min-height: 800px;
    overflow: hidden; */
    background-position: center;
    background-size: 100% auto;
  }

  .qn-fill .back-bt {
    /* position: fixed;
    right: 90px;
    top: 0;
    margin: auto; */
  }

  .qn-fill .back-bt .el-button {
    /* border-radius: 0 0 15px 15px; */
  }

  .qn-fill .paper {
    /* margin: 120px auto 0; */
    width: 100%;
    background-color: #FFFFFF;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
  }

  .img {
    width: 100px;
    height: 100px;
  }

  .qn-fill .body {
    margin-left: 20px;
    margin-right: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .qn-fill .body .title {
    font-size: 28px;
    font-weight: bold;
    padding-bottom: 10px;
    padding-top: 25px;
  }

  .qn-fill .body .description {
    /* text-align: left; */
    font-size: 16px;
    color: black;
    /* line-height: 30px; */
    align-self: self-start;
    padding-bottom: 5px;
  }

  .qn-fill .body .el-divider--horizontal {
    margin: 0;
  }

  .qn-fill .body .q-title {
    text-align: left;
    /*border: solid 1px black;*/
    font-size: 16px;
    padding: 40px 10px 10px;
    font-weight: bold;
  }

  .qn-fill .body .q-description {
    text-align: left;
    font-size: 14px;
    padding-left: 10px;
    padding-top: 5px;
    padding-bottom: 10px;
    color: #969696;
  }

  .qn-fill .body .must {
    font-weight: normal;
    color: crimson;
  }

  .qn-fill .body .q-opt {
    text-align: left;
    font-size: 16px;
    padding: 10px 10px 10px;
  }

  .qn-fill .body .el-checkbox {
    padding: 10px 0;
    display: block;
  }

  .qn-fill .body .q-opt .el-textarea__inner {
    max-height: 100px;
  }

  .qn-fill .body .submit-bt {
    padding-top: 30px;
    padding-bottom: 50px;
    /* margin-left: 26%; */
  }

  .qn-fill .tail {
    padding-top: 25px;
    font-size: 15px;
    color: #b9b9b9;
    /* border-top: solid 1px #e3e3e3; */
    height: 50px;
    margin-left: 28%;
  }
}
</style>