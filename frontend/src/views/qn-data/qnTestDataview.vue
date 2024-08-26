<template>
    <div class="common-layout">
      <el-container>
        <el-header></el-header>
        <el-main>
          <div class="mytable">
            <h2>考试统计</h2>

            <!-- 问题描述显示 -->
            <div v-if="currentQuestion" class="question-description" style="margin-top: -60px;">
                <h3>{{ currentQuestionDescription }}</h3>
            </div>

            <el-table :data="options" style="width: 50%" height="250" stripe fit size="large">
              <el-table-column fixed prop="name" label="选项" />
              <el-table-column prop="count" label="选择人数" />
              <el-table-column label="占比" >
                <template #default="scope">
                  <el-progress :percentage="parseFloat(scope.row.percentage)" /> <!-- 注意：将占比转换成数值类型 -->
                </template>              
              </el-table-column>
            </el-table>
  
            <!-- <div style="margin-top: 0px; margin-bottom: -30px; display: flex; justify-content: space-around; align-items: center; width: 50%;">
              <div>本题正确率:</div>
              <div style="flex-shrink: 0; margin-right: 10px;">{{ Math.round(correctRate) }} 人正确</div>
              <el-progress :percentage="correctRate" style="width: 100%; max-width: 300px;"></el-progress>
            </div> -->
  
            <!-- 图表展示按钮 -->
            <div class="chart-buttons">
              <!-- 添加一个下拉菜单选择要查看的问题 -->
              <el-select v-model="currentQuestion" placeholder="请选择一个问题">
                <el-option
                    v-for="(question, index) in questions"
                    :key="question.id"
                    :label="`问题 ${index + 1}`"
                    :value="question.id">
                </el-option>
                </el-select>
                <el-button type="primary" @click="toggleChart('bar')">柱状图</el-button>
                <el-button type="primary" @click="toggleChart('line')">折线图</el-button>
                <el-button type="primary" @click="toggleChart('pie')">饼状图</el-button>
                <el-button type="primary" @click="exportToExcel">导出为 Excel</el-button>
                <el-button type="primary" @click="exportToWordAndPDF">导出为 PDF</el-button>
            </div>
  
            <!-- 图表展示区域 -->
            <div id="export-content" v-if="showChart" class="chart-container">
              <canvas ref="chartCanvas"></canvas>
            </div>
  
          </div>
        </el-main>
      </el-container>
    </div>
    
  </template>
  
  <script >
  import Chart from 'chart.js/auto';
  import * as XLSX from 'xlsx';
  import html2canvas from 'html2canvas';
  import jsPDF from 'jspdf';
  import 'element-plus/dist/index.css';
  
  export default {
    props: {
      correctAnswer: { // 接收正确答案
        type: String,
        default: ''
      }
    },
    data() {
      return {
        currentQuestion: '', // 当前被选中查看的问题ID
        allquestions: [],
        questions: [], // 存储问卷的所有问题
        options: [], // 当前问题的选项统计数据
        showChart: false,
        chartType: '',
        chartData: null,
        chartLabels: [], // 图表标签
        correctRate: 0,
        // 其他数据...
      };
    },
    computed: {
        currentQuestionDescription() {
        // 在问题列表中找到当前选中的问题并返回其描述
            const currentQuestion = this.questions.find(question => question.id === this.currentQuestion);
            return currentQuestion ? currentQuestion.description : '';
        }
    },
    mounted() {
        // 在组件挂载后，初始化问题数据
        this.initQuestionsData();
    },
    watch: {
      // 监听当前选定问题的变化，以更新相关的图表和统计信息
      currentQuestion(newValue, oldValue) {
        if(newValue !== oldValue) {
          this.updateCurrentQuestionStatistics(newValue);
        }
      }
    },
    methods: {
        initQuestionsData() {
          const formData = new FormData();
          formData.append('survey_id', this.$route.params.qnid);
          this.$axios({
                method: 'post',
                url: '/question/api/listquestionforanalysis',
                data: formData,
            }).then(res => {
                switch (res.data.status_code) {
                case 1:
                    this.allquestions = JSON.parse(res.data.data);
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
                    console.log(this.allquestions);
                    console.log(this.allquestions.length);
                    console.log("success on fetching questions");
                    for (let i = 0; i < this.allquestions.length; i++) {
                      const question = this.allquestions[i];
                      console.log(question.id, question.description);
                      var param = {
                            question_id: question.question_id,
                        };
                        this.$axios({
                          method: 'post',
                          url: '/submit/api/get_question_statistics',
                          data: param,
                      }).then(res => {
                          switch (res.data.status_code) {
                          case 1:
                              this.options = res.data.statistics;
                              this.questions.push({
                                id: question.question_id,
                                description: question.description,
                                options: this.options,
                                correctAnswer: question.refer
                              })
                              for (var i = 0; i < this.questionnaires.length; i++) {
                              if (this.questionnaires[i].questionType == '1')
                                  this.questionnaires[i].questionType = '普通问卷'
                              else if (this.questionnaires[i].questionType == '2')
                                  this.questionnaires[i].questionType = '投票问卷'
                              else if (this.questionnaires[i].questionType == '3')
                                  this.questionnaires[i].questionType = '考试问卷'
                              else
                                  this.questionnaires[i].questionType = '报名问卷'
                              }
                              console.log(this.questions);
                              console.log("success on getting statistics");
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
                              console.log(res.data.status_code);
                              break;
                          }
                      }).catch(err => {
                          console.log(err);
                      });
                    }
                    console.log("checkpoint 2");
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
            console.log("checkpoint 2");
            console.log(this.allquestions);
            console.log(this.allquestions.length);
              
            // for (let i = 0; i < this.allquestions.length; i++) {
            //   const question = this.allquestions[i];
            //   console.log(question.id, question.description);
            //   var param = {
            //         question_id: question.question_id,
            //     };
            //     this.$axios({
            //       method: 'post',
            //       url: '/submit/api/get_submission',
            //       data: param,
            //   }).then(res => {
            //       switch (res.data.status_code) {
            //       case 1:
            //           this.options = res.data.statistics;
            //           this.questions.push({
            //             id: question.question_id,
            //             description: question.description,
            //             options: this.options,
            //             correctAnswer: question.refer
            //           })
            //           // for (var i = 0; i < this.questionnaires.length; i++) {
            //           // if (this.questionnaires[i].questionType == '1')
            //           //     this.questionnaires[i].questionType = '普通问卷'
            //           // else if (this.questionnaires[i].questionType == '2')
            //           //     this.questionnaires[i].questionType = '投票问卷'
            //           // else if (this.questionnaires[i].questionType == '3')
            //           //     this.questionnaires[i].questionType = '考试问卷'
            //           // else
            //           //     this.questionnaires[i].questionType = '报名问卷'
            //           // }
            //           console.log(this.allquestions);
            //           console.log("success on fetching questions");
            //           break;
            //       case 2:
            //           console.log("error 2");
            //           break;
            //       case 3:
            //           console.log("error 3");
            //           break;
            //       case 4:
            //           console.log("error 4");
            //           break;
            //       case 5:
            //           console.log("error 5");
            //           break;
            //       case -1:
            //           console.log(res.data.status_code);
            //           break;
            //       }
            //   }).catch(err => {
            //       console.log(err);
            //   });
            // }
            // console.log("checkpoint 2");
            // this.questions = [
            // {
            //     id: 'q1',
            //     description: '问题1：JavaScript是一种______语言。',
            //     options: [
            //     { id: 'q1o1', name: '编译型', count: 20 },
            //     { id: 'q1o2', name: '解释型', count: 180 },
            //     { id: 'q1o3', name: '汇编语言', count: 5 },
            //     { id: 'q1o4', name: '标记语言', count: 15 }
            //     ],
            //     correctAnswer: 'q1o2'
            // },
            // {
            //     id: 'q2',
            //     description: '问题2：下列哪个是Vue.js的核心特性？',
            //     options: [
            //     { id: 'q2o1', name: '虚拟DOM', count: 150 },
            //     { id: 'q2o2', name: '组件', count: 140 },
            //     { id: 'q2o3', name: '响应式', count: 160 },
            //     { id: 'q2o4', name: '以上都是', count: 100 }
            //     ],
            //     correctAnswer: 'q2o4'
            // }
            // // 可以根据需要添加更多的问题
            // ];
            // this.questions.push({
            //   id: 'q3',
            //   description: '问题3：Vue.js的生命周期钩子包括哪些？',
            //   options: [
            //     { id: 'q3o1', name: 'created', count: 100 },
            //     { id: 'q3o2', name: 'mounted', count: 120 },
            //     { id: 'q3o3', name: 'updated', count: 80 },
            //     { id: 'q3o4', name: '以上都是', count: 200 }
            //   ],
            //   correctAnswer: 'q3o4'
            // });
            // 默认选中第一个问题进行展示
            if(this.questions.length > 0) {
            this.currentQuestion = this.questions[0].id;
            this.updateCurrentQuestionStatistics(this.currentQuestion);
            }
        },
        updateCurrentQuestionStatistics(questionId) {
            // 根据当前选中的问题ID更新选项统计数据和正确率
            const currentQuestion = this.questions.find(q => q.id === questionId);
            if(currentQuestion) {
                this.options = this.calculatePercentage(currentQuestion.options);
                this.calculateCorrectRate(); 
                // 确保你更新了showChart、chartType等变量后调用了generateChart
                this.showChart = true; // 举一个例子
                // 之后可以添加generateChart的调用，如果需要
            }
            },
        // 保留其他方法...
        exportToExcel() {
            const tableData = this.getTableData(); // 获取表格数据
            const wb = XLSX.utils.book_new();
            const ws = XLSX.utils.json_to_sheet(tableData);
            XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
            XLSX.writeFile(wb, 'table_data.xlsx');
        },
        getTableData() {
            const tableData = this.options.map(option => ({
            name: option.name,
            count: option.count,
            percentage: option.percentage,
            }));
            tableData.push({ name: '本题正确率', count: this.correctRate, percentage: this.correctRate });
            return tableData;
        },
        exportToPDF() {
            const exportContent = document.getElementById('export-content');
            if (!exportContent) {
            console.error('未找到需要导出的内容');
            return;
            }
            html2canvas(exportContent).then(canvas => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jsPDF();
            // 获取画布的宽度和高度，并以此为基础设置PDF中图片的尺寸
            const imgProps = pdf.getImageProperties(imgData);
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
            
            // 将图片添加到PDF中，并保持比例
            pdf.addImage(imgData, 'PNG', 10, 10, pdfWidth - 20, pdfHeight); // 减去20是为了确保图片两侧有边距
            pdf.save('table_and_chart.pdf');
            }).catch(error => {
            console.error('导出PDF时发生错误:', error);
            });
        },
        getData() {
            // 获取后端数据的方法
            return [{ name: '选项1', count: 10 }, { name: '选项2', count: 15 }, { name: '选项3', count: 300 }, { name: '选项4', count: 8 }, { name: '选项5', count: 10 }];
        },
        calculatePercentage(data) {
            // 计算占比
            const total = data.reduce((sum, option) => sum + option.count, 0);
            return data.map(option => ({
            ...option,
            percentage: ((option.count / total) * 100).toFixed(2)
            }));
        },
        calculateCorrectRate() {
            // 计算本题正确率
            const totalResponses = this.options.reduce((sum, option) => sum + option.count, 0);
            const correctResponses = this.options.find(option => option.name === this.correctAnswer)?.count || 0;
            this.correctRate = ((correctResponses / totalResponses) * 100).toFixed(2);
        },
        toggleChart(type) {
            if (this.chartType === type) {
            // 如果当前已经显示该类型的图表，则收起图表
                this.showChart = false;
                this.chartType = '';
                // 销毁当前的图表实例
                if (this.chartData) {
                    this.chartData.destroy();
                    this.chartData = null;
                }
            } else {
                console.log('切换图表类型', type);
                // 否则，显示对应类型的图表
                this.showChart = true;
                this.chartType = type;
                this.$nextTick(() => {
                    this.generateChart(type);
                });
            }
        },
        generateChart(chartType) {
            // 确保chartType有效且showChart为true
            if (!chartType || !this.showChart) {
                return;
            }

            // 现在不需要以下代码，因为我们将使用传入的chartType参数
            // if (this.chartType === type) {
            //   // 如果当前已经显示该类型的图表，则收起图表
            //   this.showChart = false;
            //   …

            if (this.chartData) {
                // 销毁当前图表实例
                this.chartData.destroy();
                this.chartData = null;
            }

            const ctx = this.$refs.chartCanvas.getContext('2d');
            const labels = this.options.map(option => option.name);
            const percentages = this.options.map(option => parseFloat(option.percentage));

            // 使用数据数量来确定背景色和边框色数组的大小
            const colors = this.generateColors(labels.length);

            const data = {
                labels,
                datasets: [{
                label: '占比',
                data: percentages,
                backgroundColor: colors.background,
                borderColor: colors.border,
                borderWidth: 1
                }]
            };

            const options = {
                scales: {
                y: {
                    beginAtZero: true
                }
                }
            };

            // 只有在确实需要时才创建新的图表实例
            if (ctx) {
                this.chartData = new Chart(ctx, {
                type: chartType,
                data,
                options
                });
            }
        },
        
        // 添加新方法用于生成颜色数组
        generateColors(numOptions) {
            const baseColors = [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 80, 192, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 255, 192, 0.2)',
            'rgba(130, 20, 255, 0.2)',
            ];
    
            // 循环生成颜色数组，如果选项数量超过预定义颜色数量，则循环使用这些颜色
            const colors = {
            background: [],
            border: []
            };
            for (let i = 0; i < numOptions; i++) {
            const index = i % baseColors.length;
            colors.background.push(baseColors[index]);
            colors.border.push(baseColors[index].replace('0.2)', '1)')); // 将透明度从0.2改为1
            }
            return colors;
        },
    }
  };
  </script>
  
  <style scoped>
  .common-layout {
    display: flex;  
    flex-direction: column;
    min-height: 100vh; /* 使得父容器至少有一个视窗的高度 */
  }
  
  el-header, el-main, el-container {
    display: flex;
    flex-direction: column;
  }
  
  el-main {
    flex: 1;
    display: flex;
    justify-content: center; /* 在垂直方向上居中内容 */
    align-items: center; /* 在水平方向上居中内容 */
  }
  
  .mytable {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: #f9f9f9;
    /* Added styles */
    margin: 0 auto; /* 水平居中 */
    max-width: 80%; /* 限制最大宽度，让内容不会过于分散 */
    box-shadow: 0px 2px 15px rgba(0, 0, 0, 0.3);
    border-radius: 5px;
    overflow: hidden; /* 隐藏溢出的内容 */
    border: 1px solid #d8d8d8;
    border-bottom: 2px solid #d8d8d8;
    border-radius: 5px;
    background-color: #fff;
    color: #565a5c;
    font-family: "Open Sans", sans-serif;
    font-weight: 400;
    text-shadow: none;
    box-sizing: border-box;
    font-size: 12px;
    line-height: 32px;
    font-size: 1rem;
    line-height: 6rem;
    font-weight: 400;
  }
  .chart-container {
    width: 600px; /* 调整为你希望的宽度 */
    height: 400px; /* 调整为你希望的高度 */
    margin: 0 auto; /* 水平居中 */
    padding: 20px;
    max-width: 80%; /* 限制最大宽度，让内容不会过于分散 */
    display: flex;
    justify-content: center; /* 在水平方向上居中内容 */
    align-items: center; /* 在垂直方向上居中内容 */
  }
  </style>