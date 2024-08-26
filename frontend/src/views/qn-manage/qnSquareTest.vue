<template>
  <div>
    <FinishTest v-if="success || repeat" :quesStorage="questions"></FinishTest>
    <div class="qn-fill" v-else>
      <div class="back-bt" v-if="mode==='0' || mode===0">
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
        <div class="body" v-else>

          <DeadTime v-if="finished_time!==''&&finished_time!==undefined" :endTime="finished_time"></DeadTime>

          <div class="title">
            {{ title }}
          </div>

          <div class="description" v-if="this.description!==''">
            &emsp;&emsp;{{ description }}
          </div>

          <el-divider></el-divider>

          <div class="main">
            <div class="ques-block" v-for="item in questions" :key="item.id">
              <div class="q-title">
                {{ item.id }}. {{ item.title }}
                <span class="must" v-if="item.must">(必填)</span>
                <span
                    class="point"
                    v-if="item.type!=='name'
                   && item.type!=='stuId'
                   && item.type!=='class'
                   && item.type!=='school'"
                >
                &ensp;[分值 : {{ item.point }}]
              </span>
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
                    <el-image
                        style="width: 200px; height: 200px"
                        :src="i.url"
                        :preview-src-list="[i.url]">
                    </el-image>
                  </el-col>
                  <el-col :span="8" class="demo-image__preview" v-if="index%2===0&&index+1<=item.imgList.length-1">
                    <el-image
                        style="width: 200px; height: 200px"
                        :src="item.imgList[index+1].url"
                        :preview-src-list="[item.imgList[index+1].url]">
                    </el-image>
                  </el-col>
                </el-row>
                <span style="color: #9b9ea0;font-size: x-small;margin: 5px" v-if="item.imgList.length!==0">（点击图片查看大图）</span>


                <!--                视频-->
                <el-row class="block-img" v-for="i in item.videoList" :key="i.index">
                  <embed width=400 height=230 transparentatstart=true
                         animationatstart=false autostart=true autosize=false volume=100
                         displaysize=0 showdisplay=true showstatusbar=true showcontrols=true
                         showaudiocontrols=true showtracker=true showpositioncontrols=true
                         balance=true :src="i.url">
                </el-row>

              <!--     姓名/学号/班级/学校-->
              <div class="q-opt"
                   v-if="item.type === 'name'
                   || item.type === 'stuId'
                   || item.type === 'class'
                   || item.type === 'school'">
                <el-input
                    placeholder="请输入内容"
                    v-model="answers[item.id-1].ans">
                </el-input>
              </div>

              <!--              判断/单选-->
              <div v-if="item.type==='radio' || item.type === 'judge'">
                <div class="q-opt" v-for="opt in item.options" :key="opt.id">
                  <el-radio v-if="item.type==='radio' || item.type === 'judge'" v-model="answers[item.id-1].ans" :label="opt.title">
                  {{ opt.title }}
                </el-radio>
                </div>
              </div>

              <!--                  多选-->
              <el-checkbox-group class="q-opt" v-if="item.type==='checkbox'" v-model="answers[item.id-1].ansList">
                <el-checkbox v-for="opt in item.options" :key="opt.id" :label="opt.title">
                  {{ opt.title }}
                </el-checkbox>
              </el-checkbox-group>

              <!--                  填空-->
              <div class="q-opt" v-if="item.type==='text'">
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

            </div>
          </div>
          </div>
          <div class="submit-bt">
            <el-button type="primary" @click="submit">提交</el-button>
          </div>

        </div>

        <div class="tail">
          <a :href="rootUrl">问卷星球</a>&ensp;提供技术支持
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
  components: {FinishTest, DeadTime},
  data() {
    return {
      // rootUrl: this.GLOBAL.baseUrl,

      success: false,
      close: false,
      repeat: false,

      qn_id: '',
      mode: this.$route.query.mode,
      open: 1,
      title: '禁毒日禁毒知识测试',
      description: '本测试针对禁毒知识测试，共20道题，满分100分。',
      questions: [
        {
          id: 1,
          type: 'radio',
          title: '“国际禁毒日”是每年的哪一天?',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
            {
              title: '3月15日', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '7月28日', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '6月26日', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '5月17日', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          type: 'radio',
          title: '我国《刑法》对毒品犯罪的刑事责任年龄的规定，对已满14周岁不满16周岁的人，犯贩卖毒品罪的，应当（）',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '从轻或减轻处罚', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '责令其家长或者监护人加以管教，必要时也可以由政府收容教养', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '负刑事责任', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '不予刑事处罚', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          type: 'radio',
          title: '长期使用冰毒会导致大脑机能损坏，并伴有精神分裂，从而导致（）',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '暴力行为', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '自闭', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '抑郁', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '自杀', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          type: 'radio',
          title: '毒品的基本特征不包括（ ）',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '依赖性', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '治疗性', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '非法性', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '危害性', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          title: '“银三角”地区盛产',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '大麻', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '吗啡', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '鸦片', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '古柯、可卡因', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          type: 'radio',
          title: '“毒源地金三角”地区毗邻我国，位于（）三国交界处',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '老挝、泰国、缅甸', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '越南、马来西亚、缅甸', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '阿富汗、巴基斯坦、伊朗', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '泰国、缅甸、柬埔寨', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          type: 'radio',
          title: '“金新月”位于（）三国交界地带',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '越南、马来西亚、缅甸', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '阿富汗、巴基斯坦、伊朗', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '老挝、泰国、缅甸', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '泰国、缅甸、柬埔寨', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          type: 'radio',
          title: '走私毒品罪，是指违反国家对毒品管制的法规，逃避海关监管，非法运输或携带毒品出入国（边）境的行为。',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
            {
              title: '是', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '否', // 选项标题
              id: 2 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 9,
          type: 'radio',
          title: '冰毒是否属于麻醉药品？',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
            {
              title: '是', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '否', // 选项标题
              id: 2 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 10,
          type: 'radio',
          title: '走私、贩卖、运输、制造海洛因（）克，可判处死刑。',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '20', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '30', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '40', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '50', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 11,
          type: 'radio',
          title: '吸食大麻烟可引起气管炎、咽炎、气喘发作、喉头水肿等疾病。吸一支大麻烟对肺功能的影响比一支香烟大（ ）倍。',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '5', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '10', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '15', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '30', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 12,
          type: 'radio',
          title: '毒品犯罪诱发多种犯罪，严重影响社会安定。据统计，在我国男性吸毒人员中（ ）有犯罪行为。',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '50%', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '60%', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '70%', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '80%', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 13,
          type: 'radio',
          title: '吸毒成瘾的三个基本过程包括：耐药作用的形成，（），强化的形成。',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '对毒品反映减弱', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '身体依赖性的消失', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '对毒品反映增强', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '身体依赖性的产生', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 14,
          type: 'radio',
          title: '下面哪种不属于兴奋剂类毒品',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '可卡因', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '海洛因', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '摇头丸', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '冰毒', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 15,
          type: 'radio',
          title: '下列对世界“三大毒源”地区描述正确的是',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '“金三角”地区、“金新月”地区、“银三角”地区', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '“金三角”地区、“金新月”地区、“银新月”地区', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '“金新月”地区、“银新月”地区、“银三角”地区', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '“金三角”地区、“银三角”地区、南美地区', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 16,
          type: 'radio',
          title: '我国目前禁毒预防教育的重点是（）。',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '流动人口', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '无业人员', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '文化素质较低的人群', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '青少年', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 17,
          type: 'radio',
          title: '海洛因吸毒者的典型体征是什么？',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '身体浮肿', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '瞳孔缩小呈针尖样', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '身体瘦弱', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '瞳孔放大，不聚光', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 18,
          type: 'radio',
          title: '戒毒后复吸的原因包括：（），稽延性症状的折磨，副性生活事件的影响。',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '心瘾未除', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '使用的毒品毒性较强', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '吸毒时间长', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '戒毒时间过短', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 19,
          type: 'radio',
          title: '申请成为禁毒志愿者的年龄要求',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '没要求', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '14周岁以上', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '16周岁以上', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '18周岁以上', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          id: 20,
          type: 'radio',
          title: '对吸毒人员吸毒后的变化描述错误的是',
          must: true, // 是否必填
          description: '', // 问题描述
          options: [
          {
              title: '不明用途支出增多，编造各种谎言向家人要钱，向亲友借钱，甚至偷拿家中财物。', // 选项标题
              id: 1 // 选项id
            },
            {
              title: '发生明显改变，脾气变得暴躁、易怒，甚至狠毒、残忍。', // 选项标题
              id: 2 // 选项id
            },
            {
              title: '生活规律发生改变，一般饮茶与白酒，不喜欢吃水果。', // 选项标题
              id: 3 // 选项id
            },
            {
              title: '健康状况明显下降，表现为疲倦、憔悴、消瘦、衰老等。', // 选项标题
              id: 4 // 选项id
            },
          ],
          row: 1, // 填空区域行数
          refer: '', // 参考答案
          point: 5,  // 分值
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
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '6月26日'
        },
        {
          question_id: '2',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '负刑事责任'
        },
        {
          question_id: '3',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '自杀'
        },
        {
          question_id: '4',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '治疗性'
        },
        {
          question_id: '5',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '古柯、可卡因'
        },
        {
          question_id: '6',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '老挝、泰国、缅甸'
        },
        {
          question_id: '7',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '阿富汗、巴基斯坦、伊朗'
        },
        {
          question_id: '8',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '是'
        },
        {
          question_id: '9',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '否'
        },
        {
          question_id: '10',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '50'
        },
        {
          question_id: '11',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '10'
        },
        {
          question_id: '12',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '80%'
        },
        {
          question_id: '13',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '身体依赖性的消失'
        },
        {
          question_id: '14',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '海洛因'
        },
        {
          question_id: '15',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '“金三角”地区、“金新月”地区、“银三角”地区'
        },
        {
          question_id: '16',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '青少年'
        },
        {
          question_id: '17',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '瞳孔缩小呈针尖样'
        },
        {
          question_id: '18',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '心瘾未除'
        },
        {
          question_id: '19',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '18周岁以上'
        },
        {
          question_id: '20',
          type: 'radio',
          ans: null,
          ansList: [],
          answer: '生活规律发生改变，一般饮茶与白酒，不喜欢吃水果。'
        },
      ],
      quesStorage: [],
      type: '',
      finished_time: '',
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
              url: '/question/api/listquestionforfill',
              data: formData,
          }).then(res => {
              switch (res.data.status_code) {
              case 1:
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
.tyn-icon {
  margin: 50px ;
  padding-top: 100px;
}
.qn-fill {
  background-image: url("../../assets/images/preview_background.png");
  background-repeat: repeat-y;
  min-height: 800px;
  overflow: hidden;
  background-position:center;
  background-size: 100% auto;
  background-attachment: fixed;
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

.qn-fill .body .point {
  font-weight: normal;
  color: #EC9D2D;
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
</style>