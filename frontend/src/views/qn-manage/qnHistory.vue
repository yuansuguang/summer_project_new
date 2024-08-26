<template>
  <div class="history-management">
    <el-button type="primary" @click="goBack" style="margin-bottom: 1%;">返回</el-button>
    
    <div v-if="!favoriteQuestionnaires.length" class="white-board">
      <h3>您还没有填写过的问卷</h3>
    </div>
    
    <div v-else class="white-board">
      <el-table :data="favoriteQuestionnaires" stripe style="width: 50%; margin-left: 25%;" max-height="700">
        <el-table-column prop="questionnaireName" label="问卷名" width="200px"></el-table-column>
        <el-table-column prop="creationDate" label="上次填写时间" width="200px"></el-table-column>
        <el-table-column label="操作" width="500px">
          <template #default="{ row }">
            <el-button size="small" type="success" @click="continueWrite(row)">继续填写</el-button>
            <el-button size="small" type="danger" @click="removeFromFavorites(row)">删除记录</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        favoriteQuestionnaires: [
        {
            questionnaireName: '问卷1',
            questionnaireId: '123',
            submitId:1,
            isPublished: true,
            questionType: '普通问卷',
            answersCount: 50,
            creationDate: '2024-05-20',
            isSubmitted: true,
            isPaused: true,
            isEditing: false,
            code: '',
          },
          {
            questionnaireName: '问卷2',
            questionnaireId: '456',
            submitId:2,
            isPublished: false,
            questionType: '考试问卷',
            answersCount: 30,
            creationDate: '2024-05-21',
            isSubmitted: false,
            isPaused: false,
            isEditing: false,
            code: '',
          },
          {
            questionnaireName: '问卷3',
            questionnaireId: '789',
            isPublished: false,
            submitId:3,
            questionType: '投票问卷',
            answersCount: 50,
            creationDate: '2024-05-22',
            isSubmitted: true,
            isPaused: false,
            isEditing: false,
            code: '',
          },
          {
            questionnaireName: '问卷4',
            questionnaireId: '789',
            isPublished: false,
            submitId:4,
            questionType: '报名问卷',
            answersCount: 50,
            creationDate: '2024-05-23',
            isSubmitted: true,
            isPaused: false,
            isEditing: false,
            code: '',
          },
          {
            questionnaireName: '问卷5',
            questionnaireId: '789',
            isPublished: false,
            submitId:5,
            questionType: '其他问卷',
            answersCount: 50,
            creationDate: '2024-05-24',
            isSubmitted: true,
            isPaused: false,
            isEditing: false,
            code: '',
          },
          {
            questionnaireName: '问卷6',
            questionnaireId: '789',
            id:6,
            isPublished: false,
            questionType: '其他问卷',
            answersCount: 50,
            creationDate: '2024-05-25',
            isSubmitted: true,
            isPaused: true,
            isEditing: false,
            code: '',
          },
        ]
      };
    },
    methods: {
      goBack(){
        this.$router.push('/questionairemanage');
      },
      viewData(questionnaire){
        console.log(questionnaire.questionType);
      },
      clearData(questionnaire) {
        // 清空问卷数据操作
        // questionnaire.answersCount = 0;
        const formData = new FormData();
        formData.append('survey_id', questionnaire.questionnaireId);
        this.$axios({
        method: 'post',
        url: '/submit/api/clear_survey',
        data: formData,
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
        console.log(err);
      });
      this.fetchFavorite();
      },
      removeFromFavorites(questionnaire) {
        // 取消收藏操作
        const formData = new FormData();
        formData.append('submit_id', questionnaire.submitId);
      this.$axios({
        method: 'post',
        url: '/submit/api/delete_submission',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            console.log("success on deleting submission");
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
      this.fetchFavorite();
      },
      continueWrite(questionnaire) {
        if (questionnaire.type == '3') {
          this.$router.push({ name: 'fillQnmytest', params: { code: questionnaire.code } });
        }
        else if (questionnaire.type == '2') {
          this.$router.push({ name: 'fillQnmyvote', params: { code: questionnaire.code } });
        }
        else {
          this.$router.push({ name: 'fillQn', params: { code: questionnaire.code } });
        }
      },
      fetchHistory() {
        this.$axios({
        method: 'get',
        url: '/submit/api/get_user_submissions',
          }).then(res => {
            switch (res.data.status_code) {
              case 1:
                this.favoriteQuestionnaires = JSON.parse(res.data.data);
                console.log(this.favoriteQuestionnaires);
                console.log("success on fetching history");
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
      fetchFavorite() {
        const formData = new FormData();
      // formData.append("survey_keyword", this.loginForm.user);
      // if (this.notRealeaseChecked == true)
      //   formData.append("is_released", 1);
      // else if (this.notRealeaseChecked == false)
      //   formData.append("is_released", 2);
      // else
      formData.append("is_collected", 1);
      formData.append("is_released", 0);
      this.$axios({
        method: 'post',
        url: '/survey/api/list',
        data: formData,
      }).then(res => {
        switch (res.data.status_code) {
          case 1:
            this.favoriteQuestionnaires = JSON.parse(res.data.data);
            console.log(this.favoriteQuestionnaires);
            // for (var i = 0; i < this.questionnaires.length; i++) {
            //   this.questionnaires[i].previewVisible = false;
            //   if (this.questionnaires[i].questionType == '1')
            //     this.questionnaires[i].questionType = '普通问卷'
            //   else if (this.questionnaires[i].questionType == '2')
            //     this.questionnaires[i].questionType = '投票问卷'
            //   else if (this.questionnaires[i].questionType == '3')
            //     this.questionnaires[i].questionType = '考试问卷'
            //   else
            //     this.questionnaires[i].questionType = '报名问卷'
            // }
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
      },
    },
    created() {
    // 假设从后端获取问卷实例数据的方法为 fetchQuestionnaires()
    this.fetchHistory();
  },
  };
  </script>

  <style scoped>
  .history-management {
    padding-top: 6%;
  }
  </style>