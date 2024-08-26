<template>
    <div class="questionnaire">
      <!-- 第一行 -->
      <div class="questionnaire-info">
        <div class="info-left">
          <span>{{ questionnaireName }}</span>
        </div>
        <span>id: {{ questionnaireId }}</span>
        <!-- <span>{{ isPublished ? '已发布' : '未发布' }}</span> -->
        <span :class="{'icon-published': isPublished, 'icon-unpublished': !isPublished}" :style="{ color: isPublished ? 'green' : 'red' }">
          <img :src="publishedImagePath" alt="release status" class="icon">
          {{ isPublished ? '已发布' : '未发布' }}
        </span>
        <!-- <span>答卷: {{ answersCount }}</span> -->
        <span>答卷: <span :style="{ color: answersCount > 0 ? 'blue' : '' }">{{ answersCount }}</span></span>
        <span>创建时间：{{ creationDate }}</span>
      </div>
      <!-- 分隔线 -->
      <div class="separator"></div>
      <!-- 第二行按钮 -->
      <div class="questionnaire-actions">
        <div class="button-container">
          <div class="leftPart">
            <button @click="edit" class="leftButton">
              <img src="../../../src/assets/images/Edit.png" alt="edit-icon" class="icon">
              编辑
            </button>

            <button @click="preview" class="leftButton">
              <img src="../../../src/assets/images/Preview.png" alt="preview-icon" class="icon">
              预览
            </button>

            <button @click="share" class="leftButton">
              <img src="../../../src/assets/images/Share.png" alt="share-icon" class="icon">
              分享
            </button>

            <button @click="statistics" class="leftButton">
              <img src="../../../src/assets/images/Stats.png" alt="statistics-icon" class="icon">
              统计
            </button>

            <button @click="clear" class="leftButton">
              <img src="../../../src/assets/images/ClearAll.png" alt="clear-icon" class="icon">
              清空
            </button>

            <button @click="exportData" class="leftButton">
              <img src="../../../src/assets/images/ExportData.png" alt="exportData-icon" class="icon">
              导出
            </button>
          </div>

          <button @click="pause" class="rightButton">
            <img :src="isPaused ? require('../../../src/assets/images/Start.png') : require('../../../src/assets/images/PauseRed.png')" alt="pause-icon" class="icon">
            <span :class="{'text-red': !isPaused, 'text-black': isPaused}">{{ isPaused ? '继续' : '暂停' }}</span>
          </button>

          <button @click="copy" class="rightButton">
            <img src="../../../src/assets/images/Copy.png" alt="copy-icon" class="icon">
            复制
          </button>

          <button @click="favorite" class="rightButton">
            <img :src="isFavorited ? require('../../../src/assets/images/Like.png') : require('../../../src/assets/images/LightLike.png')" alt="favorite-icon" class="icon">
            {{ isFavorited ? '已收藏' : '收藏' }}
          </button>
          
          <button @click="remove" class="rightButton">
            <img src="../../../src/assets/images/Delete.png" alt="remove-icon" class="icon">
            删除
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  // import axios from 'axios';

  export default {
    props: {
      questionnaireName: String,
      questionnaireId: String,
      isPublished: Boolean, 
      answersCount: Number,
      creationDate: String,
      isFavorited: Boolean,
      isPaused: Boolean,
    },
    // data(){
    //   return{
    //     localQuestionnaireName: this.questionnaireName,
    //     localQuestionnaireId: this.questionnaireId,
    //     localIsPublished: this.isPublished,
    //     localAnswersCount: this.answersCount,
    //     localCreationDate: this.creationDate,
    //     localIsFavorited: this.isFavorited,
    //     localIsPaused: this.isPaused,
    //   };
    // },
    methods: {
      edit() {
        // 编辑操作
         //this.questionnaireName = "hhh";
         this.$emit('update:questionaireName',"hhhhh");
        //  console.log(this.questionnaireName);
      },
      preview() {
        // 预览操作
      },
      share() {
        // 分享操作
      },
      statistics() {
        // 统计操作
      },
      clear() {
        // 清空操作
      },
      exportData() {
        // 导出操作
      },
      pause() {
        // 暂停操作
        // this.localIsPaused = !this.localIsPaused;
        // // this.$emit('update',!this.isPaused);
        //this.isPaused = !this.isPaused;
        //this.$emit('update',!this.isPaused);
      },
      copy() {
        // 复制操作
      },
      favorite() {
        // 收藏操作
        this.$emit('update',!this.isFavorited);
      },
      remove() {
        //删除操作
      },
      // updateData() {
      //   // 当你需要通知父组件更新数据库时
      //   this.$emit('update-data', {
      //     questionnaireName: this.localQuestionnaireName,
      //     questionnaireId: this.localQuestionnaireId,
      //     isPublished: this.localIsPublished,
      //     answersCount: this.localAnswersCount,
      //     creationDate: this.localCreationDate,
      //     isFavorited: this.localIsFavorited,
      //     isPaused: this.localIsPaused,
      //   });
      // },
    },
    computed: {
      publishedImagePath() {
        return this.isPublished
          ? require('../../assets/images/Published.png')
          : require('../../assets/images/Unpublished.png');
      }
    },
  };

  </script>

  <style scoped>
  .questionnaire {
    background-color: #ffffff;
    padding: 40px;
    margin-top: 30px;
    margin-bottom: 30px;
    margin-left: 28%;
    margin-right: -320px;
    border-radius: 5px; /* 添加边框圆角 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.05); /* 添加阴影 */
    transition: box-shadow 0.3s ease; /* 添加过渡效果 */
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
    align-items: center; /* 确保内部元素垂直居中 */
    font-size: small;
  }

  .info-left {
    margin-right: 700px;
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
    cursor: pointer; /* 鼠标悬停时变为手形图标 */
  }

  .questionnaire-actions button:hover {
    /*background-color: #cecfd0; /* 当鼠标悬停时改变按钮的背景色 */
    color: rgb(15, 107, 255); /* 当鼠标悬停时改变按钮的文字颜色 */
  }

  .icon {
    width: 15px;
    height: 15px;
    vertical-align: middle;
  }

  .button-container {
    display: flex;
  }

  .leftPart {
    margin-right: 100px;
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
    color: rgb(15, 107, 255); /* 当鼠标悬停时改变按钮的文字颜色 */
  }

  .text-black:hover {
    color: rgb(15, 107, 255); /* 当鼠标悬停时改变按钮的文字颜色 */
  }

  </style>