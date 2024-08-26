<template>
    <div class="questionnaire-square">
      <h2 class="title">问卷广场</h2>
      <el-select v-model="selectedCategory" placeholder="选择分类" @change="filterQuestionnaires" class="category-select">
        <el-option v-for="category in categories" :key="category.value" :label="category.label" :value="category.value"></el-option>
      </el-select>
  
      <div class="questions-container">
        <el-row :gutter="20">
          <el-col :span="24" :md="8" v-for="questionnaire in paginatedQuestionnaires" :key="questionnaire.id">
            <el-card :body-style="{ padding: '20px' }" class="questionnaire-card">
                <h4>{{ questionnaire.title }}</h4>
                <div class="content">{{ questionnaire.description }}</div>
                <div class="card-buttons">
                    <el-button type="primary" @click="redirectToDetails(questionnaire.id)">查看详情</el-button>
                    <el-button type="success" @click="addToMyQuestionnaires(questionnaire)">添加到我的问卷</el-button>
                </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
  
      <el-pagination @current-change="handlePageChange" :current-page="currentPage" :page-size="pageSize" :total="filteredQuestionnaires.length" layout="prev, pager, next" class="pagination"></el-pagination>
    </div>
  </template>

<script>

export default {
    data() {
    return {
        searchQuery: '',
        selectedCategory: '',
        currentPage: 1,
        pageSize: 9,
        categories: [
            { value: 'technology', label: '科技' },
            { value: 'education', label: '教育' },
            { value: 'entertainment', label: '娱乐' },
            { value: 'work', label: '工作' },
            { value: 'health', label: '健康' },
            { value: 'other', label: '其他' },
            { value: 'public', label: '公众' },
            { value: '', label: '全部' },
        ],
        // 假设这里是从后端获取的问卷列表数据
        questionnaires: [
            {
                id: 1,
                title: "禁毒日禁毒知识测试",
                description: "本测试针对禁毒知识测试，共20道题，满分100分。",
                category: 'health',
            },
            {
                id: 2,
                title: "大学生恋爱观调查",
                description: "此项调查旨在了解大学生的恋爱观。",
                category: 'education',
            },
            {
                id: 3,
                title: "游戏满意度问卷",
                description: "我们非常重视每位用户的宝贵意见，期待您的参与。",
                category: 'entertainment',
            },
            {
                id: 4,
                title: "学生居家在线学习调查",
                description: "更好地服务广大学生的居家在线学习生活。",
                category: 'education',
            },
            {
                id: 5,
                title: "老年人简短营养状况问卷",
                description: "帮助医务人员识别营养不良以及早期干预需要。",
                category: 'health',
            },
            {
                id: 6,
                title: "消费市场调查问卷",
                description: "了解消费者市场动态和消费者需求。",
                category: 'other',
            },
            {
                id: 7,
                title: "宠物护理知识测试",
                description: "了解你对宠物护理的了解程度。",
                category: 'health',
            },
            {
                id: 8,
                title: "环境保护行动参与度调查",
                description: "了解人们在环境保护行动中的参与程度。",
                category: 'public',
            },
            {
                id: 9,
                title: "个人理财习惯问卷",
                description: "收集大众的理财习惯，为理财产品提供参考。",
                category: 'other',
            },
            {
                id: 10,
                title: "城市公共设施满意度调查",
                description: "收集市民对城市公共设施的满意度。",
                category: 'public',
            },
            {
                id: 11,
                title: "电影观赏偏好调查",
                description: "了解大众的电影观赏偏好。",
                category: 'entertainment',
            },
            {
                id: 12,
                title: "网络安全意识调查",
                description: "了解公众的网络安全意识和习惯。",
                category: 'technology',
            },
            {
                id: 13,
                title: "健康饮食习惯问卷",
                description: "了解人们的饮食习惯对健康的影响。",
                category: 'health',
            },
            {
                id: 14,
                title: "员工工作满意度调查",
                description: "评估员工对工作的满意度和改进意见。",
                category: 'work',
            },
            {
                id: 15,
                title: "旅游目的地偏好调查",
                description: "了解旅游者对旅游目的地的偏好。",
                category: 'entertainment',
            },
            {
                id: 16,
                title: "社区服务需求调查",
                description: "了解社区居民对社区服务的需求。",
                category: 'other',
            },
            {
                id: 17,
                title: "学习资源使用情况调查",
                description: "了解学生对学习资源的使用情况。",
                category: 'education',
            },
            {
                id: 18,
                title: "体育活动参与度调查",
                description: "了解人们参与体育活动的程度。",
                category: 'entertainment',
            },
            {
                id: 19,
                title: "社交媒体使用习惯调查",
                description: "了解社交媒体的使用习惯和对社交的影响。",
                category: 'entertainment',
            },
            {
                id: 20,
                title: "城市交通状况满意度调查",
                description: "您的意见将帮助市政部门改善交通状况。",
                category: 'public',
            }
            ]
        };
    },
    computed: {
        filteredQuestionnaires() {
            return this.questionnaires.filter(qn => {
                return qn.title.toLowerCase().includes(this.searchQuery.toLowerCase()) &&
                (this.selectedCategory === '' || qn.category === this.selectedCategory);
            });
        },
        paginatedQuestionnaires() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.filteredQuestionnaires.slice(start, end);
        },
    },
    methods: {
        handlePageChange(newPage) {
            this.currentPage = newPage;
        },
        redirectToDetails(id) {
            if (id) {
                this.$router.push('/questionnaireSquareTest');
            }
        }
    },
};
</script>

<style scoped>
.questionnaire-square {
  padding: 20px;
  padding-top: 5%;
}

.questions-container {
  margin: 0 auto;
  max-width: 1280px; /* 或者根据你的设计来 */
}

.questionnaire-card {
  margin-bottom: 20px;
  height: 180px; /* 如果内容高度不一，可以设置为 auto，以避免内容被截断 */
}

.pagination {
  margin: 20px auto;
  width: fit-content;
}

.category-select {
  display: block;
  margin: 20px auto;
  width: 20%;
}

@media (max-width: 768px) {
  .questionnaire-square {
    padding: 10px;
  }

  .questions-container {
    max-width: 100%;
  }

  .el-col {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

.questionnaire-card {
  position: relative;
}

.card-buttons {
  display: none;
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
}

.questionnaire-card:hover .card-buttons {
  display: block;
}
</style>