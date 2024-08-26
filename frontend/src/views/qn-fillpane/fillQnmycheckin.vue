<template>
    <div class="qn-fill">
      <div class="back-bt" v-if="mode==='0' || mode===0">
        <el-button icon="el-icon-arrow-left" type="danger" @click="quit">退出预览</el-button>
      </div>
      <div class="paper">
        <div v-if="success" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../assets/images/survey2.png" alt="">
          </div>
          <h1 v-if="success">报名成功，感谢您的参与！</h1>
          <el-button type="primary" size="middle" @click="gotoHome">返回首页</el-button>
        </div>
        <div v-else-if="repeat" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../assets/images/survey2.png" alt="">
          </div>
          <h1 v-if="repeat">您已报名成功，请勿重复填写！</h1>
          <el-button type="primary" size="middle" @click="gotoHome">返回首页</el-button>
        </div>
        <div v-else-if="full" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../assets/images/survey2.png" alt="">
          </div>
          <h1 v-if="full">所选活动报名人数已满，可返回查看！</h1>
          <el-button type="primary" size="middle" @click="backToSurvey">返回查看</el-button>
        </div>
        <div v-else-if="allfull" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../assets/images/survey2.png" alt="">
          </div>
          <h1 v-if="allfull">报名人数已满，感谢参与！</h1>
          <el-button type="primary" size="middle" @click="gotoHome">返回首页</el-button>
        </div>
        <div v-else-if="close" style="padding-bottom: 50px">
          <div class="tyn-icon">
            <img src="../../assets/images/survey2.png" alt="">
          </div>
          <h1 v-if="close">问卷已结束，感谢您的参与！</h1>
          <el-button type="primary" size="middle" @click="gotoHome">返回首页</el-button>
        </div>
        <div class="body" v-else>
  
          <div class="title">
            {{ title }}
          </div>
  
          <div class="description" v-if="this.description!==''">
            &emsp;&emsp;{{ description }}
          </div>
  
          <el-divider></el-divider>
  
          <div class="main">
            <div class="ques-block" v-for="item in questions" :key="item.id">
              <!-- <div v-if="item.is_shown&&ahead(item.last_question)"> -->
              <div class="q-title">
                {{ item.id }}. {{ item.title }} <span class="must" v-if="item.must">(必填)</span>
              </div>
  
              <div
                  class="q-description"
                  v-if="item.description!=='' && item.description!==null && item.description!==undefined"
              >
                {{ item.description }}
              </div>
  
              <!--                  图片-->
              <el-row class="block-img" v-for="(i,index) in item.imgList" :key="i.index">
                <el-col :offset="4" :span="8" class="demo-image__preview" v-if="index%2===0">
                  <el-image class="img"
                      :src="i.url"
                      :preview-src-list="[i.url]">
                  </el-image>
                </el-col>
                <el-col :span="8" class="demo-image__preview" v-if="index%2===0&&index+1<=item.imgList.length-1">
                  <el-image class="img"
                      :src="item.imgList[index+1].url"
                      :preview-src-list="[item.imgList[index+1].url]">
                  </el-image>
                </el-col>
              </el-row>
              <span style="color: #9b9ea0;font-size: x-small;margin: 5px" v-if="item.imgList.length!==0">（点击图片查看大图）</span>
  
  
              <!--                视频-->
              <!-- <el-row class="block-img" v-for="i in item.videoList" :key="i.index">
                <embed width=400 height=230 transparentatstart=true
                       animationatstart=false autostart=true autosize=false volume=100
                       displaysize=0 showdisplay=true showstatusbar=true showcontrols=true
                       showaudiocontrols=true showtracker=true showpositioncontrols=true
                       balance=true :src="i.url">
              </el-row> -->
  
              <!--                  单选-->
              <div v-if="item.type==='radio'">
                <div class="q-opt" v-for="opt in item.options" :key="opt.id">
                  <el-radio v-if="item.type==='radio'" v-model="answers[item.id-1].ans" :label="opt.title">
                    {{ opt.title }}
                    <span style="color: #aaaaaa;font-size: small;margin-left: 15px" v-if="opt.hasNumLimit">剩余{{opt.supply-opt.consume}}</span>
                  </el-radio>
                </div>
              </div>
  
              <!--                  多选-->
              <el-checkbox-group class="q-opt" v-if="item.type==='checkbox'" v-model="answers[item.id-1].ansList">
                <el-checkbox v-for="opt in item.options" :key="opt.id" :label="opt.title">
                  {{ opt.title }}
                  <span style="color: #aaaaaa;font-size: small;margin-left: 15px" v-if="opt.hasNumLimit">剩余{{opt.supply-opt.consume}}</span>
                </el-checkbox>
              </el-checkbox-group>
  
              <!--                  填空-->
              <div class="q-opt" v-if="item.type==='text'||item.type==='name'||item.type==='stuId'||item.type==='class'||item.type==='school'||item.type==='phone'||item.type==='email'">
                <el-input
                    v-if="item.row>1"
                    type="textarea"
                    :autosize="{ minRows: 2, maxRows: item.row}"
                    placeholder="请输入内容"
                    v-model="answers[item.id-1].ans">
                </el-input>
                <el-input
                    v-if="item.row===1"
                    placeholder="请输入内容"
                    v-model="answers[item.id-1].ans">
                </el-input>
              </div>
  
              <!--                  评分-->
              <div class="q-opt" v-if="item.type==='mark'">
                <el-rate v-model="answers[item.id-1].ans" :max="item.score"></el-rate>
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
  </template>
  
  <script>
  // import getDataApi from "@/utils/getDataApi";
  // import saveAnsApi from "@/utils/saveDataApi";
  export default {
    name: "FillQn",
    // mixins: [getDataApi, saveAnsApi],
    data() {
      return {
        timer: '',
        // rootUrl: this.GLOBAL.baseUrl,
  
        success: false,
        close: false,
        repeat: false,
        full: false,
        allfull: false,
  
        mode: this.$route.query.mode,
        title: '',
        description: '',
        questions: [
          {
            last_question: 0,
            last_option: 0,
            is_shown: true,
            question_id: 123,
            qn_id: 456,
            refer: "问卷星球",
            point: 20,
            id: 1,
            type:'checkbox',
            title:'志愿报名',
            must: true, // 是否必填
            description: '', // 问题描述
            options:[
              {
                hasNumLimit:true,
                title:'11111', // 选项标题
                id: 0 ,// 选项id
                supply:5,
                consume:0,
              },
              {
                hasNumLimit:true,
                title:'22222', // 选项标题
                id: 1 ,// 选项id
                supply:10,
                consume:0,
              }
            ],
            row:1, // 填空区域行数
            score:10, // 最大评分
            answer: "",
            imgList: [],
            videoList: []
          },
          {
            last_question: 0,
            last_option: 0,
            is_shown: true,
            question_id: 1234,
            qn_id: 4567,
            refer: "问卷星球",
            point: 20,
            id: 2,
            type:'radio',
            title:'四六级报名',
            must: true, // 是否必填
            description: '', // 问题描述
            options:[
              {
                hasNumLimit:true,
                title:'11111', // 选项标题
                id: 0 ,// 选项id
                supply:500,
                consume:0,
              },
              {
                hasNumLimit:true,
                title:'22222', // 选项标题
                id: 1 ,// 选项id
                supply:1,
                consume:0,
              }
            ],
            row:1, // 填空区域行数
            score:10, // 最大评分
            answer: "",
            imgList: [],
            videoList: []
          },
        ],
        answers: [
          {
            question_id: '1',
            type: '1',
            ans: null,
            ansList: [],
          },
          {
            question_id: '2',
            type: '2',
            ans: null,
            ansList: [],
          },
        ],
        // answers: [],
        type: ''
      }
    },
    methods: {
      autoGet() {
        if (this.mode === '0') {
          this.getQnDataForPreview(true);
        }
        else if (this.mode === '1') {
          this.getQnDataForFill(true);
        }
      },
      gotoHome() {
        this.$router.push('/');
      },
      backToSurvey() {
        this.success = false;
        this.full = false;
        this.allfull = false;
        this.repeat = false;
        this.close = false;
        location.reload();
      },
      submit: function () {
        clearInterval(this.timer);
        // this.submitAns("4");
      },
      quit: function () {
        this.$confirm('请选择返回问卷编辑页面或问卷中心？', '确认信息', {
          distinguishCancelAndClose: true,
          confirmButtonText: '编辑页面',
          cancelButtonText: '问卷中心'
        })
        .then(() => {
          location.href = this.GLOBAL.baseUrl + "/edit_form?pid=" + this.$route.query.pid;
        })
        .catch(action => {
          if (action === 'cancel') {
            this.$router.push('/index');
          }
        });
  
      },
    },
    created() {
      if (this.mode === '0') {
        this.getQnDataForPreview();
      }
      else if (this.mode === '1') {
        this.getQnDataForFill();
      }
    },
    mounted() {
      this.timer = setInterval(this.autoGet, 1000);
    },
    beforeUnmount() {
      clearInterval(this.timer);
    }
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