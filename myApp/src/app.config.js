export default {
  pages: [
    'pages/overview/index',
    'pages/tasks/index',
    'pages/upload/index',
    'pages/settings/index',
  ],
  tabBar: {
    color: '#999',
    selectedColor: '#1677ff',
    backgroundColor: '#fff',
    borderStyle: 'black',
    list: [
      { pagePath: 'pages/overview/index', text: '概览' },
      { pagePath: 'pages/tasks/index',    text: '任务' },
      { pagePath: 'pages/upload/index',   text: '上传' },
      { pagePath: 'pages/settings/index', text: '设置' },
    ],
  },
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#1677ff',
    navigationBarTitleText: '图像预处理系统',
    navigationBarTextStyle: 'white',
  },
}