<template>
  <div id="manage" style="height: 150%; width: 100%; background-color:aliceblue ;position: absolute;">
    <!-- Sidebar -->
    <!-- <div id="sidebar">
      <button class="button" id="create-survey" @click="createSurvey">+ 创建问卷</button>
      <button class="button">全部问卷</button>
      <button class="button" id="collected-questionnaire" @click="collectedQuestionnaire">星标问卷</button>
      <button class="button" id="recycle-bin" @click="recycleBin">回收站</button>
      <button class="button">文件夹</button>
      <div id="description">
        <div id="description-text">绑定微信后，可在手机同步编辑、管理问卷，实时掌握数据动态。</div>
        <button class="button" id="bind-wechat">绑定微信</button>
      </div>
    </div> -->
    <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
      style="height: 92%; top: 8%;position: fixed;display: flex;align-content: center;flex-direction: column;align-items: center">
      <el-menu-item index="1" style="height: 10%; width: 100%;">
        <span>&emsp;&emsp;</span>
        <el-icon>
          <DocumentChecked />
        </el-icon>
        <span style="font-size: 15px;">全部问卷&emsp;&emsp;&emsp;</span>
      </el-menu-item>
      <el-menu-item index="2" style="height: 10%; width: 100%;" @click="collectedQuestionnaire">
        <span>&emsp;&emsp;</span>
        <el-icon>
          <Star />
        </el-icon>
        <span style="font-size: 15px;">收藏问卷&emsp;&emsp;&emsp;</span>
      </el-menu-item>
      <el-menu-item index="3" style="height: 10%; width: 100%;" @click="recycleBin">
        <span>&emsp;&emsp;</span>
        <el-icon>
          <Delete />
        </el-icon>
        <span style="font-size: 15px;">回收站&emsp;&emsp;&emsp;</span>
      </el-menu-item>
      <el-menu-item index="4" style="height: 10%; width: 100%;" @click="historyBin">
        <span>&emsp;&emsp;</span>
        <el-icon>
          <Setting />
        </el-icon>
        <span style="font-size: 15px;">历史记录&emsp;&emsp;&emsp;</span>
      </el-menu-item>

      <img src="@/assets/images/ques1.png" style="width: 200px; height: 200px;margin-top: 30%;">
      <el-button type="primary" size="large" style="width: 80%; font-size: 20px; font-family: 'JinBuTi';" :style="{
        boxShadow: `var(--el-box-shadow-dark)`,
        borderRadius: `var(--el-border-radius-round)`,
      }" @click="createSurvey">+ 新建问卷</el-button>
    </el-menu>
    <!-- Content -->
    <div id="content">
      <div class="toolbar">
        <div id="survey-title" style="font-size: 40px; font-family: 'JinBuTi';">我的问卷</div>
        <div class="sort-container" @mouseenter="showSortOptions = true" @mouseleave="showSortOptions = false">
          <el-dropdown>
            <el-button link size="dafault"><el-icon>
                <SortDown />
              </el-icon>时间排序</el-button>
            <template #dropdown>
              <el-row><span>&emsp;</span><el-radio v-model="ascendingChecked" @click="updateSort1" value="0"
                  size="dafault">时间正序&emsp;</el-radio></el-row>
              <el-row><span>&emsp;</span><el-radio v-model="descendingChecked" @click="updateSort2" value="1"
                  size="dafault">时间倒序&emsp;</el-radio></el-row>
            </template>
          </el-dropdown>

          <!-- <div v-if="showSortOptions" class="sort-options">
            <label>
              <input type="checkbox" v-model="ascendingChecked" @click="updateSort1"> 时间正序
            </label>
            <label>
              <input type="checkbox" v-model="descendingChecked" @click="updateSort2"> 时间倒序
            </label>
          </div> -->
        </div>

        <div class="mytype-container" @mouseenter="showTypeOptions = true" @mouseleave="showTypeOptions = false">
          <el-dropdown>
            <el-button link size="dafault"><el-icon>
                <SortDown />
              </el-icon>问卷类型</el-button>
            <template #dropdown>
              <el-checkbox-group v-model="checkedTypes" :max="1"
                style="display: flex; align-content: center; flex-direction: column; align-items: center; width: 100px;">
                <el-row><span>&emsp;</span><el-checkbox @click="updateTypetoNormal" :label="'a'" :value="'a'"
                    size="dafault">普通型&emsp;</el-checkbox></el-row>
                <el-row><span>&emsp;</span><el-checkbox @click="updateTypetoVote" :label="'b'" :value="'b'"
                    size="dafault">投票型&emsp;</el-checkbox></el-row>
                <el-row><span>&emsp;</span><el-checkbox @click="updateTypetoApplication" :label="'c'" :value="'c'"
                    size="dafault">报名型&emsp;</el-checkbox></el-row>
                <el-row><span>&emsp;</span><el-checkbox @click="updateTypetoTest" :label="'d'" :value="'d'"
                    size="dafault">考试型&emsp;</el-checkbox></el-row>
                <!-- <el-row><span>&emsp;</span><el-checkbox @click="updateTypetoAll" :label="'e'" :value="'e'"
                  size="dafault">全部问卷</el-checkbox></el-row> -->
              </el-checkbox-group>
            </template>
          </el-dropdown>

          <!-- <div  class="type-options">
            <label>
              <input type="checkbox" v-model="isVote" @click="updateTypetoVote"> 投票型
            </label>
            <label>
              <input type="checkbox" v-model="isApplication" @click="updateTypetoApplication"> 报名型
            </label>
            <label>
              <input type="checkbox" v-model="isTest" @click="updateTypetoTest"> 考试型
            </label>
            <label>
              <input type="checkbox" v-model="isNormal" @click="updateTypetoNormal"> 普通型
            </label>
            <label>
              <input type="checkbox" v-model="isAll" @click="updateTypetoAll"> 全部问卷
            </label>
          </div> -->
        </div>

        <div class="realease-container">
          <el-dropdown>
            <el-button link size="dafault"><el-icon>
                <SortDown />
              </el-icon>问卷状态</el-button>
            <template #dropdown>
              <el-checkbox-group v-model="checkedTypesB" :max="1"
                style="display: flex; align-content: center; flex-direction: column; align-items: center; width: 100px;">
                <el-row><span>&emsp;</span><el-checkbox @click="updateRealease1" :label="'a'" :value="'a'"
                    size="dafault">已发布&emsp;</el-checkbox></el-row>
                <el-row><span>&emsp;</span><el-checkbox @click="updateRealease2" :label="'b'" :value="'b'"
                    size="dafault">未发布&emsp;</el-checkbox></el-row>
                <!-- <el-row><span>&emsp;</span><el-radio v-model="isAll" @click="updateTypetoAll"
                  size="dafault">所有问卷&emsp;</el-radio></el-row> -->
              </el-checkbox-group>
            </template>
          </el-dropdown>
          <!-- <button>状态</button>
          <div v-if="showRealeaseOptions" class="realease-options">
            <label>
              <input type="checkbox" v-model="realeaseChecked" @click="updateRealease"> 已发布
            </label>
            <label>
              <input type="checkbox" v-model="notRealeaseChecked" @click="updateRealease"> 未发布
            </label>
          </div> -->
        </div>

        <div class="search-box" style="width: 270px; left: 650px; margin-top:100px; position: relative">
          <el-input v-model="input3" style="max-width: 600px" placeholder="请输入搜索内容" class="input-with-select"
            size="dafault">

            <template #append>
              <el-button @click="search">搜索</el-button>
            </template>
          </el-input>
        </div>
      </div>
      <div v-for="(questionnaire, index) in paginatedQuestionnaires" :key="index" class="questionnaire">
        <!-- 第一行 -->
        <div class="questionnaire-info">
          <div class="info-left">
            <span>{{ questionnaire.questionnaireName }}</span>
          </div>
          <!-- <span>id: {{ questionnaire.questionnaireId }}&emsp;</span> -->
          <span>类型：{{ questionnaire.questionType }}&emsp;</span>
          <!-- <span>{{ isPublished ? '已发布' : '未发布' }}</span> -->
          <span :class="{ 'icon-published': questionnaire.isPublished, 'icon-unpublished': !questionnaire.isPublished }"
            :style="{ color: questionnaire.isPublished ? 'green' : 'red' }">
            <img :src="publishedImagePath(questionnaire.isPublished)" alt="release status" class="icon">
            {{ questionnaire.isPublished ? '已发布' : '未发布' }}&emsp;
          </span>
          <!-- <span>答卷: {{ answersCount }}</span> -->
          <span>答卷: <span :style="{ color: questionnaire.answersCount > 0 ? 'blue' : '' }">{{ questionnaire.answersCount
              }}</span>&emsp;</span>
          <span>创建时间：{{ questionnaire.creationDate }}&emsp;</span>
        </div>
        <!-- 分隔线 -->
        <div class="separator"></div>
        <!-- 第二行按钮 -->
        <div class="questionnaire-actions">
          <div class="button-container">
            <div class="leftPart">
              <button @click="edit(questionnaire)" class="leftButton">
                <img src="../../../src/assets/images/Edit.png" alt="edit-icon" class="icon">
                编辑
              </button>

              <button @click="preview(questionnaire)" class="leftButton">
                <img src="../../../src/assets/images/Preview.png" alt="preview-icon" class="icon">
                预览
              </button>

              <button @click="share(questionnaire)" class="leftButton">
                <img src="../../../src/assets/images/Share.png" alt="share-icon" class="icon">
                分享
              </button>

              <el-dropdown>
                <button class="leftButton">
                  <img src="../../../src/assets/images/Stats.png" alt="statistics-icon" class="icon">
                  数据分析
                </button>
                <template #dropdown>
                  <el-dropdown-menu
                    style=" display: flex; flex-direction: column; align-items: center; align-content: center;">
                    <el-dropdown-item style=" height: 30px; font-size: 13px;" @click="statistics(questionnaire)"><el-icon><TopRight /></el-icon>朴素分析</el-dropdown-item>
                    <el-dropdown-item style=" height: 30px; font-size: 13px;" @click="CrossAnalysis(questionnaire)"><el-icon><Rank /></el-icon>交叉分析</el-dropdown-item>
                    <!-- <el-dropdown-item>Action 4</el-dropdown-item>
          <el-dropdown-item>Action 5</el-dropdown-item> -->
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <button @click="clear(questionnaire)" class="leftButton">
                <img src="../../../src/assets/images/ClearAll.png" alt="clear-icon" class="icon">
                清空
              </button>

              <!-- <button @click="exportData" class="leftButton">
                <img src="../../../src/assets/images/ExportData.png" alt="exportData-icon" class="icon">
                导出
              </button> -->
            </div>
            <div class="rightPart">
              <button v-if="questionnaire.isPublished" @click="pause(questionnaire)" class="rightButton">
                <img
                  :src="questionnaire.isPaused ? require('../../../src/assets/images/Start.png') : require('../../../src/assets/images/PauseRed.png')"
                  alt="pause-icon" class="icon">
                <span :class="{ 'text-red': !questionnaire.isPaused, 'text-black': questionnaire.isPaused }">{{
                  questionnaire.isPaused ? '继续' : '暂停' }}</span>
              </button>

              <button @click="copy(questionnaire, VindexToRindex(index))" class="rightButton">
                <img src="../../../src/assets/images/Copy.png" alt="copy-icon" class="icon">
                复制
              </button>

              <button @click="favorite(questionnaire)" class="rightButton">
                <img
                  :src="questionnaire.isFavorited ? require('../../../src/assets/images/Like.png') : require('../../../src/assets/images/LightLike.png')"
                  alt="favorite-icon" class="icon">
                {{ questionnaire.isFavorited ? '已收藏' : '收藏&emsp;' }}
              </button>

              <button @click="remove(questionnaire, VindexToRindex(index))" class="rightButton">
                <img src="../../../src/assets/images/Delete.png" alt="remove-icon" class="icon">
                删除
              </button>
            </div>
          </div>
        </div>
        
        <el-dialog :title="发布链接" v-model="questionnaire.publishDialogVisible" class="dialog" style="min-width:400px; display: flex; align-items: center;">
            <el-row><span>发布链接：{{ linkShare }}</span></el-row>
        </el-dialog>

        <el-dialog :title="预览问卷" v-model="questionnaire.previewVisible" class="dialog" width="600px">
          <el-row class="ques-block" v-for="item in questions" :key="item.id" :style="{

            borderRadius: `var(--el-border-radius-round)`,
          }">

            <el-col :span="16" class="block-content">
              <div class="block-title">
                {{ item.id }}. {{ item.title }} <span class="must" v-if="item.must">(必填)</span>
              </div>

              <div class="block-info" v-if="item.type === 'name' || item.type === 'stuId' || item.type === 'class' || item.type === 'school'
                || item.type === 'phone' || item.type === 'email'">
                <el-input placeholder="请输入内容" style="margin-left: 10px">
                </el-input>
              </div>

              <div class="block-choice" v-if="item.type === 'sex'">
                <div style="padding-bottom: 10px"><el-radio value="0">男</el-radio></div>
                <div><el-radio value="0">女</el-radio></div>
              </div>

              <div class="block-description"
                v-if="item.description !== '' && item.description !== null && item.description !== undefined">
                {{ item.description }}
              </div>

              <!--                  图片-->
              <!-- <el-row class="block-img" v-for="(i, index) in item.imgList" :key="i.index">
          <el-col :offset="2" :span="10" class="demo-image__preview" v-if="index % 2 === 0">
            <el-image style="width: 200px; height: 200px" :src="i.url" :preview-src-list="[i.url]">
            </el-image>
          </el-col>
          <el-col :span="10" class="demo-image__preview" v-if="index % 2 === 0 && index + 1 <= item.imgList.length - 1">
            <el-image style="width: 200px; height: 200px" :src="item.imgList[index + 1].url"
              :preview-src-list="[item.imgList[index + 1].url]">
            </el-image>
          </el-col>
        </el-row>
        <span style="color: #9b9ea0;font-size: x-small" v-if="item.imgList.length !== 0">（点击图片查看大图）</span> -->


              <!--                视频-->
              <!-- <el-row class="block-img" v-for="i in item.videoList" :key="i.index">
          <embed width=400 height=230 transparentatstart=true animationatstart=false autostart=true autosize=false
            volume=100 displaysize=0 showdisplay=true showstatusbar=true showcontrols=true showaudiocontrols=true
            showtracker=true showpositioncontrols=true balance=true :src="i.url">
        </el-row> -->


              <div class="block-choice" v-for="ans in item.options" :key="ans.id">

                <!--                  单选-->
                <el-radio v-if="item.type === 'radio'" value="0">
                  {{ ans.title }}<span style="color: #aaaaaa;font-size: small;margin-left: 15px"
                    v-if="ans.hasNumLimit">剩余{{
                      ans.supply - ans.consume }}&emsp;总计{{ ans.supply }}</span>
                </el-radio>

                <!--                  多选-->
                <el-checkbox v-if="item.type === 'checkbox'" value="0">
                  {{ ans.title }}
                  <span style="color: #aaaaaa;font-size: small;margin-left: 15px" v-if="ans.hasNumLimit">剩余{{
                    ans.supply -
                    ans.consume }}&emsp;总计{{ ans.supply }}</span>
                </el-checkbox>

                <!--                  填空-->
                <el-input v-if="item.type === 'text' && item.row > 1" type="textarea" placeholder="请输入内容"
                  v-bind="ans.title">
                </el-input>
                <el-input v-if="item.type === 'text' && item.row === 1" placeholder="请输入内容" v-bind="ans.title">
                </el-input>
              </div>

              <div class="block-choice" v-if="item.type === 'mark'">
                <!--                  评分-->
                <el-rate value="0" :max="item.score"></el-rate>
              </div>

              <!--                 关联信息-->
              <div class="block-relation" v-if="isLogic && item.last_question !== 0">
                <!-- <div>{{ relatedQs(item) }}</div> -->
                <div>关联逻辑待设置</div>
              </div>
            </el-col>
          </el-row>
        </el-dialog>

      </div>

      <div class="survey-page">
        <div class="pagination" v-if="totalPages >= 1">
          <el-button
            @click="previousPage"
            :style="{ color: currentPage === 1 ? '#d9d9d9' : 'black' }"
            :disabled="currentPage === 1"
            link
            size="default"
          >上一页</el-button>
          <span>&emsp;第 {{ currentPage }} 页 / 共 {{ totalPages }} 页&emsp;</span>
          <el-button
            @click="nextPage" 
            :style="{ color: currentPage === totalPages ? '#d9d9d9' : 'black' }"
            :disabled="currentPage === totalPages"
            link
            size="default"
          >下一页</el-button>
          <el-row><span>&emsp;</span></el-row>
          <el-row><span>&emsp;</span></el-row>
        </div>
      </div>

    </div>
  </div>

</template>



<script>
// import QnInstance from './qnInstance.vue';
import { ElMessageBox } from 'element-plus';

export default {
  data() {
    return {
      showSortOptions: false,
      showTypeOptions: false,
      ascendingChecked: false,
      descendingChecked: false,
      showRealeaseOptions: false,
      realeaseChecked: false,
      notRealeaseChecked: false,
      isVote: false,
      isApplication: false,
      isTest: false,
      isNormal: false,
      isAll: false,
      questionnaires: [],
      checkedTypes: [],
      checkedTypesB: [],
      itemsPerPage: 4,
      currentPage: 1,
      input3: '',
      keyword: '',
      linkShare: '',
      //previewVisible: false,
      questions: [
        // {
        //   id: 1,
        //   type: 'checkbox',
        //   title: '您常玩的游戏类型是？',
        //   description: '',
        //   must: true,
        //   options: [{
        //     id: 1,
        //     title: 'RPG',
        //   }, {
        //     id: 2,
        //     title: '动作',
        //   }, {
        //     id: 3,
        //     title: '卡牌',
        //   }, {
        //     id: 4,
        //     title: 'Rougelike',
        //   }, {
        //     id: 5,
        //     title: '解密',
        //   }, {
        //     id: 6,
        //     title: '塔防',
        //   }, {
        //     id: 7,
        //     title: '类银河恶魔城',
        //   }],
        //   row: 0,
        //   score: 0,
        // },
        // {
        //   id: 2,
        //   type: 'radio',
        //   title: '您玩游戏的月均消费为？',
        //   description: '单位为人民币',
        //   must: true,
        //   options: [{
        //     id: 1,
        //     title: '0 ~ 100',
        //   }, {
        //     id: 2,
        //     title: '100 ~ 1000',
        //   }, {
        //     id: 3,
        //     title: '1000 ~ 2000',
        //   }, {
        //     id: 4,
        //     title: '2000以上',
        //   }],
        //   row: 0,
        //   score: 0,
        // },
        // {
        //   id: 3,
        //   type: 'radio',
        //   title: '您玩游戏多长时间了？',
        //   description: '',
        //   must: true,
        //   options: [{
        //     id: 1,
        //     title: '0 ~ 1 年',
        //   }, {
        //     id: 2,
        //     title: '1 ~ 5 年',
        //   }, {
        //     id: 3,
        //     title: '5 ~ 10 年',
        //   }, {
        //     id: 4,
        //     title: '10年以上',
        //   }],
        //   row: 0,
        //   score: 0,
        // },
        // {
        //   id: 4,
        //   type: 'text',
        //   title: '您对本游戏的评价如何？',
        //   description: '',
        //   must: false,
        //   options: [{
        //     id: 0,
        //     title: '',
        //   }],
        //   row: 3,
        //   score: 0,
        // },
        // {
        //   id: 5,
        //   type: 'mark',
        //   title: '给本游戏打个分吧~',
        //   description: '',
        //   must: true,
        //   options: [{
        //     id: 0,
        //     title: '',
        //   }],
        //   row: 0,
        //   score: 10,
        // },
      ],
    };
  },
  computed: {
    paginatedQuestionnaires() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return this.questionnaires.slice(startIndex, startIndex + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.questionnaires.length / this.itemsPerPage);
    },
    // publishedImagePath() {
    //   return this.isPublished
    //     ? require('../../assets/images/Published.png')
    //     : require('../../assets/images/Unpublished.png');
    // }
  },
  created() {
    // 假设从后端获取问卷实例数据的方法为 fetchQuestionnaires()
    this.fetchQuestionnaires();
    // this.updateTypetoNormal = this.updateTypetoNormal.bind(this);
    // this.updateTypetoTest = this.updateTypetoTest.bind(this);
    // this.search = this.search.bind(this);
  },

  methods: {
    VindexToRindex(index) {
      return (this.currentPage - 1) * this.itemsPerPage + index;
    },
    deleteqn(index) {
      let qns = this.questionnaires;
      qns.splice(index, 1);
    },
    search() {
      //这里是添加搜索方法的
      this.fetchQuestionnaires();

      console.log("Searching...");
    },
    updateSort1() {
      if (this.ascendingChecked) {
        this.ascendingChecked = false;
      }
      else {
        this.ascendingChecked = true;
        if (this.descendingChecked) {
          this.descendingChecked = false;
        }
      }
      if (this.ascendingChecked) {
        this.sortQuestionnairesAscending();
      }
      else if (this.descendingChecked) {
        this.sortQuestionnairesDescending();
      }
      else {
        this.restoreDefaultSort();
      }
    },
    updateSort2() {
      if (this.descendingChecked) {
        this.descendingChecked = false;
      }
      else {
        this.descendingChecked = true;
        if (this.ascendingChecked) {
          this.ascendingChecked = false;
        }
      }
      if (this.ascendingChecked) {
        this.sortQuestionnairesAscending();
      }
      else if (this.descendingChecked) {
        this.sortQuestionnairesDescending();
      }
      else {
        this.restoreDefaultSort();
      }
    },
    updateRealease1() {
      if (this.realeaseChecked) {
        this.realeaseChecked = false;
      }
      else {
        this.realeaseChecked = true;
        this.notRealeaseChecked = false;
        this.isAll = false;
        console.log('run');
      }
      this.$nextTick(() => {
        this.fetchQuestionnaires();
      });
    },
    updateRealease2() {
      if (this.notRealeaseChecked) {
        this.notRealeaseChecked = false;
      }
      else {
        this.notRealeaseChecked = true;
        this.realeaseChecked = false;
        this.isAll = false;
      }
      this.$nextTick(() => {
        this.fetchQuestionnaires();
      });
    },
    updateTypetoNormal() {
      console.log("before update:", this.isNormal);
      if (this.isNormal) {
        this.isNormal = false;
      }
      else {
        this.isNormal = true;
        this.isApplication = false;
        this.isTest = false;
        this.isVote = false;
        this.isAll = false;
      }
      this.$nextTick(() => {
        this.fetchQuestionnaires();
      });
    },
    updateTypetoVote() {
      if (this.isVote) {
        this.isVote = false;
      }
      else {
        this.isVote = true;
        this.isNormal = false;
        this.isApplication = false;
        this.isTest = false;
        this.isAll = false;
      }
      this.$nextTick(() => {
        this.fetchQuestionnaires();
      });
    },
    updateTypetoApplication() {
      if (this.isApplication) {
        this.isApplication = false;
      }
      else {
        this.isApplication = true;
        this.isNormal = false;
        this.isTest = false;
        this.isVote = false;
        this.isAll = false;
      }
      this.$nextTick(() => {
        this.fetchQuestionnaires();
      });
    },
    updateTypetoTest() {
      if (this.isTest) {
        this.isTest = false;
      }
      else {
        this.isTest = true;
        this.isNormal = false;
        this.isApplication = false;
        this.isVote = false;
        this.isAll = false;
      }
      this.$nextTick(() => {
        this.fetchQuestionnaires();
      });
    },
    updateTypetoAll() {
      if (this.isAll) {
        this.isAll = false;
      }
      else {
        this.isAll = true;
        this.isNormal = false;
        this.isApplication = false;
        this.isVote = false;
        this.isTest = false;
        this.notRealeaseChecked = false;
        this.realeaseChecked = false;
      }
      this.$nextTick(() => {
        this.fetchQuestionnaires();
      });
    },
    fetchQuestionnaires() {
      // 假设从后端获取问卷实例数据的过程
      console.log(this);
      console.log(this.isNormal);
      const formData = new FormData();
      // formData.append("survey_keyword", this.loginForm.user);
      formData.append("is_released", 0);
      if (this.realeaseChecked == true)
        formData.append("is_released", 1);
      if (this.notRealeaseChecked == true)
        formData.append("is_released", 2);
      // else

      console.log(this.realeaseChecked);
      console.log("normal:");
      console.log(this.isNormal);
      console.log("vote:");
      console.log(this.isVote);

      if (this.isNormal)
        formData.append("survey_type", '1');
      if (this.isVote)
        formData.append("survey_type", '2');
      if (this.isTest)
        formData.append("survey_type", '3');
      if (this.isApplication)
        formData.append("survey_type", '4');


      if (this.keyword)
        formData.append("survey_keyword", this.keyword);
      console.log("formdata structed");
      this.$axios({
        method: 'post',
        url: '/survey/api/list',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            this.questionnaires = JSON.parse(res.data.data);
            console.log(this.questionnaires);
            for (var i = 0; i < this.questionnaires.length; i++) {
              this.questionnaires[i].previewVisible = false;
              this.questionnaires[i].publishDialogVisible = false;
              if (this.questionnaires[i].questionType == '1')
                this.questionnaires[i].questionType = '普通问卷'
              else if (this.questionnaires[i].questionType == '2')
                this.questionnaires[i].questionType = '投票问卷'
              else if (this.questionnaires[i].questionType == '3')
                this.questionnaires[i].questionType = '考试问卷'
              else
                this.questionnaires[i].questionType = '报名问卷'
            }
            console.log("success on fetching questionnaires");
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
      // this.questionnaires = [
      //   {
      //     questionnaireName: '问卷1',
      //     questionnaireId: '123',
      //     id: 1,
      //     isPublished: true,
      //     questionType: '普通问卷',
      //     answersCount: 50,
      //     creationDate: '2024-05-20',
      //     isFavorited: true,
      //     isPaused: true,
      //     isEditing: false,
      //   },
      //   {
      //     questionnaireName: '问卷2',
      //     questionnaireId: '456',
      //     id: 2,
      //     isPublished: false,
      //     questionType: '考试问卷',
      //     answersCount: 30,
      //     creationDate: '2024-05-21',
      //     isFavorited: false,
      //     isPaused: false,
      //     isEditing: false,
      //   },
      //   {
      //     questionnaireName: '问卷3',
      //     questionnaireId: '789',
      //     isPublished: false,
      //     id: 3,
      //     questionType: '投票问卷',
      //     answersCount: 50,
      //     creationDate: '2024-05-22',
      //     isFavorited: true,
      //     isPaused: false,
      //     isEditing: false,
      //   },
      //   {
      //     questionnaireName: '问卷4',
      //     questionnaireId: '789',
      //     isPublished: false,
      //     id: 4,
      //     questionType: '报名问卷',
      //     answersCount: 50,
      //     creationDate: '2024-05-23',
      //     isFavorited: true,
      //     isPaused: false,
      //     isEditing: false,
      //   },
      //   {
      //     questionnaireName: '问卷5',
      //     questionnaireId: '789',
      //     isPublished: false,
      //     id: 5,
      //     questionType: '其他问卷',
      //     answersCount: 50,
      //     creationDate: '2024-05-24',
      //     isFavorited: true,
      //     isPaused: false,
      //     isEditing: false,
      //   },
      //   {
      //     questionnaireName: '问卷6',
      //     questionnaireId: '789',
      //     id: 6,
      //     isPublished: false,
      //     questionType: '其他问卷',
      //     answersCount: 50,
      //     creationDate: '2024-05-25',
      //     isFavorited: true,
      //     isPaused: true,
      //     isEditing: false,
      //   },
      // ];
      // 将（模拟后端）获取的数据赋值给组件的数据属性

    },
    sortQuestionnairesAscending() {
      this.questionnaires.sort((a, b) => {
        return new Date(a.creationDate) - new Date(b.creationDate);
      });
    },

    sortQuestionnairesDescending() {
      this.questionnaires.sort((a, b) => {
        return new Date(b.creationDate) - new Date(a.creationDate);
      });
    },

    restoreDefaultSort() {
      this.questionnaires.sort((a, b) => {
        return new Date(a.creationDate) - new Date(b.creationDate);
      });
    },
    previousPage() {
      console.log(this.currentPage);
      if (this.currentPage > 1) {
        this.currentPage -= 1;
        console.log(this.currentPage);
      }
      console.log(this.currentPage);
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
        console.log(this.currentPage);
      }
      console.log(this.currentPage);
    },

    filterQuestionnaires() {
      // 现在感觉这件事可以全权交给前端了！
      // 根据已发布和未发布状态过滤问卷列表
      // 例如：
      // if (this.realeaseChecked) {
      //   this.filteredQuestionnaires = this.questionnaires.filter(questionnaire => questionnaire.published);
      // } else if (this.notRealeaseChecked) {
      //   this.filteredQuestionnaires = this.questionnaires.filter(questionnaire => !questionnaire.published);
      // } else {
      //   this.filteredQuestionnaires = this.questionnaires;
      // }
      // if(this.realeaseChecked)
      // {

      // }
    },

    publishedImagePath(isPublished) {
      return isPublished
        ? require('../../assets/images/Published.png')
        : require('../../assets/images/Unpublished.png');
    },

    edit(questionaire) {
      // 编辑操作
      console.log(questionaire);
      if (questionaire.questionType == '普通问卷')
        this.$router.push({ name: 'questionaireEdit', params: { qnid: questionaire.questionnaireId } });//跳转到编辑问卷界面，待更改
      else if (questionaire.questionType == '投票问卷')
        this.$router.push({ name: 'questionaireEditVote', params: { qnid: questionaire.questionnaireId } });
      else if (questionaire.questionType == '考试问卷')
        this.$router.push({ name: 'questionaireEditTest', params: { qnid: questionaire.questionnaireId } });
      else
        this.$router.push('/questionaireEdit');//跳转到编辑问卷界面，待更改
    },
    preview(questionaire) {
      const formData = new FormData();
      formData.append('survey_id', questionaire.questionnaireId);
      this.$axios({
        method: 'post',
        url: '/question/api/listquestionforpreview',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            this.title = res.data.title;
            this.description = res.data.description;
            this.questions = JSON.parse(res.data.data);
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
      // this.questions = questionaire.questionnaireId;
      questionaire.previewVisible = true;
    },
    share(questionnaire) {
      // 分享操作
      const formData = new FormData();
      formData.append('survey_id', questionnaire.questionnaireId);
      this.$axios({
        method: 'post',
        url: '/survey/api/link',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            this.linkShare = 'http://localhost:8080' + '/fillQnmytest/' + res.data.code;
            questionnaire.publishDialogVisible = true;
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
            // console.log(this.title);
            // console.log(this.description);
            // console.log(this.questions);
            // console.log("success on fetching questions");
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
            this.$message({
                    type: 'info',
                    message: '问卷尚未发布'
                });
            break;
          case -1:
            break;
        }
      }).catch(err => {
        console.log(err);
      });
    },
    statistics(questionnaire) {
      // 统计操作
      this.$router.push({ name: 'questionaireDataview', params: { qnid: questionnaire.questionnaireId } });
    },
    CrossAnalysis(questionnaire){
      this.$router.push({ name: 'testAnalysis', params: { qnid: questionnaire.questionnaireId } });
    },
    clear(questionnaire) {
      ElMessageBox.confirm(
        '这将清空当前问卷的所有答卷数据，此操作不可撤销。您确定要继续吗？',
        '清空确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(() => {
        questionnaire.answersCount = 0;
        const formData = new FormData();
        formData.append('survey_id', questionnaire.questionnaireId);
        return this.$axios({
          method: 'post',
          url: '/submit/api/clear_survey',
          data: formData,
        });
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            console.log("success on cleaning questionnaire");
            break;
          case 2:
            console.log("error 2");
            break;
          case 3:
            console.log("error 3");
            break;
          case -1:
            break;
        }
      }).catch(err => {
        if (err && err.response) {
          console.log(err);
        } else {
          console.log('清空操作已取消');
        }
      });
    },
    exportData() {
      // 导出操作
    },
    pause(questionnaire) {
      // 暂停操作
      questionnaire.isPaused = !questionnaire.isPaused;
      const formData = new FormData();
      formData.append('survey_id', questionnaire.questionnaireId);
      this.$axios({
        method: 'post',
        url: '/surveymanage/api/openorclosesurvey',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            console.log("success on opening/closing questionnaire");
            break;
          case 2:
            console.log("error 2");
            break;
          case 3:
            console.log("error 3");
            break;
          case -1:
            break;
        }
      }).catch(err => {
        console.log(err);
      });
    },
    copy(questionnaire, index) {
      ElMessageBox.confirm(
        '您确定要复制这个问卷吗？',
        '复制问卷',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'info'
        }
          ).then(() => {
        let qns = this.questionnaires;
        qns.splice(index, 0, qns[index]);
        const formData = new FormData();
        formData.append('survey_id', questionnaire.questionnaireId);
        this.$axios({
          method: 'post',
          url: '/surveymanage/api/duplicatesurvey',
          data: formData,
        }).then(res => {
          switch (res.data.status_code) {
            case 1:
              console.log("success on duplicating questionnaire");
              this.fetchQuestionnaires();
              break;
            case 2:
              console.log("error 2");
              break;
            case 3:
              console.log("error 3");
              break;
            case -1:
              break;
          }
        }).catch(err => {
          console.log(err);
        });
      }).catch(() => {
        console.log('用户取消了复制操作');
      });
    },
    favorite(questionnaire) {
      // 收藏操作
      questionnaire.isFavorited = !questionnaire.isFavorited;
      const formData = new FormData();
      formData.append('survey_id', questionnaire.questionnaireId);
      this.$axios({
        method: 'post',
        url: '/surveymanage/api/collectsurvey',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            console.log("success on collecting/uncollecting questionnaire");
            break;
          case 2:
            console.log("error 2");
            break;
          case 3:
            console.log("error 3");
            break;
          case -1:
            break;
        }
      }).catch(err => {
        console.log(err);
      });
    },
    remove(questionnaire, index) {
      ElMessageBox.confirm(
        '您确定要删除这个问卷吗？可以在回收站中找到被删除的问卷。',
        '删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
        ).then(() => {
        this.deleteqn(index);
        if (!this.paginatedQuestionnaires.length && this.currentPage > 1) {
          this.currentPage--;
        }

        const formData = new FormData();
        formData.append('survey_id', questionnaire.questionnaireId);

        this.$axios({
          method: 'post',
          url: '/surveymanage/api/removetorecycle',
          data: formData,
        }).then(res => {
          switch (res.data.status_code) {
            case 1:
              console.log("success on removing questionnaire");
              break;
            case 2:
              console.log("error 2");
              break;
            case 3:
              console.log("error 3");
              break;
            case -1:
              break;
          }
        }).catch(err => {
          console.error(err);
        });
      }).catch(() => {
        console.log('用户取消了删除操作');
      });
    },

    createSurvey() {
      this.$router.push('/questionaireCreate');
    },
    recycleBin() {
      this.$router.push('/questionaireRecycle');
    },
    historyBin(){
      this.$router.push('/questionaireHistory');
    },
    collectedQuestionnaire() {
      this.$router.push('/questionaireCollect');
    },
  },
}

</script>

<style>
#manage {
  display: flex;
}

.qnentry {
  display: flex;
}

.Instance {
  margin-top: 20px;
}

/* #sidebar {
  width: 20%;
  height: 760px;
  background-color: #757070a0;
  padding: 20px;
  box-sizing: border-box;
  margin-top: 60px;
  position:
    fixed;
} */

.button {
  display: block;
  width: 100%;
  text-align: center;
  padding: 10px;
  margin-bottom: 10px;
  border: none;
  cursor: pointer;
  outline: none;
}

.button:hover {
  border: 1px solid #000;
}

#create-survey {
  background-color: #007bff;
  color: #fff;
  font-weight: bold;
}

#bind-wechat {
  background-color: #28a745;
  color: #fff;
  font-weight: bold;
}

#description {
  margin-top: 250px;
  background-color: white;
  padding: 20px;
}

#description-text {
  margin-bottom: 10px;
}

.dialog {
  text-align: left;
}

.dialog .block-title {
  text-align: left;
  /*border: solid 1px black;*/
  font-size: 16px;
  padding: 20px 10px 10px;
  font-weight: bold;
}

.dialog .block-description {
  text-align: left;
  /*border: solid 1px black;*/
  font-size: 14px;
  padding-top: 5px;
  padding-bottom: 15px;
  padding-left: 10px;
  color: gray;
}

.dialog .block-choice {
  text-align: left;
  /*border: solid 1px black;*/
  font-size: 16px;
  padding: 5px 10px 10px;
}

.toolbar {
  display: flex;
  align-items: center;
  flex-direction: row;
  position: fixed;
  top: -30px;
  left: 12.9%;
  width: 88%;
  box-sizing: border-box;
  padding-top: 10px;
  padding-bottom: 30px;
  margin-top: 15px;
  z-index: 5;
  background-color: #ffffff;
  border-bottom: 1px solid #e0d8d8;
}

.sort-container {
  margin-left: 600px;
  margin-right: -500px;
  margin-top: 100px;
  position: relative;
}

.mytype-container {
  margin-left: 550px;
  margin-right: -500px;
  margin-top: 100px;
  position: relative;
}

.realease-container {
  margin-left: 550px;
  margin-right: -500px;
  margin-top: 100px;
  position: relative;
}

.search-box {
  right: 2%;
  margin-top: 100px;
  position: relative;
}

.sort-container button {
  border: transparent;
}

.mytype-container button {
  border: transparent;
}

.realease-container button {
  border: transparent;
}

#search {
  margin-top: 20px;
  display: flex;
  align-items: center;
}

#content {
  width: 80%;
  padding: 20px;
  box-sizing: border-box;
}

#survey-title {
  font-size: 30px;
  text-align: left;
  font-weight: bold;
  margin-left: 70px;
  margin-right: -100px;
  margin-top: 100px;
  position: fixed;
  /* margin-bottom: 20px; */
}

#search-box button {
  height: 36px;
  margin-left: 420px;
  margin-top: -20px;
  background-color: rgb(0, 167, 250);
  color: white;
  font-weight: bolder;
  position: fixed;
  border-radius: 5px;
}

#search-box input[type="text"] {
  padding: 10px;
  width: 300px;
  margin-left: 100px;
  margin-top: -20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  position: fixed;
}

.sort-options {
  position: absolute;
  font-size: 15px;
  width: 100px;
  display: block;
  top: 100%;
  background-color: #a09595;
  border: 1px solid #ccc;
}

.type-options {
  position: absolute;
  font-size: 15px;
  width: 70px;
  display: block;
  top: 100%;
  background-color: #a09595;
  border: 1px solid #ccc;
}

.realease-options {
  position: absolute;
  font-size: 15px;
  width: 70px;
  display: block;
  top: 100%;
  background-color: #a09595;
  border: 1px solid #ccc;
}

.survey-list-container {
  max-height: 500px;
  overflow-y: auto;
}

.pagination {
  margin-left: 32%;
  margin-bottom: 130px;
  position: relative;
  top: 120px;
}

.questionnaire {
  background-color: #ffffff;
  padding: 40px;
  margin-top: 30px;
  margin-bottom: 30px;
  margin-left: 18%;
  margin-right: -250px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
  position: relative;
  top: 120px;
}

.separator {
  height: 1px;
  background-color: #d3d3d3;
  margin: 25px 0;
}

.questionnaire-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  align-items: center;
  font-size: small;
}

.info-left {
  margin-right: 500px;
  font-size: x-large;
  font-weight: 600;
}

.questionnaire-actions button {
  margin-right: 15px;
  background-color: transparent;
  border: 0px;
  border-radius: 3px;
  padding: 15px 20px;
  transition: background-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.questionnaire-actions button:hover {
  color: rgb(15, 107, 255);
}

.icon {
  width: 15px;
  height: 15px;
  vertical-align: middle;
}

.button-container {
  display: flex;
  justify-content: space-between;
}

.leftPart {
  margin-right: 18%;
}

.rightPart {
}

.leftButton {
  font-size: 15px;
}

.rightButton {
  font-size: 15px;
}

.text-black {
  color: black;
  font-size: 15px;
}

.text-red {
  color: red;
  font-size: 15px;
}

.text-red:hover {
  color: rgb(15, 107, 255);
}

.text-black:hover {
  color: rgb(15, 107, 255);
}

.el-tooltip__trigger:focus-visible {
    outline: unset;
} 
</style>