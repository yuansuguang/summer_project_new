<template>
  <div>
    <FinishVote v-if="success || repeat" :questions="questions"></FinishVote>
    <div class="qn-fill" v-else>
      <div class="back-bt" v-if="mode === '0' || mode === 0">
        <el-button icon="el-icon-arrow-left" type="danger" @click="quit">退出预览</el-button>
      </div>
      <div class="paper">
        <div v-if="success" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../../src/assets/images/Edit.png" alt="">
          </div>
          <h1 v-if="success">提交成功，感谢您的参与！</h1>
          <el-button type="primary" size="middle" @click="backToSurvey">查看投票结果</el-button>
        </div>
        <div v-else-if="close" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../assets/images/survey2.png" alt="">
          </div>
          <h1 v-if="close">问卷已结束，感谢您的参与！</h1>
          <el-button type="primary" size="middle">返回</el-button>
        </div>
        <div class="body" v-else>

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
                {{ item.id }}. {{ item.title }}
                <span class="must" v-if="item.must">(必填)</span>
                <span class="voteQs" v-if="item.isVote"> [投票题] </span>
              </div>

              <div class="q-description"
                v-if="item.description !== '' && item.description !== null && item.description !== undefined">
                {{ item.description }}
              </div>

              <!--                  单选-->
              <div v-if="item.type === 'radio'">
                <div class="q-opt" v-for="opt in item.options" :key="opt.id">
                  <el-radio v-if="item.type === 'radio'" v-model="answers[item.id - 1].ans" :label="opt.title">
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
                <el-input v-if="item.row === 1" placeholder="请输入内容" v-model="answers[item.id - 1].ans">
                </el-input>
              </div>

              <!--                  评分-->
              <div class="q-opt" v-if="item.type === 'mark'">
                <el-rate v-model="answers[item.id - 1].ans" :max="item.score"></el-rate>
              </div>
            </div>
          </div>

          <div class="submit-bt">
            <el-button type="primary" size="default">暂存并退出</el-button>
            <el-button type="primary" @click="submit" size="default">提交</el-button>
          </div>

        </div>

        <div class="tail">
          <a :href="rootUrl">问卷星球</a>&ensp;提供技术支持
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FinishVote from "@/views/qn-fillpane/FinishVote";
// import getDataApi from "@/utils/getDataApi";
// import saveAnsApi from "@/utils/saveDataApi";
export default {
  name: "FillQn",
  // mixins: [getDataApi, saveAnsApi],
  components: { FinishVote },
  data() {
    return {
      repeat: false,
      // rootUrl: this.GLOBAL.baseUrl,
      success: false,
      close: false,
      mode: this.$route.query.mode,
      open: 1,
      surveyId: 0,
      title: '',
      description: '',
      questions: [
        {
          question_id: 0,
          id: 1,
          type: 'radio',
          title: '鸡煲人上人',
          must: true, // 是否必填
          isVote: true,//是否是投票题
          description: '转来转去像个小丑', // 问题描述
          options: [
            {
              title: '鸡煲', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '劣人', // 选项标题
              id: 2 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          score: 5, // 最大评分
        }
      ],
      answers: [
        {
          question_id: '1',
          type: 'name',
          ans: null,
          ansList: [],
        },
      ],
      type: ''
    }
  },
  methods: {
    backToSurvey() {
      this.$router.push({ name: 'questionaireDataview', params: { qnid: this.surveyId } });
    },
    submit: function () {
      this.submitAns("3");
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
            this.surveyId = res.data.surveyId;
            this.title = res.data.title;
            this.description = res.data.description;
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
  mounted() {
  },
  created() {
    // if (this.mode === '0') {
    //   this.getQnDataForPreview();
    // }
    // else if (this.mode === '1') {
    //   this.getQnDataForFill();
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
    border-top: solid 1px #e3e3e3;
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