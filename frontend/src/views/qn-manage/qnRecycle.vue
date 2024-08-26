<template>
  <div class="questionnaire-management">
    <!-- 提示信息：如果用户没有被删除的问卷 -->
    <div v-if="!deletedQuestionnaires.length" class="info-text">
      <p>如果您想释放上传文件题的空间，请点击“清空数据”，数据清空后将无法恢复，请谨慎操作！</p>
      <el-button type="danger" @click="clearRecycleBin">清空回收站</el-button>
      <el-button type="primary" @click="goBack">返回</el-button>
    </div>

    <!-- 提示信息：您还没有删除过的问卷 -->
    <div v-if="!deletedQuestionnaires.length" class="white-board">
      <h3>您还没有删除过的问卷</h3>
    </div>
    
    <!-- 已删除问卷列表 -->
    <div v-else class="white-board">
      <el-button type="primary" @click="goBack">返回</el-button>
      <el-table :data="deletedQuestionnaires" stripe style="width: 50%; margin-left: 25%;" max-height="700">
        <el-table-column prop="name" label="问卷名" width="240px"></el-table-column>
        <el-table-column prop="publishTime" label="发布时间" width="120px"></el-table-column>
        <el-table-column prop="answersCount" label="答卷数" width="120px"></el-table-column>
        <el-table-column label="操作" width="340px">
          <template #default="{ row }">
            <el-button size="small" type="warning" @click="clearData(row.id)">清空数据</el-button>
            <el-button size="small" type="success" @click="restoreQuestionnaire(row.id)">恢复</el-button>
            <el-button size="small" type="danger" @click="deletePermanently(row.id)">彻底删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <p class="red-text">被删除的问卷保留6个月后将被彻底删除，无法再恢复运行！</p>
  </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        deletedQuestionnaires: [
          // 示例已删除问卷数据
          // { id: 1, name: '问卷1', publishTime: '2024-05-01', answersCount: 20 },
          // { id: 2, name: '问卷2', publishTime: '2024-05-10', answersCount: 15 }
        ]
      };
    },
    methods: {
      goBack(){
        this.$router.push('/questionairemanage');
      },
      highlightButton() {
        // 高亮清空回收站按钮
        document.querySelector('.clear-btn').style.fontWeight = 'bold';
        document.querySelector('.clear-btn').style.color = 'blue';
      },
      unhighlightButton() {
        // 取消清空回收站按钮高亮
        document.querySelector('.clear-btn').style.fontWeight = 'normal';
        document.querySelector('.clear-btn').style.color = 'black';
      },
      clearRecycleBin() {
        // 清空回收站操作
        console.log('清空回收站');
      },
      clearData(questionnaireId) {
        // 清空问卷数据操作
        console.log('清空问卷数据，问卷ID：', questionnaireId);
      },
      restoreQuestionnaire(questionnaireId) {
        // 恢复问卷操作
        console.log('恢复问卷，问卷ID：', questionnaireId);
      },
      deletePermanently(questionnaireId) {
        // 彻底删除问卷操作
        console.log('彻底删除问卷，问卷ID：', questionnaireId);
      }
    }
  };
  </script>
  
  <style scoped>
  /* 样式 */
  .questionnaire-management{
    padding-top: 4%;
  }
  .blue-text {
    color: blue;
  }
  
  .red-text {
    color: red;
  }
  
  .white-board {
    background-color: white;
    padding: 20px;
    margin-top: 20px;
    width:50%;
    margin-left: 23%;
  }
  </style>