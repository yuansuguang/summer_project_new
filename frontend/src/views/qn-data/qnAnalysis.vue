<template>
    <div>
      <el-row type="flex" justify="center">
        <el-col :span="12">
          <h1>问卷交叉分析</h1>
          <el-form>
            <el-form-item label="选择分析的第一个维度：">
              <el-select v-model="selectedPrimary" placeholder="请选择">
                <el-option
                  v-for="question in questionsData"
                  :key="question.name"
                  :label="question.displayName"
                  :value="question.name">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="选择分析的第二个维度：">
              <el-select v-model="selectedSecondary" placeholder="请选择">
                <el-option
                  v-for="question in questionsData"
                  :key="question.name"
                  :label="question.displayName"
                  :value="question.name">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="performAnalysis">执行分析</el-button>
              <el-button type="success" @click="exportToExcel">导出Excel</el-button>
              <el-button type="warning  " @click="exportChart">导出立体图</el-button>
            </el-form-item>
          </el-form>
          <div v-if="analysisResult && Object.keys(analysisResult).length">
            <h2>分析结果：</h2>
            <el-card class="box-card" v-for="(result, key) in analysisResult" :key="key">
              <div>
                <h3>{{ getDisplayName(key) }}:</h3>
                <el-list v-for="(count, answer) in result" :key="answer">
                  <el-list-item>{{ getDisplayName(answer) }}: {{ count }} 次<br></el-list-item>
                </el-list>
              </div>
            </el-card>
            <h2>交叉分析表格：</h2>
            <el-table :data="formattedTableData" style="width: 100%" stripe>
                <el-table-column prop="primary" label="第一维度"></el-table-column>
                <el-table-column prop="secondary" label="第二维度"></el-table-column>
                <el-table-column prop="count" label="计数"></el-table-column>
            </el-table>
            <div id="chart" style="width: 800px;height:600px;"></div>
          </div>
        </el-col>
      </el-row>
    </div>
  </template>

<script>
  import {nextTick } from 'vue';
  import * as echarts from 'echarts';
  import 'echarts-gl';
  import * as XLSX from 'xlsx';
  
  export default {
    data() {
      return {
        selectedPrimary: '',
        selectedSecondary: '',
        analysisResult: {},
        surveyData: [
          
        ],
        myChart: null
      };
    },
    computed: {
      questionsData() {
        if (!this.surveyData.length || !this.surveyData[0].length) return [];
        const questionSet = new Set();
        this.surveyData.forEach(response => {
          response.forEach(item => {
            questionSet.add(item.question_description);
          });
        });
        return Array.from(questionSet).map(question => ({ 
          name: question, 
          displayName: question 
        }));
      },
      formattedTableData() {
        let tableData = [];
        if (Object.keys(this.analysisResult).length) {
            Object.keys(this.analysisResult).forEach(primary => {
            Object.keys(this.analysisResult[primary]).forEach(secondary => {
                tableData.push({
                primary: this.getDisplayName(primary),
                secondary: this.getDisplayName(secondary),
                count: this.analysisResult[primary][secondary]
                });
            });
            });
        }
        return tableData;
      }
    },
    methods: {
      performAnalysis() {
        const primaryQuestionDescription = this.selectedPrimary;
        const secondaryQuestionDescription = this.selectedSecondary;
        let analysisMap = new Map();
  
        this.surveyData.forEach(response => {
          const primaryResponse = response.find(item => item.question_description === primaryQuestionDescription).answer;
          const secondaryResponse = response.find(item => item.question_description === secondaryQuestionDescription).answer;
  
          if (!analysisMap.has(primaryResponse)) {
            analysisMap.set(primaryResponse, {});
          }
  
          const secondaryCounts = analysisMap.get(primaryResponse);
          secondaryCounts[secondaryResponse] = (secondaryCounts[secondaryResponse] || 0) + 1;
        });
  
        let result = {};
        analysisMap.forEach((counts, primaryAnswer) => {
          result[primaryAnswer] = counts;
        });
  
        this.analysisResult = result;
  
        // Ensure the chart updates with the new analysis result
        nextTick(() => {
          if (Object.keys(this.analysisResult).length > 0) {
            this.setChart();
          }
        });
      },
      getDisplayName(questionName) {
        const question = this.questionsData.find(q => q.name === questionName);
        return question ? question.displayName : questionName;
      },
      setChart() {
        nextTick(() => {
          const chartDom = document.getElementById('chart');
          if (chartDom && this.analysisResult) {
            this.myChart = echarts.init(chartDom);
            const dimensions = { x: '', y: '', z: '' };
  
            let data = [];
            let xData = [];
            let yData = [];
            Object.keys(this.analysisResult).forEach(x => {
              Object.keys(this.analysisResult[x]).forEach(y => {
                data.push([x, y, this.analysisResult[x][y]]);
                if (xData.indexOf(x) === -1) xData.push(x);
                if (yData.indexOf(y) === -1) yData.push(y);
              });
            });
  
            dimensions.x = this.selectedPrimary;
            dimensions.y = this.selectedSecondary;
            dimensions.z = '数量';
  
            let option = {
              tooltip: {},
              visualMap: {
                max: 20,
                inRange: {
                  color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
                }
              },
              xAxis3D: {
                type: 'category',
                data: xData,
                name: dimensions.x,
                axisLabel: {
                  formatter: function (value) {
                    return value;
                  }
                }
              },
              yAxis3D: {
                type: 'category',
                data: yData,
                name: dimensions.y
              },
              zAxis3D: {
                type: 'value',
                name: dimensions.z
              },
              grid3D: {
                boxWidth: 200,
                boxDepth: 80,
                viewControl: {
                  // projection: 'orthographic'
                },
                light: {
                  main: {
                    intensity: 1.2,
                    shadow: true
                  },
                  ambient: {
                    intensity: 0.3
                  }
                }
              },
              series: [{
                type: 'bar3D',
                data: data.map(function (item) {
                  return {
                    value: [item[0], item[1], item[2]],
                  }
                }),
                shading: 'lambert',
                label: {
                  textStyle: {
                    fontSize: 16,
                    borderWidth: 1
                  }
                },
                emphasis: {
                  label: {
                    textStyle: {
                      fontSize: 20,
                      color: '#900'
                    }
                  },
                  itemStyle: {
                    color: '#900'
                  }
                }
              }]
            };
            this.myChart.setOption(option);
          }
        });
      },
      exportToExcel() {
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(this.formattedTableData);
        XLSX.utils.book_append_sheet(wb, ws, 'AnalysisResult');
        XLSX.writeFile(wb, 'analysis_result.xlsx');
      },
      exportChart() {
        if (this.myChart) {
          const img = new Image();
          const url = this.myChart.getDataURL({
            pixelRatio: 2,
            backgroundColor: '#fff'
          });
  
          img.src = url;
          // 创建下载链接并点击进行下载
          const a = document.createElement('a');
          a.download = 'chart.png';
          a.href = url;
          a.click();
        }
      },
      fetchsubmission() {
        var param = {
                    survey_id: this.$route.params.qnid
                };
        var paramer = JSON.stringify(param);
        console.log(paramer);
                this.$axios({
                    method: 'post',
                    url: '/submit/api/get_survey_submissions',
                    data: paramer,
                })
                    .then(res => {
                      switch (res.data.status_code) {
                case 1:
                    this.surveyData = res.data.submissions;
                    console.log("success on fetching survey data");
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
                    console.log(res.data.message);
                    break;
                case -1:
                    break;
                }
            }).catch(err => {
                console.log(err);
            });
      }
    },
    created() {
      this.fetchsubmission();
    },
    mounted() {
      if (this.questionsData.length > 0) {
        this.selectedPrimary = this.questionsData[0].name;
        this.selectedSecondary = this.questionsData.length > 1 ? this.questionsData[1].name : this.questionsData[0].name;
      }
    },
    watch: {
      analysisResult(newVal) {
        if (newVal) {
          this.setChart();
        }
      }
    }
  };
  </script>
  
  
  <style>
  .box-card {
    margin-bottom: 20px;
  }
  
  .el-col {
    padding-top: 100px; /* Adjust this value as necessary */
  }

  /* 图表区域样式 */
  #chart {
    margin-top: 20px;
    padding: 15px;
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  }

  /* 按钮区域样式 */
  .chart-buttons {
    display: flex;
    justify-content: center;
  }
  </style>