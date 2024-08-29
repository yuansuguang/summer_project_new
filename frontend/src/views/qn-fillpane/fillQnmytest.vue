<template>
  <div>
    <FinishTest v-if="success" :quesStorage="questions"></FinishTest>
    <div class="qn-fill" v-else>
      <div class="back-bt" v-if="mode === '0' || mode === 0">
        <el-button icon="el-icon-arrow-left" type="danger" @click="quit">退出预览</el-button>
      </div>
      <div class="paper">
        <div v-if="close" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../assets/images/survey2.png" alt="">
          </div>
          <h1 v-if="close">问卷已结束，感谢您的参与！</h1>
          <el-button type="primary" size="middle" @click="gotoHome">返回</el-button>
        </div>
        <!--        <div v-if="repeat" style="padding-bottom: 50px">-->
        <!--          <div class="tyn-icon">-->
        <!--            <img src="../../assets/images/survey2.png" alt="">-->
        <!--          </div>-->
        <!--          <h1 v-if="repeat">您已填写过此问卷！</h1>-->
        <!--          <el-button type="primary" size="middle" @click="gotoHome">返回</el-button>-->
        <!--        </div>-->
        <div class="body" v-else>

          <DeadTime v-if="finished_time !== '' && finished_time !== undefined" :endTime="finished_time"></DeadTime>

          <div class="title">
            {{ title }}
          </div>

          <div class="description" v-if="this.description !== ''">
            &emsp;&emsp;{{ description }}
          </div>

          <el-divider></el-divider>

          <div class="main">
            <div class="ques-block" v-for="item in questions" :key="item.id">
              <div class="q-title">
                {{ item.title }}
                <span class="must" v-if="item.must">(必填)</span>
                <span class="point" v-if="item.type !== 'name'
                  && item.type !== 'stuId'
                  && item.type !== 'class'
                  && item.type !== 'school'">
                  &ensp;[分值 : {{ item.point }}]
                </span>
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
                  <el-image class="img" :src="item.imgList[index + 1].url"
                    :preview-src-list="[item.imgList[index + 1].url]">
                  </el-image>
                </el-col>
              </el-row>
              <span style="color: #9b9ea0;font-size: x-small;margin: 5px"
                v-if="item.imgList.length !== 0">（点击图片查看大图）</span>


              <!--                视频-->
              <!-- <el-row class="block-img" v-for="i in item.videoList" :key="i.index">
                    <embed width=400 height=230 transparentatstart=true
                           animationatstart=false autostart=true autosize=false volume=100
                           displaysize=0 showdisplay=true showstatusbar=true showcontrols=true
                           showaudiocontrols=true showtracker=true showpositioncontrols=true
                           balance=true :src="i.url">
                  </el-row> -->

              <!--     姓名/学号/班级/学校-->
              <div class="q-opt" v-if="item.type === 'name'
                || item.type === 'stuId'
                || item.type === 'class'
                || item.type === 'school'">
                <el-input placeholder="请输入内容" v-model="answers[item.id - 1].ans" style="z-index: 0;">
                </el-input>
              </div>

              <!--              判断/单选-->
              <div v-if="item.type === 'radio' || item.type === 'judge'">
                <div class="q-opt" v-for="opt in item.options" :key="opt.id">
                  <el-radio v-if="item.type === 'radio' || item.type === 'judge'" v-model="answers[item.id - 1].ans"
                    :label="opt.title">
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
                  placeholder="请输入内容" v-model="answers[item.id - 1].ans">
                </el-input>
                <el-input v-if="item.row === 1" placeholder="请输入内容" v-model="answers[item.id - 1].ans" style="z-index: 0px;">
                </el-input>
              </div>

            </div>
          </div>
        </div>
        <div class="submit-bt">
          <el-button type="primary" size="default">暂存并退出</el-button>
          <el-button type="primary" @click="submit" size="default">提交</el-button>
        </div>
        <p></p>
        <p></p>
        <p></p>
        <el-divider/>
        <div class="tail">
          <a :href="rootUrl">问卷星球</a>&ensp;提供技术支持
        </div>
      </div>




    </div>
  </div>
</template>

<script>
import FinishTest from "@/views/qn-fillpane/FinishTest.vue";
import getDataApi from "@/utils/getDataApi";
import saveAnsApi from "@/utils/saveDataApi";
import toolApi from "@/utils/toolApi";
import DeadTime from "@/views/qn-fillpane/components/ddl.vue";
export default {
  name: "FillQn",
  mixins: [getDataApi, saveAnsApi, toolApi],
  components: { FinishTest, DeadTime },
  data() {
    return {
      // rootUrl: this.GLOBAL.baseUrl,
      success: false,
      close: false,
      repeat: false,
      // finished_time: '999',
      qn_id: '',
      mode: this.$route.query.mode,
      open: 1,
      duration: 999,
      title: '考试问卷Beta',
      description: '直接就是填写',
      questions: [
        {
          id: 1,
          type: 'name',
          title: '姓名',
          must: true, // 是否必填
          description: '111', // 问题描述
          options: [
            {
              title: '111', // 选项标题
              id: 0 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
        {
          id: 2,
          type: 'stuId',
          title: '学号',
          must: true, // 是否必填
          description: '111', // 问题描述
          options: [
            {
              title: '111', // 选项标题
              id: 0 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
        {
          id: 3,
          type: 'class',
          title: '班级',
          must: true, // 是否必填
          description: '111', // 问题描述
          options: [
            {
              title: '111', // 选项标题
              id: 0 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
        {
          id: 4,
          type: 'school',
          title: '学校',
          must: true, // 是否必填
          description: '111', // 问题描述
          options: [
            {
              title: '111', // 选项标题
              id: 0 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
        {
          id: 5,
          type: 'radio',
          title: '这是什么题',
          must: true, // 是否必填
          description: '111', // 问题描述
          options: [
            {
              title: '单选题', // 选项标题
              id: 0 // 选项id
            },
            {
              title: '多选题', // 选项标题
              id: 1 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
        {
          id: 6,
          type: 'checkbox',
          title: '哪些是正确答案',
          must: true, // 是否必填
          description: '111', // 问题描述
          options: [
            {
              title: '1+1=2', // 选项标题
              id: 0 // 选项id
            },
            {
              title: '1+4=2', // 选项标题
              id: 0 // 选项id
            },
            {
              title: '1+3=4', // 选项标题
              id: 0 // 选项id
            },
            {
              title: '1+4=4', // 选项标题
              id: 0 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
        {
          id: 7,
          type: 'text',
          title: '填点东西',
          must: true, // 是否必填
          description: '111', // 问题描述
          options: [
            {
              title: '描述', // 选项标题
              id: 0 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
        {
          id: 8,
          type: 'judge',
          title: '这是判断题',
          must: true, // 是否必填
          description: '1', // 问题描述
          options: [
            {
              title: '对', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '错', // 选项标题
              id: 2 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 20,  // 分值
          answer: '',
          imgList: [],
          // videoList: [],
          // last_question: 0,
          // last_option: 0,
          // is_shown: true,
          // question_id: 1,
          // qn_id: 456,
          // score: 10, // 最大评分
        },
      ],
      answers: [
        {
          question_id: '1',
          type: 'name',
          ans: null,
          ansList: [],
          answer: ''
        },
        {
          question_id: '2',
          type: 'stuId',
          ans: null,
          ansList: [],
          answer: ''
        },
        {
          question_id: '3',
          type: 'class',
          ans: null,
          ansList: [],
          answer: ''
        },
        {
          question_id: '4',
          type: 'school',
          ans: null,
          ansList: [],
          answer: ''
        },
        {
          question_id: '5',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: ''
        },
        {
          question_id: '6',
          type: 'checkbox',
          ans: null,
          ansList: [],
          answer: ''
        },
        {
          question_id: '7',
          type: 'text',
          ans: null,
          ansList: [],
          answer: ''
        },
        {
          question_id: '8',
          type: 'judge',
          ans: null,
          ansList: [],
          answer: ''
        },
      ],
      quesStorage: [],
      type: '',
      finished_time: new Date(),
    }
  },
  methods: {
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
      this.submitAns('2');
    },
    quit: function () {
      this.$confirm('请选择返回问卷编辑页面或问卷中心？', '确认信息', {
        distinguishCancelAndClose: true,
        confirmButtonText: '编辑页面',
        cancelButtonText: '问卷中心'
      })
        .then(() => {
          location.href = this.GLOBAL.baseUrl + "/edit_test?pid=" + this.$route.query.pid;
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
            this.duration = res.data.duration;
            this.finished_time = new Date();
            console.log("duration:", res.data.duration);
            this.finished_time.setMinutes(this.finished_time.getMinutes() + res.data.duration);
            console.log("finish time:", this.finished_time);
            this.questions = JSON.parse(res.data.data);
            this.answers = this.questions.map(question => ({
              id: question.id,
              type: question.type,
              ans: '',
              ansList: []
            }));
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
    //   this.getQnDataForFill(false, true, true);
    // }
    this.fetchQuestions();
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
    /* border-top: solid 1px #e3e3e3; */
    height: 50px;
    margin: 0 30px 130px;
  }
}

@media screen and (max-width: 600px) {
  .tyn-icon {
    margin: 50px;
    padding-top: 100px;
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

  .paper .submit-bt {
    padding-top: 30px;
    padding-bottom: 50px;
    margin-left: 26%;
    /* border-top: solid 1px #e3e3e3; */
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