<template v-slot:footer>
  <div class="create-que">    
    <el-carousel trigger="hover" height="710px" indicator-position="outside" type="card" interval="4000">
      <el-carousel-item v-for="card in carouselCards" :key="card.type">
        <el-card class="box-card">
          <div style="text-align: center;">
            <img class="image" :src="card.imageUrl" :alt="card.title" style="margin-top: 20px" />
          </div>
          <div>
            <h3>{{ card.title }}</h3>
            <p class="describe" style="margin-top: -220px; margin-bottom: 40px;">{{ card.description }}</p>
            <el-button :type="card.buttonType" @click="createSurvey(card.type)" v-if="card.type !== 'more'">立即创建</el-button>
            <el-button v-if="card.type === 'more'" style="visibility: hidden;">占位按钮</el-button>
          </div>
        </el-card>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>
  
  <script>
  import user from "@/storage/user";
  
  export default {
    name: "createQue",
    data() {
      return {
        isHoverSurvey: false,
        isHoverTest: false,
        isHoverForm: false,
        isHoverVote: false,
        isHoverPunch: false,
        dialogVisible :false,
        quesType: 1,
        surveyTitle: "",
        carouselCards: [
          {
            type: 'survey',
            imageUrl: require('@/assets/images/qnCreateInvestigation.png'),
            title: '空白问卷',
            description: '这是一个完全空白的模板，为您提供最大的创造自由。您可以从头开始设计您的问卷，包括选择题型、题目顺序、题目描述和题目内容等，让您的问卷完全符合您的需求。',
            buttonType: 'primary',
          },
          {
            type: 'test',
            imageUrl: require('@/assets/images/qnCreateExam.png'),
            title: '考试问卷',
            description: '专为教育和培训设计的考试问卷模板。易于设置题目和正确答案，支持自动评分功能，让您可以迅速创建在线考试和测验。考试问卷适用于学校、在线课程或企业内部培训。',
            buttonType: 'danger',
          },
          {
            type: 'vote',
            imageUrl: require('@/assets/images/qnCreateVote.png'),
            title: '投票问卷',
            description: '汇集公众或特定群体的意见和偏好，帮助您做出群体决策。适用于社区活动、企业决策和公众事务。提供多种投票选项和即时结果统计和分析功能，让投票过程既公平又高效。',
            buttonType: 'warning',
          },
          {
            type: 'more',
            imageUrl: require('@/assets/images/qnCreateMore.png'),
            title: '更多问卷',
            description: '更多精彩内容正在开发中，敬请期待。我们致力于不断创新，为您提供更多样化、易用的问卷设计体验。未来计划将推出更多功能强大、专业定制的问卷模板。',
            buttonType: 'danger',
          },
          {
            type: 'checkin',
            imageUrl: require('@/assets/images/qnCreateCheckin.png'),
            title: '报名问卷',
            description: '无论是社交活动、工作坊还是大型会议，它都可以帮助您轻松创建报名表。报名问卷支持收集参与者的基本信息、偏好和其他自定义数据，使活动组织工作更加高效。',
            buttonType: 'success',
          },
        ],
      }
    },
    methods: {
      createSurvey(tag) {
        var formData = new FormData();
        const userInfo = user.getters.getUser(user.state());
        console.log(userInfo);
        // formData.append("username", userInfo.user.username);
        formData.append("title", this.surveyTitle);
        formData.append("description", "");

        console.log(userInfo.user.username);
  
        var editUrlName = '';
  
        switch (tag) {
          case 'survey':
            formData.append("type", "1");
            editUrlName = 'questionaireEdit';
            break;
          case 'test':
            console.log("enter here");
            formData.append("type", "3");
            editUrlName = 'questionaireEditTest';
            break;
          case 'vote':
            formData.append("type", "2");
            editUrlName = 'questionaireEditVote';
            break;
          case 'checkin':
            formData.append("type", "4");
            editUrlName = 'questionaireEdit';
            break;
          default:
            formData.append("type", "5");
            editUrlName = 'EditHate';
            break;
        }

        console.log(formData);
  
        this.$axios({
          method: 'post',
          url: '/surveymanage/api/createsurvey',
          data: formData,
        })
        .then(res => {
          switch (res.data.status_code) {
            case 1:
              var surveyId = res.data.survey_id;
              this.$router.push({
                name: editUrlName,
                params: { qnid: surveyId }
              });
              break;
            case 2:
              this.$message.warning("form invalid");
              break;
            default:
              this.$message.error("操作失败！");
              console.log(res.data.status_code);
              break;
          }
        })
        .catch(err => {
          console.log(err);
        })
      },
      create(type) {
        if (type == 'survey') {
          this.$router.push('/questionaireTest');//待修改
        }
        else if (type == 'test') {
          this.$router.push('/questionaireTest');
        }
        else if (type == 'vote') {
          this.$router.push('/questionaireVote');
        }
        else if (type == 'checkin') {
          this.$router.push('/questionaireTest');//待修改
        }
      },
      create1() {
        this.dialogVisible=true;
        this.quesType=1;
      }
    }
  }
  </script>
  
  <style scoped>
  .create-que {
    padding-top: 154px; /* 根据需要调整这个值 */
    height: 79vh;
    background-color: #ffffff;
  }

  .el-carousel {
    height: 79vh;
    width: 70%;
    margin-left: 15%;
    background-color: #ffffff;
  }

  .el-carousel__item h3 {
    font-size: 1.5em; /* 增大标题字体 */
    color: #475669;
    text-align: center;
    margin-bottom: .5em; /* 增加标题下边距 */
    height: 300px;
  }

  .el-card {
    padding: 20px;
    text-align: center;
    border: none; /* 移除卡片的边框 */
    width: 60%; /* 或其他百分比，根据需要调整 */
    margin: auto; 
  }

  .el-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between; /* 垂直方向上均匀分布内容 */
    padding: 20px;
    text-align: center;
    border: none;
    width: 60%;
    margin: auto; 
  }

  .el-card .image {
    height: 50%;
    width: 50%;
    margin-bottom: 15px;
  }

  .el-card .describe {
    font-size: 0.9em; /* 设置描述文字的大小 */
    color: #59678c;
    margin-bottom: 20px; /* 设置描述文字和按钮之间的距离 */
  }

  .el-card .el-button {
    margin-top: 15px; /* 按钮距离卡片内容的顶部距离 */
  }

  .el-card .el-button:hover {
    transform: translateY(-1.5px); /* 当鼠标悬停在按钮上时，让按钮轻微向上移动 */
    box-shadow: 0 4px 12px 0 rgba(0,0,0,.1); /* 为按钮添加悬停效果的阴影 */
  }
  </style>